from django.conf.urls import url, include

from api.table.entity.object_views import ObjectViewSet
from api.table.entity.user_views import UserViewSet
from . import views
from api.table.entity import object_views
from .entity import object_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'objects', ObjectViewSet, basename='object')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls