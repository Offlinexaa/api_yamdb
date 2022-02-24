from django.core.mail import send_mail
from rest_framework import viewsets, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, User, Title, Review
from .permissions import (AdminOnly, AdminOrReadonly,
                          AuthorModeratorAdminOrReadonly)
from .mixins import (CreateByAdminOrReadOnlyModelMixin,
                     CreateOrChangeByAdminOrReadOnlyModelMixin,
                     PostByAny)
from .serializers import (CategorySerializer, GenreSerializer,
                          UserSerializer, ConfirmationSerializer,
                          TitleSerializer, UserCreateUpdateSerializer,
                          ReviewSerializer, CommentSerializer)


class CategoryViewSet(CreateByAdminOrReadOnlyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(CreateByAdminOrReadOnlyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)



class TitleViewSet(CreateOrChangeByAdminOrReadOnlyModelMixin):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User. Доступен только администраторам."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'


class NewUserAPIView(PostByAny):
    """
    Класс представления для создания пользователя.
    Пользователь создаётся с правами user.
    В поле confirmation_code модели user сохраняется код подтверждения.
    На электронный адрес пользователя отправляется письмо с кодом
    подтверждения.
    """
    def post(self, request, *args, **kwargs):
        def _check_not_exist_partial():
            """
            Логика проверки частичного присутствия имени или адреса почты
            в имеющихся пользователях.
            """
            if User.objects.filter(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            ).exists() or (not User.objects.filter(
                username=serializer.validated_data['username']
            ).exists() and not User.objects.filter(
                email=serializer.validated_data['email']
            ).exists()):
                return True
            return False

        serializer = UserCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if _check_not_exist_partial():
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


class UserSelfManagementAPIView(RetrieveUpdateAPIView):
    """
    Класс управления собственным пользователем.
    """
    def retrieve(self, request, *args, **kwargs):
        serializer = UserCreateUpdateSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = UserCreateUpdateSerializer(request.user,
                                                data=request.data,
                                                partial=True)
        if serializer.is_valid():
            if (
                'role' in serializer.validated_data
                and request.user.role != 'admin'
            ):
                serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrReadonly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AdminOrReadonly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrReadonly,)

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
        if self.action == 'list' or self.action == 'retrieve':
            return (AdminOrReadonly(),)
        return super().get_permissions()
