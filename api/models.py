
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from api.table.enums.EnumHelper import get_enum_choices
from urban_app.settings import AUTH_USER_MODEL
from enum import IntEnum


class EActivityStatus(IntEnum):
    BUSINESS = 0
    ADMIN = 1

class EObjectType(IntEnum):
    TREE = 0
    LIGHT = 1
    ADVERTISMENT = 3

class Corporation(models.Model):
    """
    Корпорации
    """
    name = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    class Meta:
        db_table = 'corporations'

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Пользователь
    """
    corporation = models.ForeignKey(Corporation, null=True, on_delete=models.PROTECT)
    experience = models.IntegerField(default=0)
    money = models.IntegerField(default=0)
    avatar = models.ImageField(null=True)
    activity = models.IntegerField(default=EActivityStatus.BUSINESS, choices=get_enum_choices(EActivityStatus))

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Mission(models.Model):
    """
    Миссии
    """
    name = models.TextField(max_length=255)
    activity = models.IntegerField(max_length=10, choices=get_enum_choices(EActivityStatus))
    experience = models.IntegerField()
    money = models.IntegerField()
    description = models.TextField(max_length=255)


class MissionUser(models.Model):
    """
    Так как у миссии могут быть назначены многим пользователям
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    mission = models.ForeignKey(Mission, on_delete=models.PROTECT)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()


class Object(models.Model):
    """
    Городские объекты
    """
    location = models.PointField()
    address = models.CharField(max_length=255)
    state = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    name = models.CharField(max_length=255)
    type = models.IntegerField(max_length=10, choices=get_enum_choices(EObjectType))
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = 'objects'

    def __str__(self):
        return "{} - {}".format(str(self.id), self.name)


class ObjectsUserManage(models.Model):
    """
    Для отслеживания взаимодействий с объектами
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    object = models.ForeignKey(Object, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)

class ObjectPhoto(models.Model):
    """
    Фотографии объектов
    """
    url = models.ImageField()
    object = models.ForeignKey(Object, on_delete=models.PROTECT)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "photos"

    def __str__(self):
        return str(self.url)
