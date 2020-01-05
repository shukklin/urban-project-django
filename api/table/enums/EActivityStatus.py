from django.db import models


class EActivityStatus(models.IntegerChoices):
    BUSINESS = 0
    ADMIN = 1
