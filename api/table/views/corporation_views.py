from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.table.serializers.models_serializers import CorporationSerializer
from ...models import Corporation


class CorporationViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CorporationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Corporation.objects.all()
        corporations = get_list_or_404(queryset)
        serializer = CorporationSerializer(corporations, many=True)
        return Response(serializer.data)