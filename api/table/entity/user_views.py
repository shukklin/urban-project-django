from rest_framework import viewsets
from django.shortcuts import get_object_or_404, get_list_or_404
from api.table.serializers import UserSerializer
from api.models import User
from ..serializers import LocationSerializer, ObjectSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)