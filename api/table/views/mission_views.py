import datetime

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.table.helpers.ExperienceHelper import ExperienceHelper
from api.table.helpers.MissionHelper import MissionHelper
from api.table.helpers.MoneyHelper import MoneyHelper
from api.table.serializers.models_serializers import MissionSerializer, MissionUserSerializer, MissionListSerializer
from ...models import Mission, MissionUser


class MissionViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        context = {'request': request}
        queryset = Mission.objects.all()
        mission = get_object_or_404(queryset, pk=pk)
        serializer = MissionSerializer(mission, context=context)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def assign(self, request, pk=None):
        is_already_taken = MissionUser.objects.filter(mission_id=pk, user=request.user).count() > 0
        mission = get_object_or_404(Mission.objects.all(), pk=pk)

        if mission.activity != request.user.activity:
            return Response(status=403, data='The mission require the different activity type')

        if is_already_taken:
            return Response(status=403, data='The mission is already taken')

        serializer = MissionUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, mission_id=pk, start_timestamp=datetime.datetime.now(datetime.timezone.utc))

        return Response(status=status.HTTP_200_OK, data='Mission has been assigned')

    @action(detail=True, methods=['POST'])
    def done(self, request, pk=None):
        user_mission = get_object_or_404(MissionUser.objects.filter(mission_id=pk, user=request.user))
        mission = get_object_or_404(Mission.objects.all(), pk=pk)

        if MissionHelper.is_mission_finished(user_mission):
            return Response(status=403, data='The mission is already finished')

        if MissionHelper.is_mission_done(user_mission, mission, request.user):

            current_dt =datetime.datetime.now(datetime.timezone.utc)
            MissionUser.objects.filter(pk=user_mission.id).update(end_timestamp=current_dt)

            MoneyHelper.set_money(mission.money, request.user)
            ExperienceHelper.set_experience(mission.experience, request.user)

            return Response(status=status.HTTP_200_OK, data='Mission has been done')
        else:
            return Response(status=403, data='The mission is not done yet')

    def list(self, request):
        context = {'request': request}
        queryset = Mission.objects.filter(activity=request.user.activity)
        missions = get_list_or_404(queryset)
        serializer = MissionListSerializer(missions, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)