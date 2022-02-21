from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import AllowAny

from .permissions import (AdminOrReadonly)


class CreateByAdminOrReadOnlyModelMixin(mixins.CreateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    permission_classes = (AdminOrReadonly)


class CreateOrChangeByAdminOrReadOnlyModelMixin(mixins.CreateModelMixin,
                                                mixins.ListModelMixin,
                                                mixins.DestroyModelMixin,
                                                mixins.UpdateModelMixin,
                                                viewsets.GenericViewSet):
    permission_classes = AdminOrReadonly


class PostByAny(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny, )
