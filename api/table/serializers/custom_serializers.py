from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object, User
from api.table.serializers.object_serializers import ObjectSerializer


class LocationSerializer(ObjectSerializer):
    location = PointField()

    class Meta:
        model = Object
        fields = ['id', 'location', 'is_own_object']

class ChangeUserCorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['corporation']