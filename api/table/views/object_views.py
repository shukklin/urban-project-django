import datetime
import math

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Object, ObjectPhoto
from api.table.enums.EAppConfig import EAppConfig
from api.table.helpers.ExperienceHelper import ExperienceHelper, EExperienceType
from api.table.helpers.MoneyHelper import MoneyHelper, EMoneyType
from api.table.helpers.ObjectHelper import ObjectHelper
from api.table.serializers.custom_serializers import LocationSerializer
from api.table.serializers.models_serializers import ObjectUserManageSerializer, ObjectPhotoSerializer
from api.table.serializers.object_serializers import ObjectSerializer, ObjectUpdateSerializer


class ObjectViewSet(viewsets.ViewSet):
    def list(self, request):
        z, lat, lng = float(request.query_params['z']), float(request.query_params['lat']), float(
            request.query_params['lng'])

        if z > 0:
            radius = math.floor(100 / z)
        else:
            return Response(status=400, data='Input parameters is not correct')

        queryset = Object.objects.filter(is_deleted__exact=False,
                                         location__distance_lt=(Point(lng, lat), Distance(km=radius)))

        context = {'request': request}
        serializer = LocationSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Object.objects.filter(is_deleted__exact=False)
        object_item = get_object_or_404(queryset, pk=pk)
        context = {'request': request}
        serializer = ObjectSerializer(object_item, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def photos(self, request):
        list_images = request.FILES.getlist('images[]')

        # If current count photos more than in conf do throw an error
        if len(list_images) > EAppConfig.MAX_UPLOAD_PHOTOS:
            return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        if len(list_images) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # prepare data for serializer
        prepared_data = [
            {
                'user': request.user.id,
                'object': self.request.data['object'],
                'url': image
            }
            for image in list_images
        ]

        serializer = ObjectPhotoSerializer(data=prepared_data, many=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'])
    def photos(self, request, pk=None):
        queryset = ObjectPhoto.objects.filter(is_deleted__exact=False)
        photos = get_list_or_404(queryset, pk=pk)
        serializer = ObjectPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def activate(self, request, pk=None):
        try:
            object_item = Object.objects.get(is_deleted__exact=False, pk=pk)

            if not ObjectHelper.can_be_activated(object_item, self.request.user):
                return Response(status=403, data='You can not activate this object')

            Object.objects.filter(is_deleted__exact=False, pk=pk).update(is_activated=True)
        except Object.DoesNotExist:
            return Response(status=404)

        MoneyHelper.add(EMoneyType.MISSION, request.user, object_item)

        return Response(status=status.HTTP_200_OK, data='Object has been activated')

    @action(detail=True, methods=['POST'])
    def manage(self, request, pk=None):
        queryset = Object.objects.filter(is_deleted__exact=False)
        object_item = get_object_or_404(queryset, pk=pk)

        current_dt = datetime.datetime.now(datetime.timezone.utc)

        if not ObjectHelper.can_be_managed(object_item, request.user):
            return Response(status=403, data='You do not have permission to manage this object')

        if ObjectHelper.is_own_object(object_item, request.user) and ObjectHelper.is_object_in_property(object_item):
            Object.objects.filter(pk=pk).update(timestamp=current_dt)

        serializer = ObjectUserManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, object_id=object_item.pk)
        MoneyHelper.add(EMoneyType.MANAGE_OBJECT, request.user, object_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        context = {'request': request}
        serializer = ObjectSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        location = serializer.validated_data['location']

        if not ObjectHelper.can_create_object(location):
            return Response(status=403, data='It is forbidden more than 1 object in ' + str(
                ObjectHelper.OBJECT_CAN_CREATE_IN_RADIUS_METERS) + 'meters radius')

        serializer.save(user=request.user)
        MoneyHelper.add(EMoneyType.CREATE_OBJECT, request.user, serializer.data)
        ExperienceHelper.add(EExperienceType.CREATE_OBJECT, request.user, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        queryset = Object.objects.filter(is_deleted__exact=False)
        object_item = get_object_or_404(queryset, pk=pk)
        context = {'request': request}
        serializer = ObjectUpdateSerializer(object_item, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(isActivate=False)
        MoneyHelper.add(EMoneyType.UPDATE_OBJECT, request.user, serializer.data)
        ExperienceHelper.add(EExperienceType.UPDATE_OBJECT, request.user, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        queryset = Object.objects.filter(is_deleted__exact=False)
        object_item = get_object_or_404(queryset, pk=pk)

        if not ObjectHelper.can_object_be_captured(object_item, request.user):
            return Response(status=403, data='You can not capture this object yet')

        current_dt = datetime.datetime.now(datetime.timezone.utc)

        Object.objects.filter(pk=pk).update(timestamp=current_dt, user=request.user)

        MoneyHelper.add(EMoneyType.CAPTURE_OBJECT, request.user, object_item)
        ExperienceHelper.add(EExperienceType.CAPTURE_UPDATE, request.user, object_item)
        return Response(data='Object was successfully captured', status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            object_item = Object.objects.get(is_deleted__exact=False, pk=pk)

            if not ObjectHelper.can_be_deleted(object_item, self.request.user):
                return Response(status=403, data='You can not delete this object')

            Object.objects.filter(is_deleted__exact=False, pk=pk).update(is_deleted=True)
        except Object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
