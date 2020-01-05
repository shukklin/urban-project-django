from rest_framework.routers import DefaultRouter

from api.table.views.corporation_views import CorporationViewSet
from api.table.views.mission_user_views import MissionUserViewSet
from api.table.views.mission_views import MissionViewSet
from api.table.views.object_views import ObjectViewSet
from api.table.views.user_views import UserViewSet

router = DefaultRouter()

router.register(r'objects', ObjectViewSet, basename='objects')
router.register(r'users', UserViewSet, basename='users')
router.register(r'corporations', CorporationViewSet, basename='corporations')
router.register(r'missions', MissionViewSet, basename='missions')
router.register(r'missionsuser', MissionUserViewSet, basename='missionsuser')

urlpatterns = router.urls
