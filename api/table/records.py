from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.table.constants import MAX_UPLOAD_PHOTOS
from api.models import Object, Photo
from api.table.serializers import ObjectSerializer, PhotoSerializer


class TreePhotosView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return get_list_or_404(Photo.objects.all(), tree_id=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        list_images = request.FILES.getlist('url[]')

        # If current count photos more than in conf not accept
        if len(list_images) > MAX_UPLOAD_PHOTOS:
            return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        if len(list_images) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # prepare data for serializer
        prepared_data = [
            {
                'user': request.user.id,
                'tree': self.kwargs['pk'],
                'url': image
            }
            for image in list_images
        ]

        serializer = PhotoSerializer(data=prepared_data, many=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TreeRecordView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecordSerializer

    def get_object(self):
        return get_object_or_404(
            Record.objects.distinct('tree_id'), tree_id=self.kwargs['pk'])


class RecordsView(CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecordSerializer

    def create(self, request, *args, **kwargs):
        serializer_record = RecordSerializer(data=request.data)
        serializer_record.is_valid(raise_exception=True)
        serializer_record.save(user=request.user)
        return Response(serializer_record.data, status=status.HTTP_201_CREATED)


class TreesInRadiusView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ObjectSerializer

    def get_queryset(self):
        z, lat, lng = float(self.kwargs['z']), float(self.kwargs['lat']), float(self.kwargs['lng'])

        if z > 0:
            radius = 1000 / z
        else:
            radius = 1000

        return Object.objects.filter(
            location__distance_lt=(Point(lat, lng), Distance(km=radius)))
