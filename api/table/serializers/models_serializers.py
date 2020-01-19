from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import *
from api.table.helpers.MissionHelper import MissionHelper


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
    objects_count = serializers.SerializerMethodField(read_only=True)
    corporation = serializers.StringRelatedField(read_only=True)

    def get_objects_count(self, obj):
        return Object.objects.filter(user=obj).count()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'experience',
                  'money', 'corporation', 'avatar', 'activity', 'objects_count')
        read_only_fields = ('experience', 'money', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class MissionSerializer(serializers.ModelSerializer):
    in_progress = serializers.SerializerMethodField(read_only=True)
    is_finished = serializers.SerializerMethodField(read_only=True)
    can_finish = serializers.SerializerMethodField(read_only=True)
    current_progress = serializers.SerializerMethodField(read_only=True)

    def get_in_progress(self, obj):
        return MissionUser.objects.filter(user=self.context.get('request').user, start_timestamp__isnull=False,
                                          end_timestamp__isnull=True, mission=obj).exists()

    def get_is_finished(self, obj):
        try:
            user_mission = get_object_or_404(
                MissionUser.objects.filter(mission_id=obj.id, user=self.context.get('request').user))
        except:
            return None
        return MissionHelper.is_mission_finished(user_mission)

    def get_can_finish(self, obj):
        try:
            user_mission = get_object_or_404(
                MissionUser.objects.filter(mission_id=obj.id, user=self.context.get('request').user))
            mission = get_object_or_404(Mission.objects.all(), pk=obj.id)
        except:
            return None

        return not MissionHelper.is_mission_finished(user_mission) and (
                    MissionHelper.is_mission_done(user_mission, mission, self.context.get(
                        'request').user))

    def get_current_progress(self, obj):
        try:
            user_mission = get_object_or_404(
                MissionUser.objects.filter(mission_id=obj.id, user=self.context.get('request').user))
        except:
            return None
        return MissionHelper.get_manage_done_count(user_mission, self.context.get('request').user)

    class Meta:
        model = Mission
        fields = '__all__'


class MissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ('id', 'name')


class MissionUserSerializer(serializers.ModelSerializer):
    mission = serializers.StringRelatedField(read_only=True)
    until_manage_done_count = serializers.SerializerMethodField(read_only=True)

    def get_until_manage_done_count(self, obj):
        if obj.mission.activity == EActivityStatus.BUSINESS:
            return MissionHelper.get_manage_done_count(obj, self.context.get('request').user)
        elif obj.mission.activity == EActivityStatus.ADMIN:
            return MissionHelper.get_admin_manage_done_count(obj, self.context.get('request').user)

    class Meta:
        model = MissionUser
        fields = '__all__'
        read_only_fields = ('user', 'start_timestamp', 'end_timestamp')

    def create(self, validated_data):
        return MissionUser.objects.create(**validated_data)


class CorporationSerializer(serializers.ModelSerializer):
    count_players = serializers.SerializerMethodField(read_only=True)
    experience = serializers.SerializerMethodField(read_only=True)
    money = serializers.SerializerMethodField(read_only=True)
    is_member = serializers.SerializerMethodField(read_only=True)

    def get_is_member(self, obj):
        return User.objects.filter(pk=self.context.get('request').user.id, corporation=obj).exists()

    def get_money(self, obj):
        return User.objects.filter(corporation=obj).aggregate(Sum('money'))['money__sum']

    def get_experience(self, obj):
        return User.objects.filter(corporation=obj).aggregate(Sum('experience'))['experience__sum']

    def get_count_players(self, obj):
        return User.objects.filter(corporation=obj).count()

    class Meta:
        model = Corporation
        fields = '__all__'
        read_only_fields = ('experience', 'money')


class ObjectUserManageSerializer(serializers.ModelSerializer):
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
