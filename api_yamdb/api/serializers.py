from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Genre, Title, User, USER_ROLES


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


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
