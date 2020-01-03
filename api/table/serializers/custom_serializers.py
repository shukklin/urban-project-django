from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object


class LocationSerializer(serializers.ModelSerializer):
    location = PointField()
    in_property = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ['id', 'location', 'in_property']

    def get_in_property(self, obj):
        return obj.user == self.context.get('request').user