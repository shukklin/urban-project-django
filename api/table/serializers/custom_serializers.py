from drf_extra_fields.geo_fields import PointField

from api.models import Object
from api.table.serializers.object_serializers import ObjectSerializer


class LocationSerializer(ObjectSerializer):
    location = PointField()

    class Meta:
        model = Object
        fields = ['id', 'location', 'is_own_object']
