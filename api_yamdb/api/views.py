from .models import Category, Genre, Title
from .mixins import (
    CreateByAdminOrReadOnlyModelMixin,
    CreateOrChangeByAdminOrReadOnlyModelMixin
)
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(CreateByAdminOrReadOnlyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)


class GenreViewSet(CreateByAdminOrReadOnlyModelMixin):
    serializer_class = GenreSerializer
    search_fields = ('name',)
    queryset = Genre.objects.all()


class TitleViewSet(CreateOrChangeByAdminOrReadOnlyModelMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
