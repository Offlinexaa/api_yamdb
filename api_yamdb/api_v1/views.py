from .models import Category, Genre
from .mixins import (CreateByAdminOrReadOnlyModelMixin)
from .serializers import (CategorySerializer, GenreSerializer)


class CategoryViewSet(CreateByAdminOrReadOnlyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)


class GenreViewSet(CreateByAdminOrReadOnlyModelMixin):
    serializer_class = GenreSerializer
    search_fields = ('name',)
    queryset = Genre.objects.all()
