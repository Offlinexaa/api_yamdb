"""Модуль управления путями для api."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, ConfirmAPIView,
                    GenreViewSet, NewUserAPIView, ReviewViewSet, TitleViewSet,
                    UserViewSet)

app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', NewUserAPIView.as_view(), name='new_user'),
    path('v1/auth/token/', ConfirmAPIView.as_view(), name='confirm_user'),
    path('v1/', include(v1_router.urls)),
]
