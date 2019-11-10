from django.shortcuts import get_list_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import SubObjectType
from api.table.serializers.models_serializers import SubObjectTypeSerializer


class SubObjectTypeViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = SubObjectType.objects.all()
        corporations = get_list_or_404(queryset)
        serializer = SubObjectTypeSerializer(corporations, many=True)
        return Response(serializer.data)