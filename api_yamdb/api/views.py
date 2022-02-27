"""Модуль содержит вьюсеты и вью-классы."""
from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import (CreateByAdminOrReadOnlyModelMixin,
                     CreateOrChangeByAdminOrReadOnlyModelMixin, PostByAny)
from .permissions import (AdminOnly, AdminOrReadonly,
                          AuthorModeratorAdminOrReadonly)
from .serializers import (CategorySerializer, CommentSerializer,
                          ConfirmationSerializer, GenreSerializer,
                          ReadTitleSerializer, ReviewSerializer,
                          TitleSerializer, UserCreateSerializer,
                          UserSerializer)


class CategoryViewSet(CreateByAdminOrReadOnlyModelMixin):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(CreateByAdminOrReadOnlyModelMixin):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class TitleViewSet(CreateOrChangeByAdminOrReadOnlyModelMixin):
    """
    Вьюсет для модели Title.
    Для метода GET применяется сериализатор ReadTitleSerializer.
    Для других методов применяется сериализатор TitleSerializer.
    Добавляется динамическое поле, содержащее агрегирующую функцию.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadTitleSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели User.
    Доступен только администраторам.
    Получение экземпляра модели User по полю username.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me(self, request):
        """
        Функция управления собственным пользователем.
        При попытке изменения роли кем-либо, кроме администратора,
        в базу передаётся текущая роль пользователя.
        """
        if request.method.lower() == 'get':
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            if (
                'role' in serializer.validated_data
                and not request.user.is_admin
            ):
                serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewUserAPIView(PostByAny):
    """
    Класс представления для создания пользователя.
    Пользователь создаётся с правами user.
    В поле confirmation_code модели user сохраняется код подтверждения.
    На электронный адрес пользователя отправляется письмо с кодом
    подтверждения.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            if not User.objects.filter(
                username=serializer.validated_data['username']
            ).exists():
                serializer.save(role='user')
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
            user.confirmation_code = str(RefreshToken.for_user(user))
            user.save(update_fields=['confirmation_code'])
            mail = EmailMessage(
                subject='Confirmation code.',
                body=user.confirmation_code,
                to=[user.email, ]
            )
            mail.send(fail_silently=True)
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAPIView(PostByAny):
    """
    Класс представления для получения токена доступа по коду подтверждения.
    """
    def post(self, request, *args, **kwargs):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
            user.confirmation_code = ''
            user.save(update_fields=['confirmation_code'])
            return Response(
                {'token':
                 str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadonly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AdminOrReadonly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadonly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (AdminOrReadonly(),)
        return super().get_permissions()
