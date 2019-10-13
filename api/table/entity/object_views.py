from rest_framework import viewsets, generics, status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from api.models import Object
from ..serializers import LocationSerializer, ObjectSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.response import Response


class ObjectListView(ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        z, lat, lng = float(self.kwargs['z']), float(self.kwargs['lat']), float(self.kwargs['lng'])

        if z > 0:
            radius = 1000 / z
        else:
            radius = 1000

        return Object.objects.filter(
            location__distance_lt=(Point(lat, lng), Distance(km=radius)))


class ObjectViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        z, lat, lng = float(request.query_params['z']), float(request.query_params['lat']), float(request.query_params['lng'])

        if z > 0:
            radius = 1000 / z
        else:
            radius = 1000

        queryset = Object.objects.filter(
            location__distance_lt=(Point(lat, lng), Distance(km=radius)))

        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = Object.objects.all()
        object = get_object_or_404(queryset, pk=pk)
        serializer = ObjectSerializer(object)
        return Response(serializer.data)


    def post(self, request):
        serializer = ObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)