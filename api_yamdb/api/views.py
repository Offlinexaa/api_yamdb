from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from reviews.models import Category, Genre, User, Title
from .permissions import AdminOnly
from .mixins import (CreateByAdminOrReadOnlyModelMixin,
                     CreateOrChangeByAdminOrReadOnlyModelMixin,
                     PostByAny)
from .serializers import (CategorySerializer, GenreSerializer,
                          UserSerializer, ConfirmationSerializer,
                          TitleSerializer)


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


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User. Доступен только администраторам."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = PageNumberPagination


class NewUserAPIView(PostByAny):
    """
    Класс представления для создания пользователя.
    Пользователь создаётся с правами user.
    В поле confirmation_code модели user сохраняется код подтверждения.
    На электронный адрес пользователя отправляется письмо с кодом
    подтверждения.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
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
            send_mail(
                subject='Confirmation code.',
                message=user.confirmation_code,
                from_email='noreply@yamdb.local',
                recipient_list=[user.email, ]
            )
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
