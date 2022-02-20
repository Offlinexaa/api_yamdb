from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api_v1'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet,
                basename='categories api endpoint')
router.register('genres', views.GenreViewSet,
                basename='genres api endpoint')
router.register('titles', views.TitleViewSet,
                basename='titles api endpoint')


urlpatterns = [ path('v1/', include(router.urls)),]
