"""Модуль содержит сериализаторы, используемые в REST API."""
from django.utils.timezone import datetime
from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    Получение экземпляров по полю slug.
    """
    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    Получение экземпляров по полю slug.
    """
    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Применяется для методов POST и PATCH.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    description = serializers.CharField(required=False)

    def validate_year(self, value):
        year = datetime.today().year
        if value <= 0 or value > year:
            raise serializers.ValidationError(
                'Год указан некорректно.'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReadTitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Применяется для метода GET.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Применяется для самостоятельного создания пользователя и получения
    кода подтверждения.
    Не допускает использования me в качестве username.
    """
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    @staticmethod
    def validate_username(username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'username':
                 f'Нельзя использовать \'{username}\' как имя пользователя.'}
            )
        return username

    def validate(self, attrs):
        """
        Логика проверки частичного присутствия имени или адреса почты
        в имеющихся пользователях.
        Если есть полное совпадение - занчит запрос на себя для получения
        кода подтверждения, всё валидно.
        Если в базе есть пользователи с совпавшим username или email,
        то какое-то из полей не валидно. Информируем об этом пользователя.
        Если в базе нет совпавших ни username ни email - значит запрос
        на создание нового пользователя, всё валидно.
        """
        if User.objects.filter(username=attrs['username'],
                               email=attrs['email']).exists():
            return attrs
        if (
            User.objects.filter(username=attrs['username']).exists()
            or User.objects.filter(email=attrs['email']).exists()
        ):
            message_dict = {}
            if User.objects.filter(username=attrs['username']).exists():
                message_dict.update(
                    {
                        'username':
                        'Пользователь с именем {} уже есть в базе.'.format(
                            attrs['username']
                        )
                    }
                )
            if User.objects.filter(email=attrs['email']).exists():
                message_dict.update(
                    {
                        'email':
                        'Пользователь с адресом {} уже есть в базе.'.format(
                            attrs['email']
                        )
                    }
                )
            raise serializers.ValidationError(message_dict)
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Используется для управления пользователями.
    """
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким именем уже существует.'
            )
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким адресом почты уже существует.'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'


class ConfirmationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Используется для запросов токенов доступа.
    Проверяется соответствие переданного кода и кода, хранящегося в модели.
    """
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if not user.confirmation_code == attrs['confirmation_code']:
            raise serializers.ValidationError(
                {'confirmation_code': 'Код подтверждения некорректен.'}
            )
        return attrs

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    Выполняется контроль правила 'от каждого пользователя возможен только
    один отзыв на каждое произведение'.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    def validate(self, attrs):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Извините, возможен только один отзыв'
                )
        return attrs

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'score', 'title')
        read_only_fields = ('id', 'title')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('review', 'id',)
        model = Comment
