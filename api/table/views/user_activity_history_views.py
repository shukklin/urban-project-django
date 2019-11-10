from django.shortcuts import get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from ...models import UserActivityHistory
from api.table.serializers.models_serializers import ActivitySerializer, UserActivityHistorySerializer


class UserActivityHistoryViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserActivityHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = UserActivityHistory.objects.all()
        history = get_list_or_404(queryset, user=request.user)
        serializer = UserActivityHistorySerializer(history, many=True)
        return Response(serializer.data)