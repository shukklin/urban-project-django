from django.db.models import (
    Count,
)
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Photo, Record, User
from ..serializers import UserRecordSerializer, UserSerializer, UserScoreSerializer, UsersScoresSerializer, \
    PhotoSerializer, RecordSerializer


class UsersTreeView(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UserRecordSerializer

    def get_queryset(self):
        return get_list_or_404(
            Record.objects.values('user__username', 'date_input'), tree_id=self.kwargs['pk'])


class UserPhotosView(ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return get_list_or_404(Photo.objects.all(), user=self.request.user)


class UserTreesView(ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        return get_list_or_404(Record.objects.values(
            'common_name', 'date_input', 'nearest_address').filter(user=self.request.user))


class UserScoresView(ListAPIView):
    """
    Get top 3 favorite tree name and total records made by user
    """
    serializer_class = UserScoreSerializer

    def get_queryset(self):
        return get_list_or_404(Record.objects.filter(user=self.request.user)
                               .values('common_name__name', 'common_name__name_ru')
                               .annotate(total_records=Count('user'))
                               .order_by('-total_records')[:3])


class UsersScoresView(ListAPIView):
    """
    Get top 10 users by records they made
    """
    serializer_class = UsersScoresSerializer

    def get_queryset(self):
        return get_list_or_404(Record.objects
                               .values('user__username')
                               .annotate(total_records=Count('user'))
                               .order_by('-total_records')[:10])


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User.objects.all(), pk=self.request.user.pk)
