from django.db import models


class EObjectType(models.IntegerChoices):
    TREE = 0
    LIGHT = 1
    ADVERTISMENT = 2
    MAILBOX = 3
    BUS_STOP = 4
    SIGN = 5
    BENCH = 6