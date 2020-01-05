import math


class CorporationHelper:
    REFILL_BY_USER_ACTION_PERCENT = 10

    @staticmethod
    def charge(score):
        return math.ceil((score / 100) * CorporationHelper.REFILL_BY_USER_ACTION_PERCENT)