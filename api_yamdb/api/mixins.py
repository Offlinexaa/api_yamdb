"""Модуль содержит самописные миксины."""
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny

from .permissions import AdminOrReadonly


class CreateByAdminOrReadOnlyModelMixin(mixins.CreateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    """
    Миксин для вюсетов: методы GET (только список), POST и DELETE.
    GET - разрешён всем.
    POST, DELETE - только администраторам.
    """
    permission_classes = (AdminOrReadonly, )


class CreateOrChangeByAdminOrReadOnlyModelMixin(mixins.CreateModelMixin,
                                                mixins.ListModelMixin,
                                                mixins.DestroyModelMixin,
                                                mixins.UpdateModelMixin,
                                                mixins.RetrieveModelMixin,
                                                viewsets.GenericViewSet):
    """
    Миксин для вюсетов: методы GET , POST, PATCH и DELETE.
    GET - разрешён всем.
    POST, PATCH, DELETE - только администраторам.
    """
    permission_classes = (AdminOrReadonly, )


class PostByAny(mixins.CreateModelMixin, generics.GenericAPIView):
    """Миксин для классов: метод POST, разрешён всем."""
    permission_classes = (AllowAny, )
