from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from api.models import Tree, Photo, Record, User, SiteType, CommonName, ScientificName


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


class TreeSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Tree
        fields = '__all__'

    def create(self, validated_data):
        obj, created = Tree.objects.get_or_create(**validated_data)
        return obj, created


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Record
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)


class UserScoreSerializer(serializers.Serializer):
    common_name__name = serializers.StringRelatedField()
    common_name__name_ru = serializers.StringRelatedField()
    total_records = serializers.IntegerField()


class UsersScoresSerializer(serializers.Serializer):
    user__username = serializers.StringRelatedField()
    total_records = serializers.IntegerField()


class UserRecordSerializer(serializers.Serializer):
    date_input = serializers.DateField()
    user__username = serializers.StringRelatedField()


class ScientificNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificName
        fields = '__all__'


class CommonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonName
        fields = '__all__'


class SiteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteType
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)
