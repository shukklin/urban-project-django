from django.db.models import Sum
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

    def get_in_progress(self, obj):
        return MissionUser.objects.filter(user=self.context.get('request').user, start_timestamp__isnull=False, end_timestamp__isnull=True, mission=obj).exists()

    def get_is_finished(self, obj):
        return MissionUser.objects.filter(user=self.context.get('request').user, end_timestamp__isnull=False, mission=obj).exists()

    class Meta:
        model = Mission
        fields = '__all__'

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
