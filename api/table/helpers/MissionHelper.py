from api.models import ObjectsUserManage, Object
from api.table.enums.EActivityStatus import EActivityStatus


class MissionHelper:
    @staticmethod
    def get_manage_done_count(user_mission, user):
        if user.activity == EActivityStatus.BUSINESS:
            return ObjectsUserManage.objects.filter(timestamp__gte=user_mission.start_timestamp, user=user).count()
        elif user.activity == EActivityStatus.ADMIN:
            return ObjectsUserManage.objects.filter(timestamp__gte=user_mission.start_timestamp,
                                  user=user, object__is_activated__exact=True).count()
        return None

    @staticmethod
    def is_mission_done(user_mission, mission, user):
        return MissionHelper.get_manage_done_count(user_mission, user) == mission.manage_count

    @staticmethod
    def is_mission_finished(user_mission):
        return user_mission.end_timestamp is not None