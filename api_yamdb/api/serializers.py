from datetime import date
from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404

from reviews.models import (Category, Genre, Title, User, USER_ROLES,
                            Review, Comment)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )
    description = serializers.CharField(required=False)

    def validate_year(self, value):
        year = date.today().year
        if value <= 0 or value > year:
            raise serializers.ValidationError(
                'Год указан некорректно.'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReadTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=USER_ROLES, required=False)

    @staticmethod
    def validate_username(username):
        if username == 'me':
            raise serializers.ValidationError(
                {'username':
                 'Нельзя использовать \'me\' как имя пользователя.'}
            )
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')


class UserSerializer(UserCreateUpdateSerializer):
    """Сериализатор для модели User"""
    username = serializers.RegexField(
        r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким именем уже существует.')])
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким адресом почты уже существует.')])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = 'username'


class ConfirmationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not user.confirmation_code == data['confirmation_code']:
            raise serializers.ValidationError(
                {'confirmation_code': 'Код подтверждения некорректен.'}
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=author
            ).exists():
                raise serializers.ValidationError(
                    'Извините, возможен только один отзыв'
                )
        return data

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'score', 'title')
        read_only_fields = ('id', )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        read_only_fields = ('review', 'id',)
        model = Comment
