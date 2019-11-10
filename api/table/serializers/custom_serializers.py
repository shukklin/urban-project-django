from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object


class LocationSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Object
        fields = ['id', 'location']