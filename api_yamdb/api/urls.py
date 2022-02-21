"""Модуль управления путями для api."""
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, NewUserAPIView, ConfirmAPIView


app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('auth/signup/', NewUserAPIView.as_view(), name='new_user'),
    path('auth/token/', ConfirmAPIView.as_view(), name='confirm_user'),
]
