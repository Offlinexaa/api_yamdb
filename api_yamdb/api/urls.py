"""Модуль управления путями для api."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (UserViewSet, NewUserAPIView, ConfirmAPIView,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    UserSelfManagementAPIView)


app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet,
                   basename='categories api endpoint')
v1_router.register('genres', GenreViewSet,
                   basename='genres api endpoint')
v1_router.register('titles', TitleViewSet,
                   basename='titles api endpoint')

urlpatterns = [
    path('auth/signup/', NewUserAPIView.as_view(), name='new_user'),
    path('auth/token/', ConfirmAPIView.as_view(), name='confirm_user'),
    path('users/me/', UserSelfManagementAPIView.as_view(),
         name='self_management'),
    path('', include(v1_router.urls)),
]
