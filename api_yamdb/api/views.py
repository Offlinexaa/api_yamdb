from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Category, Genre, User
from .permissions import AdminOnly
from .mixins import (CreateByAdminOrReadOnlyModelMixin)
from .serializers import (CategorySerializer, GenreSerializer,
                          UserSerializer)


class CategoryViewSet(CreateByAdminOrReadOnlyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)


class GenreViewSet(CreateByAdminOrReadOnlyModelMixin):
    serializer_class = GenreSerializer
    search_fields = ('name',)
    queryset = Genre.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = PageNumberPagination
