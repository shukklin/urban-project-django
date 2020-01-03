from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object
from api.table.serializers.models_serializers import ObjectSerializer


class LocationSerializer(ObjectSerializer):
    location = PointField()

    class Meta:
        model = Object
        fields = ['id', 'location', 'in_property']
