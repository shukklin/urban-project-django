from django.db.models import F

from api.models import User
from api.table.helpers import ObjectHelper


class EMoneyType:
    CREATE_OBJECT = 10
    UPDATE_OBJECT = 5
    MANAGE_OWN_OBJECT = 2
    MANAGE_FOREIGN_OBJECT = 1
    MANAGE_CORPORATION_OBJECT = 2
    CAPTURE_FOREIGN_OBJECT = 1
    CAPTURE_EMPTY_OBJECT = 2
    EXEC_MISSION_USER = 1
    EXEC_MISSION_ADMIN = 1

class MoneyHelper:
    @staticmethod
    def add_money(type, user, obj):
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
        elif type == EMoneyType.MANAGE_OWN_OBJECT and obj.user == user:
            return EMoneyType.MANAGE_OWN_OBJECT
        elif type == EMoneyType.MANAGE_FOREIGN_OBJECT and obj.user != user:
            return EMoneyType.MANAGE_FOREIGN_OBJECT
        elif type == EMoneyType.MANAGE_CORPORATION_OBJECT and obj.user.corporation:
            return EMoneyType.MANAGE_CORPORATION_OBJECT
        elif type == EMoneyType.CAPTURE_FOREIGN_OBJECT and ObjectHelper.can_object_be_captured(obj, user):
            return EMoneyType.CAPTURE_FOREIGN_OBJECT
        elif type == EMoneyType.CAPTURE_EMPTY_OBJECT and ObjectHelper.can_object_be_captured(obj, user):
            return EMoneyType.CAPTURE_EMPTY_OBJECT
        elif type == EMoneyType.EXEC_MISSION_USER:
            return EMoneyType.EXEC_MISSION_USER
        elif type == EMoneyType.EXEC_MISSION_ADMIN:
            return EMoneyType.EXEC_MISSION_ADMIN
        return 0

    @staticmethod
    def set_money(money, user):
        User.objects.filter(pk=user.id).update(money=F('money') + money)