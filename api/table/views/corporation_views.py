from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.table.serializers.models_serializers import CorporationSerializer
from ...models import Corporation, User


class CorporationViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        context = {'request': request}
        queryset = Corporation.objects.all()
        corporation = get_object_or_404(queryset, pk=pk)
        serializer = CorporationSerializer(corporation, context=context)
        return Response(serializer.data)

    def list(self, request):
        context = {'request': request}
        queryset = Corporation.objects.all()
        corporations = get_list_or_404(queryset)
        serializer = CorporationSerializer(corporations, many=True, context=context)
        return Response(serializer.data)