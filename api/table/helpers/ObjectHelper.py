import datetime

from django.contrib.gis.measure import Distance

from api.models import ObjectsUserManage, Object
from api.table.enums.EActivityStatus import EActivityStatus


class ObjectHelper:
    OBJECT_LOCKED_IN_DAYS = 2
    OBJECT_LOST_IN_DAYS = 30
    OBJECT_CAN_CREATE_IN_RADIUS_METERS = 5
    OBJECT_CAPTURE_STREAK_COUNT = 3
    OBJECT_MANAGE_THROTTLING = 1

    @staticmethod
    def is_object_capture_streak_done(object_item, user):
        current_streak_count = ObjectsUserManage.objects.filter(timestamp__gt=object_item.timestamp, object_id__exact=object_item.id,
                                                                               user=user).count()
        return ObjectHelper.OBJECT_CAPTURE_STREAK_COUNT <= current_streak_count

    @staticmethod
    def can_object_be_captured(object_item, user):
        return not ObjectHelper.is_own_object(object_item, user) and (ObjectHelper.is_object_capture_streak_done(object_item, user)
                                                   or not ObjectHelper.is_object_in_property(object_item))

    @staticmethod
    def can_create_object(location):
        return Object.objects.filter(
            location__distance_lt=(location, Distance(m=ObjectHelper.OBJECT_CAN_CREATE_IN_RADIUS_METERS))).count() == 0

    @staticmethod
    def can_be_managed(object_item, user):
        current_dt = datetime.datetime.now(datetime.timezone.utc)
        last_manage_records = ObjectsUserManage.objects.order_by('-id').filter(timestamp__gt=object_item.timestamp,
                                                                               object_id__exact=object_item.id,
                                                                               user=user)
        is_can_manage_by_throttling = len(last_manage_records) == 0 or (len(last_manage_records) > 0 and current_dt > (
                    last_manage_records[0].timestamp + datetime.timedelta(ObjectHelper.OBJECT_MANAGE_THROTTLING)))
        is_object_available = current_dt > (object_item.timestamp + datetime.timedelta(
           ObjectHelper.OBJECT_LOCKED_IN_DAYS))
        is_can_be_captured = ObjectHelper.can_object_be_captured(object_item, user  )

        return is_object_available and is_can_manage_by_throttling and not is_can_be_captured

    @staticmethod
    def is_own_object(object_item, user):
        return object_item.user.id == user.id

    @staticmethod
    def can_be_activated(object_item, user):
        return not object_item.is_activated and user.activity == EActivityStatus.ADMIN

    @staticmethod
    def can_be_deleted(object_item, user):
        return not object_item.is_deleted and user.activity == EActivityStatus.ADMIN

    @staticmethod
    def is_object_in_property(object_item):
        return datetime.datetime.now(datetime.timezone.utc) < (object_item.timestamp + datetime.timedelta(ObjectHelper.OBJECT_LOST_IN_DAYS))