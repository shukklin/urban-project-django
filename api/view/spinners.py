from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.models import SiteType, CommonName, ScientificName
from ..serializers import ScientificNameSerializer, CommonNameSerializer, SiteTypeSerializer


class SiteTypesView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = SiteType.objects.all()
    serializer_class = SiteTypeSerializer


class CommonNamesView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = CommonName.objects.all()
    serializer_class = CommonNameSerializer


class ScientificNamesView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ScientificName.objects.all()
    serializer_class = ScientificNameSerializer
