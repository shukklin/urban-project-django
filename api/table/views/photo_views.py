
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.table.constants import MAX_UPLOAD_PHOTOS
from api.table.serializers.models_serializers import PhotoSerializer


class PhotoViewSet(viewsets.ViewSet):
    def list(self, request):
        pass

    def create(self, request):
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