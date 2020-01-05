import datetime
import math

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Object, ObjectsUserManage, EActivityStatus
from api.table.constants.object_constants import OBJECT_CAN_CREATE_IN_RADIUS_METERS, OBJECT_CAPTURE_STREAK_COUNT
from api.table.helpers.ObjectHelper import ObjectHelper
from api.table.serializers.custom_serializers import LocationSerializer
from api.table.serializers.models_serializers import ObjectUserManageSerializer
from api.table.serializers.object_serializers import ObjectSerializer, ObjectUpdateSerializer, ObjectCaptureSerializer


class ObjectViewSet(viewsets.ViewSet):
    def list(self, request):
        z, lat, lng = float(request.query_params['z']), float(request.query_params['lat']), float(
            request.query_params['lng'])

        if z > 0:
            radius = math.floor(100 / z)
        else:
            return Response(status=400)

        queryset = Object.objects.filter(
            location__distance_lt=(Point(lng, lat), Distance(km=radius)))

        context = {'request': request}
        serializer = LocationSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Object.objects.all()
        object = get_object_or_404(queryset, pk=pk)
        context = {'request': request}
        serializer = ObjectSerializer(object, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def activate(self, request, pk=None):
        if request.user.activity != EActivityStatus.ADMIN:
            return Response(status=403, data='You must enable ADMIN activity for this action')

        Object.objects.filter(pk=pk).update(isActivated=True)

        return Response(status=status.HTTP_200_OK, data='Object has been activated')

    @action(detail=True, methods=['POST'])
    def manage(self, request, pk=None):
        queryset = Object.objects.all()
        object_item = get_object_or_404(queryset, pk=pk)

        context = {'request': request}

        serialized_object = ObjectSerializer(object_item, data=request.data, context=context)
        serialized_object.is_valid(raise_exception=True)

        current_dt = datetime.datetime.now(datetime.timezone.utc)

        locked_until = serialized_object.data['locked_manage_until']

        # if locked_until > current_dt:
        #     return Response(status=403, data='Object is locked until ' + str(locked_until))

        if ObjectHelper.can_not_object_be_managed(object_item, request.user):
            return Response(status=403, data='You can manage any object only once in a day')

        if object_item.user == request.user:
            Object.objects.filter(pk=pk).update(timestamp=current_dt)

        serializer = ObjectUserManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, object_id=object_item.pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        context = {'request': request}
        serializer = ObjectSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        location = serializer.validated_data['location']

        objects_in_radius_count = Object.objects.filter(
            location__distance_lt=(location, Distance(m=OBJECT_CAN_CREATE_IN_RADIUS_METERS))).count()

        if objects_in_radius_count > 0:
            return Response(status=403, data='It is forbidden more than 1 object in ' + str(
                OBJECT_CAN_CREATE_IN_RADIUS_METERS) + 'meters radius')

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        queryset = Object.objects.all()
        object_item = get_object_or_404(queryset, pk=pk)
        context = {'request': request}
        serializer = ObjectUpdateSerializer(object_item, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(isActivate=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        queryset = Object.objects.all()
        object_item = get_object_or_404(queryset, pk=pk)

        if not ObjectHelper.can_object_be_captured(object_item, request.user):
            return Response(status=403, data='You can not capture this object yet')

        context = {'request': request}
        serializer = ObjectCaptureSerializer(object_item, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
