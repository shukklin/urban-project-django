from django.db import models


class EObjectType(models.IntegerChoices):
    TREE = 0
    LIGHT = 1
    ADVERTISMENT = 3