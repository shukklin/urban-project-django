from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
import datetime
from api.models import *
from api.table.constants.object_constants import OBJECT_LOCKED_IN_DAYS


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


class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    manage_status = serializers.SerializerMethodField()
    offensive_status = serializers.IntegerField()
    user_corporation = serializers.CharField(source='user.corporation')
    location = PointField()
    locked_until = serializers.SerializerMethodField()

    def get_locked_until(self, obj):
        return (obj.timestamp + (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(OBJECT_LOCKED_IN_DAYS)))

    def get_manage_status(self, obj):
        return (datetime.datetime.now(datetime.timezone.utc) - obj.timestamp).days

    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('id', 'user', 'user_corporation', 'manage_status', 'offensive_status')

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class ObjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('location',)

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class ObjectPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPhoto
        fields = '__all__'

    def create(self, validated_data):
        return ObjectPhoto.objects.create(**validated_data)
