import datetime

from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object, ObjectsUserManage
from api.table.enums.EActivityStatus import EActivityStatus
from api.table.helpers.ObjectHelper import ObjectHelper


class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    manage_status = serializers.SerializerMethodField(read_only=True)
    user_corporation = serializers.CharField(source='user.corporation', read_only=True)
    location = PointField()
    offense_status = serializers.SerializerMethodField()
    locked_manage_until = serializers.SerializerMethodField(read_only=True)
    is_own_object = serializers.SerializerMethodField(read_only=True)
    can_be_captured = serializers.SerializerMethodField(read_only=True)
    can_be_managed = serializers.SerializerMethodField(read_only=True)
    can_be_activated = serializers.SerializerMethodField(read_only=True)
    can_be_deleted = serializers.SerializerMethodField(read_only=True)
    until_capture_count = serializers.SerializerMethodField(read_only=True)

    def get_until_capture_count(self, obj):
        capture_count = ObjectHelper.OBJECT_CAPTURE_STREAK_COUNT - ObjectsUserManage.objects.filter(timestamp__gt=obj.timestamp, user=self.context.get('request').user).count()

        if capture_count > 0:
            return capture_count
        return 0

    def get_can_be_captured(self, obj):
        return ObjectHelper.can_object_be_captured(obj, self.context.get('request').user)

    def get_can_be_activated(self, obj):
        return ObjectHelper.can_be_activated(obj, self.context.get('request').user)

    def get_can_be_deleted(self, obj):
        return ObjectHelper.can_be_deleted(obj, self.context.get('request').user)

    def get_can_be_managed(self, obj):
        return ObjectHelper.can_be_managed(obj, self.context.get('request').user)

    def get_locked_manage_until(self, obj):
        locked_until_dt = (obj.timestamp + datetime.timedelta(
           ObjectHelper.OBJECT_LOCKED_IN_DAYS))
        throttling_locked_until_dt = (obj.timestamp + datetime.timedelta(
           ObjectHelper.OBJECT_MANAGE_THROTTLING))

        return max(locked_until_dt, throttling_locked_until_dt)

    def get_offense_status(self, obj):
        return ObjectsUserManage.objects.filter(object_id=obj.id, timestamp__gt=obj.timestamp).exclude(user=obj.user).count()

    def get_manage_status(self, obj):
        return (datetime.datetime.now(datetime.timezone.utc) - obj.timestamp).days

    def get_is_own_object(self, obj):
        return self.context.get('request').user.id == obj.user.id

    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('id', 'user', 'isActivated')

    def create(self, validated_data):
        return Object.objects.create(**validated_data)


class ObjectUpdateSerializer(ObjectSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('location', 'user', 'timestamp', 'isActivated')