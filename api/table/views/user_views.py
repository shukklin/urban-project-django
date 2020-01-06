from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import User, ObjectPhoto
from api.table.permissions.IsCreationOrIsAuthenticated import IsCreationOrIsAuthenticated
from api.table.serializers.models_serializers import UserSerializer, ObjectPhotoSerializer, AuthSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsCreationOrIsAuthenticated, )

    def create(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        serializer = UserSerializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def photos(self, request):
        queryset = ObjectPhoto.objects.all()
        photos = get_list_or_404(queryset, user=request.user)
        serializer = ObjectPhotoSerializer(photos, many=True)
        return Response(serializer.data)