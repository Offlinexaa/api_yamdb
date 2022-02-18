from rest_framework import mixins, viewsets

from .permissions import (AdminOrReadonly)


class CreateByAdminOrReadOnlyModelMixin(mixins.CreateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    permission_classes = (AdminOrReadonly)