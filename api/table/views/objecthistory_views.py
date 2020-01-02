from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from api.models import Object, ObjectHistory
from api.table.serializers.custom_serializers import LocationSerializer
from api.table.serializers.models_serializers import ObjectSerializer, ObjectHistorySerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.response import Response
import math

class ObjectHistoryViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = ObjectHistory.objects.all()
        history = get_list_or_404(queryset, user=request.user)
        serializer = ObjectHistorySerializer(history, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ObjectHistory.objects.all()
        objects = get_object_or_404(queryset, pk=pk)
        serializer = ObjectHistorySerializer(objects)
        return Response(serializer.data)

    def create(self, request):
        serializer = ObjectHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)