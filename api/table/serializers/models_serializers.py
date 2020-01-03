from django.db.models import Sum
from rest_framework import serializers

from api.models import *


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
        return User.objects.create(**validated_data)


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'


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
