from django.db import models


class EObjectType(models.IntegerChoices):
    TREE = 0
    LIGHT = 1
    ADVERTISMENT = 3
    MAILBOX = 4
    BUS_STOP = 5
    SIGN = 6
    BENCH = 7