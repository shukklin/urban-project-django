import datetime

from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import *
from api.table.constants.object_constants import OBJECT_LOST_IN_DAYS, OBJECT_LOCKED_IN_DAYS


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'password')
        extra_kwargs = {'password': {
            'write_only': True
        }}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'experience',
                  'money', 'corporation', 'avatar', 'activity')
        read_only_fields = ('experience', 'money', 'username', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = '__all__'
        read_only_fields = ('experience', 'money')

class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    manage_status = serializers.SerializerMethodField(read_only=True)
    user_corporation = serializers.CharField(source='user.corporation', read_only=True)
    location = PointField()
    offense_status = serializers.SerializerMethodField()
    locked_manage_until = serializers.SerializerMethodField(read_only=True)
    in_property = serializers.SerializerMethodField(read_only=True)

    def get_locked_manage_until(self, obj):
        return (obj.timestamp + datetime.timedelta(
           OBJECT_LOCKED_IN_DAYS))

    def get_offense_status(self, obj):
        return ObjectsUserManage.objects.filter(object_id=obj.id, timestamp__gt=obj.timestamp).exclude(user=obj.user).count()

    def get_manage_status(self, obj):
        return (datetime.datetime.now(datetime.timezone.utc) - obj.timestamp).days

    def get_in_property(self, obj):
        return obj.user == self.context.get('request').user and datetime.datetime.now(datetime.timezone.utc) <= (obj.timestamp + datetime.timedelta(OBJECT_LOST_IN_DAYS))

    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class ObjectUpdateSerializer(ObjectSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('location', 'user', 'timestamp')


class ObjectManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectsUserManage
        fields = '__all__'
        read_only_fields = ('user', 'object')

    def create(self, validated_data):
        return ObjectsUserManage.objects.create(**validated_data)


class ObjectPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPhoto
        fields = '__all__'

    def create(self, validated_data):
        return ObjectPhoto.objects.create(**validated_data)
