from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import *


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'corporation', 'avatar')
        extra_kwargs = {'password': {
            'write_only': True
        }}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'experience',
                  'money', 'corporation', 'avatar')
        read_only_fields = ('experience', 'money', 'username')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = '__all__'


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'
        read_only_fields = ('experience', 'money')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class UserActivityHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityHistory
        fields = '__all__'
        read_only_fields = ('user',)


class SubObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubObjectType
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    location = PointField()

    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class ObjectPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPhoto
        fields = '__all__'

    def create(self, validated_data):
        return ObjectPhoto.objects.create(**validated_data)
