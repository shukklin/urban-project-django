from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models import Mission
from api.table.serializers.models_serializers import ActivitySerializer, UserActivityHistorySerializer, \
    MissionSerializer


class MissionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = MissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = Mission.objects.all()
        missions = get_list_or_404(queryset)
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)