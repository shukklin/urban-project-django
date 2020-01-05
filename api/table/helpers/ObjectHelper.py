import datetime

from api.models import ObjectsUserManage
from api.table.constants.object_constants import OBJECT_CAPTURE_STREAK_COUNT, OBJECT_LOST_IN_DAYS


class ObjectHelper:
    @staticmethod
    def is_object_capture_streak_done(object_item, user):
        return OBJECT_CAPTURE_STREAK_COUNT - ObjectsUserManage.objects.filter(timestamp__gt=object_item.timestamp,
                                                                               user=user).count() == 0

    @staticmethod
    def can_object_be_captured(object_item, user):
        return object_item.user != user and (ObjectHelper.is_object_capture_streak_done(object_item, user)
                 or not ObjectHelper.is_in_property(object_item, user))

    @staticmethod
    def can_not_object_be_managed(object_item, user):
        current_dt = datetime.datetime.now(datetime.timezone.utc)

        last_manage_records = ObjectsUserManage.objects.order_by('-id').filter(timestamp__gt=object_item.timestamp,
                                                                               user=user)
        return len(last_manage_records) > 0 and current_dt < (last_manage_records[0].timestamp + datetime.timedelta(1))

    @staticmethod
    def is_in_property(object_item, user):
        return object_item.user == user and datetime.datetime.now(datetime.timezone.utc) < (object_item.timestamp + datetime.timedelta(OBJECT_LOST_IN_DAYS))