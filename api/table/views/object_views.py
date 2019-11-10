from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from api.models import Object
from api.table.serializers.custom_serializers import LocationSerializer
from api.table.serializers.models_serializers import ObjectSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.response import Response
import math

class ObjectViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        z, lat, lng = float(request.query_params['z']), float(request.query_params['lat']), float(
            request.query_params['lng'])

        if z > 0:
            radius = math.floor(100 / z)
        else:
            return Response(status=400)

        queryset = Object.objects.filter(
            location__distance_lt=(Point(lng, lat), Distance(km=radius)))

        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Object.objects.all()
        object = get_object_or_404(queryset, pk=pk)
        serializer = ObjectSerializer(object)
        return Response(serializer.data)

    def create(self, request):
        serializer = ObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        queryset = Object.objects.all()
        object_item = get_object_or_404(queryset, pk=pk)

        serializer = ObjectSerializer(object_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
