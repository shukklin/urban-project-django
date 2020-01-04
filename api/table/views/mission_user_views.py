from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.table.serializers.models_serializers import MissionUserSerializer
from ...models import MissionUser


class MissionUserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = MissionUser.objects.filter(user=request.user, start_timestamp__isnull=False, end_timestamp__isnull=True)
        missions = get_list_or_404(queryset)
        context = {'request': request}
        serializer = MissionUserSerializer(missions, many=True, context=context)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def finished(self, request):
        queryset = MissionUser.objects.filter(user=request.user, start_timestamp__isnull=False, end_timestamp__isnull=False)
        missions = get_list_or_404(queryset)
        context = {'request': request}
        serializer = MissionUserSerializer(missions, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)