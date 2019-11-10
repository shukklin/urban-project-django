from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models import ObjectType
from api.table.serializers.models_serializers import ObjectTypeSerializer


class ObjectTypeViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ObjectTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = ObjectType.objects.all()
        corporations = get_list_or_404(queryset)
        serializer = ObjectTypeSerializer(corporations, many=True)
        return Response(serializer.data)