"""Модуль управления путями для api."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api_v1.views import UserViewSet


app_name = 'api_v1'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls))
]
