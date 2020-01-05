import datetime

from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Object, ObjectsUserManage
from api.table.constants.object_constants import OBJECT_LOCKED_IN_DAYS, OBJECT_LOST_IN_DAYS, OBJECT_CAPTURE_STREAK_COUNT
from api.table.helpers.ObjectHelper import ObjectHelper


class ObjectSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    manage_status = serializers.SerializerMethodField(read_only=True)
    user_corporation = serializers.CharField(source='user.corporation', read_only=True)
    location = PointField()
    offense_status = serializers.SerializerMethodField()
    locked_manage_until = serializers.SerializerMethodField(read_only=True)
    in_property = serializers.SerializerMethodField(read_only=True)
    can_be_captured = serializers.SerializerMethodField(read_only=True)
    until_capture_count = serializers.SerializerMethodField(read_only=True)

    def get_until_capture_count(self, obj):
        return OBJECT_CAPTURE_STREAK_COUNT - ObjectsUserManage.objects.filter(timestamp__gt=obj.timestamp, user=self.context.get('request').user).count()

    def get_can_be_captured(self, obj):
        return ObjectHelper.can_object_be_captured(obj, self.context.get('request').user)

    def get_locked_manage_until(self, obj):
        return (obj.timestamp + datetime.timedelta(
           OBJECT_LOCKED_IN_DAYS))

    def get_offense_status(self, obj):
        return ObjectsUserManage.objects.filter(object_id=obj.id, timestamp__gt=obj.timestamp).exclude(user=obj.user).count()

    def get_manage_status(self, obj):
        return (datetime.datetime.now(datetime.timezone.utc) - obj.timestamp).days

    def get_in_property(self, obj):
        return ObjectHelper.is_in_property(obj, self.context.get('request').user)

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

class ObjectCaptureSerializer(ObjectSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        read_only_fields = ('location', 'isActivated')
