from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from api_v1.models import User
from api_v1.serializers import UserSerializer
from api_v1.permissions import AdminOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    pagination_class = PageNumberPagination
