from django.shortcuts import get_list_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from ...models import ObjectPhoto
from api.table.constants.app_constants import MAX_UPLOAD_PHOTOS
from api.table.serializers.models_serializers import ObjectPhotoSerializer


class ObjectPhotoViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = ObjectPhoto.objects.all()
        photos = get_list_or_404(queryset, user=request.user)
        serializer = ObjectPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ObjectPhoto.objects.all()
        photos = get_list_or_404(queryset, pk=pk)
        serializer = ObjectPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def create(self, request):
        list_images = request.FILES.getlist('images[]')

        # If current count photos more than in conf do throw an error
        if len(list_images) > MAX_UPLOAD_PHOTOS:
            return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        if len(list_images) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # prepare data for serializer
        prepared_data = [
            {
                'user': request.user.id,
                'object': self.request.data['object'],
                'url': image
            }
            for image in list_images
        ]

        serializer = ObjectPhotoSerializer(data=prepared_data, many=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)