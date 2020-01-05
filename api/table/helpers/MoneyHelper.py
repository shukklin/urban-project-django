from django.db.models import F

from api.models import User
from api.table.helpers import ObjectHelper
from api.table.helpers.CorporationHelper import CorporationHelper
from api.table.enums.EActivityStatus import EActivityStatus


class EManageType:
    OWN_OBJECT = 2
    FOREIGN_OBJECT = 1
    CORPORATION_OBJECT = 2

class ECaptureType:
    FOREIGN_OBJECT = 1
    EMPTY_OBJECT = 2

class EMissionType:
    ADMIN = 2

class EMoneyType:
    CREATE_OBJECT = 10
    UPDATE_OBJECT = 5
    MANAGE_OBJECT = 1
    CAPTURE_OBJECT = 1
    MISSION = 1

class MoneyHelper:
    @staticmethod
    def add(type, user, obj):
        money =  MoneyHelper.get_money(type, user, obj)

        if money == 0:
            return

        MoneyHelper.set_money(money, user)

    @staticmethod
    def get_money(type, user, obj):
        if type == EMoneyType.CREATE_OBJECT:
            return EMoneyType.CREATE_OBJECT
        elif type == EMoneyType.UPDATE_OBJECT:
            return EMoneyType.UPDATE_OBJECT
        elif type == EMoneyType.MANAGE_OBJECT:
            if obj.user == user:
                return EManageType.OWN_OBJECT
            elif obj.user != user:
                return EManageType.FOREIGN_OBJECT
            if obj.user.corporation:
                return EManageType.CORPORATION_OBJECT
        elif type == EMoneyType.CAPTURE_OBJECT:
            if ObjectHelper.can_object_be_captured(obj, user):
                return ECaptureType.FOREIGN_OBJECT
            elif ObjectHelper.can_object_be_captured(obj, user):
                return ECaptureType.EMPTY_OBJECT
        elif type == EMoneyType.MISSION:
            if user.activity == EActivityStatus.ADMIN:
                return EMissionType.ADMIN
        return 0

    @staticmethod
    def set_money(money, user):
        if user.corporation:
            money = CorporationHelper.charge(money)

        User.objects.filter(pk=user.id).update(money=F('money') + money)