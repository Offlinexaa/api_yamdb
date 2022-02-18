from rest_framework import serializers

from api_v1.models import Category, Genre, User


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
    username = serializers.RegexField(r'^[\w.@+-]+\z)',
                                      max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False, default='user')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
