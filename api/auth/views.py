from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api.table.serializers.models_serializers import UserSerializer, AuthSerializer


class SignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer
