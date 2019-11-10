from api.table.views.activity_views import ActivityViewSet
from api.table.views.corporation_views import CorporationViewSet
from api.table.views.object_views import ObjectViewSet
from api.table.views.objecttype_views import ObjectTypeViewSet
from api.table.views.photo_views import PhotoViewSet
from api.table.views.subobjecttype_views import SubObjectTypeViewSet
from api.table.views.user_views import UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'objects', ObjectViewSet, basename='objects')
router.register(r'users', UserViewSet, basename='users')
router.register(r'corporations', CorporationViewSet, basename='corporations')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'objecttypes', ObjectTypeViewSet, basename='objecttypes')
router.register(r'photos', PhotoViewSet, basename='photos')
router.register(r'subobjecttypes', SubObjectTypeViewSet, basename='subobjecttypes')

urlpatterns = router.urls
