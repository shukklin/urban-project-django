from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password':
                {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType


class CorporationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity


class SubObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubObjectType


class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    location = PointField()

    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)
