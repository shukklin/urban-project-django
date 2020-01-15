import datetime

from django.contrib.gis.measure import Distance

from api.models import ObjectsUserManage, Object


class ObjectHelper:
    OBJECT_LOCKED_IN_DAYS = 5
    OBJECT_LOST_IN_DAYS = 30
    OBJECT_CAN_CREATE_IN_RADIUS_METERS = 50
    OBJECT_CAPTURE_STREAK_COUNT = 3

    @staticmethod
    def is_object_capture_streak_done(object_item, user):
        return (ObjectHelper.OBJECT_CAPTURE_STREAK_COUNT - ObjectsUserManage.objects.filter(timestamp__gt=object_item.timestamp, object_id__exact=object_item.id,
                                                                               user=user).count()) == 0

    @staticmethod
    def can_object_be_captured(object_item, user):
        return object_item.user.id != user.id and (ObjectHelper.is_object_capture_streak_done(object_item, user)
                                                   or not ObjectHelper.is_object_in_property(object_item))

    @staticmethod
    def can_create_object(location):
        return Object.objects.filter(
            location__distance_lt=(location, Distance(m=ObjectHelper.OBJECT_CAN_CREATE_IN_RADIUS_METERS))).count() == 0

    @staticmethod
    def is_object_locked(locked_until):
        current_dt = datetime.datetime.now(datetime.timezone.utc)
        return  locked_until > current_dt

    @staticmethod
    def is_own_object(object_item, user):
        return object_item.user.id == user.id

    @staticmethod
    def can_not_object_be_managed(object_item, user):
        current_dt = datetime.datetime.now(datetime.timezone.utc)

        last_manage_records = ObjectsUserManage.objects.order_by('-id').filter(timestamp__gt=object_item.timestamp,
                                                                               user=user)
        return len(last_manage_records) > 0 and current_dt < (last_manage_records[0].timestamp + datetime.timedelta(1))

    @staticmethod
    def is_object_in_property(object_item):
        return datetime.datetime.now(datetime.timezone.utc) < (object_item.timestamp + datetime.timedelta(ObjectHelper.OBJECT_LOST_IN_DAYS))