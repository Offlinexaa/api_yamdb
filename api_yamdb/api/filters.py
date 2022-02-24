"""Модуль содержит самописные фильтры."""
import django_filters as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """
    Фильтр для произведений, спроектирован по требованиям тестов.
    Имя произведения фильтруется по частичному совпадению.
    """
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    year = filters.NumberFilter(field_name='year')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = '__all__'
