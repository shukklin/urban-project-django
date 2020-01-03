import datetime

from api.models import ObjectsUserManage
from api.table.constants.object_constants import OBJECT_CAPTURE_STREAK_COUNT


class ObjectHelper:
    @staticmethod
    def can_object_be_captured(object_item, user):
        return object_item.user != user and (
                OBJECT_CAPTURE_STREAK_COUNT - ObjectsUserManage.objects.filter(timestamp__gt=object_item.timestamp,
                                                                               user=user).count()) == 0
    @staticmethod
    def can_not_object_be_managed(object_item, user):
        current_dt = datetime.datetime.now(datetime.timezone.utc)

        last_manage_records = ObjectsUserManage.objects.order_by('-id').filter(timestamp__gt=object_item.timestamp,
                                                                               user=user)
        return len(last_manage_records) > 0 and current_dt < (last_manage_records[0].timestamp + datetime.timedelta(1))