from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Category, Genre, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    username = serializers.RegexField(r'^[\w.@+-]+\Z',
                                      max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'username':
                 'Нельзя использовать \'me\' как имя пользователя.'}
            )
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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
