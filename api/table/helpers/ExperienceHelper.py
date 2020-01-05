import datetime

from django.db.models import F

from api.models import User
from api.table.constants.object_constants import OBJECT_LOST_IN_DAYS


class EExperienceType:
    CREATE_OBJECT = 10
    UPDATE_OBJECT = 5
    CAPTURE_UPDATE = 10


class ExperienceHelper:
    @staticmethod
    def add_experience(type, user, obj):
        experience = ExperienceHelper.get_experience(type, obj)

        if experience == 0:
            return

        ExperienceHelper.set_experience(experience, user)

    @staticmethod
    def get_experience(type, obj):
        if type == EExperienceType.CREATE_OBJECT:
            return EExperienceType.CREATE_OBJECT
        elif type == EExperienceType.UPDATE_OBJECT:
            return EExperienceType.UPDATE_OBJECT
        elif type == EExperienceType.CAPTURE_UPDATE and obj.timestamp > (obj.timestamp + datetime.timedelta(OBJECT_LOST_IN_DAYS)):
            return EExperienceType.CAPTURE_UPDATE
        return 0

    @staticmethod
    def set_experience(experience, user):
        User.objects.filter(pk=user.id).update(experience=F('experience') + experience)