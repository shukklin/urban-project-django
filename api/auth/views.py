from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..serializers import UserSerializer


class SignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
