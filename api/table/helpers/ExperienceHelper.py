from django.db.models import F

from api.models import User
from api.table.helpers.CorporationHelper import CorporationHelper
from api.table.helpers.ObjectHelper import ObjectHelper


class EExperienceType:
    CREATE_OBJECT = 10
    UPDATE_OBJECT = 5
    CAPTURE_UPDATE = 10


class ExperienceHelper:
    @staticmethod
    def add(type, user, obj):
        experience = ExperienceHelper.get_experience(type, user, obj)

        if experience == 0:
            return

        ExperienceHelper.set_experience(experience, user)

    @staticmethod
    def get_experience(type, user, obj):
        if type == EExperienceType.CREATE_OBJECT:
            return EExperienceType.CREATE_OBJECT
        elif type == EExperienceType.UPDATE_OBJECT:
            return EExperienceType.UPDATE_OBJECT
        elif type == EExperienceType.CAPTURE_UPDATE:
            if ObjectHelper.can_object_be_captured(obj, user):
                return EExperienceType.CAPTURE_UPDATE
        return 0

    @staticmethod
    def set_experience(experience, user):
        if user.corporation:
            experience = CorporationHelper.charge(experience)

        User.objects.filter(pk=user.id).update(experience=F('experience') + experience)