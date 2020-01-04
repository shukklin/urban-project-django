from api.models import ObjectsUserManage, Object


class MissionHelper:
    @staticmethod
    def get_admin_manage_done_count(user_mission, user):
        return Object.objects.filter(timestamp__gte=user_mission.start_timestamp,
                                                user=user, is_activated=True).count()

    @staticmethod
    def get_manage_done_count(user_mission, user):
        return ObjectsUserManage.objects.filter(timestamp__gte=user_mission.start_timestamp, user=user).count()

    @staticmethod
    def is_mission_done(user_mission, mission, user):
        return MissionHelper.get_manage_done_count(user_mission, user) == mission.manage_count

    @staticmethod
    def is_admin_mission_done(user_mission, mission, user):
        return MissionHelper.get_admin_manage_done_count(user_mission, user) == mission.manage_count