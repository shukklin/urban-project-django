from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from api.table.enums.EActivityStatus import EActivityStatus
from api.table.enums.EObjectType import EObjectType
from urban_app.settings import AUTH_USER_MODEL


class Corporation(models.Model):
    """
    Корпорации
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Пользователь
    """
    corporation = models.ForeignKey(Corporation, null=True, on_delete=models.PROTECT)
    experience = models.IntegerField(default=0, validators=[
            MinValueValidator(0)
        ])
    money = models.IntegerField(default=0, validators=[
            MinValueValidator(0)
        ])
    avatar = models.ImageField(null=True)
    activity = models.IntegerField(default=EActivityStatus.BUSINESS, choices=EActivityStatus.choices)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Mission(models.Model):
    """
    Миссии
    """
    name = models.CharField(max_length=255, unique=True)
    activity = models.IntegerField(choices=EActivityStatus.choices)
    manage_count = models.IntegerField(validators=[
            MinValueValidator(0)
        ])
    experience = models.IntegerField(validators=[
            MinValueValidator(0)
        ])
    money = models.IntegerField(validators=[
            MinValueValidator(0)
        ])
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MissionUser(models.Model):
    """
    Так как у миссии могут быть назначены многим пользователям
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    mission = models.ForeignKey(Mission, on_delete=models.PROTECT)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField(null=True)


class Object(models.Model):
    """
    Городские объекты
    """
    location = models.PointField(unique=True)
    address = models.CharField(max_length=255)
    state = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ])
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=EObjectType.choices)
    timestamp = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_activated = models.BooleanField(default=False)

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

    def __str__(self):
        return str(self.url)
