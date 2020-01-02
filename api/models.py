from django.contrib.auth.models import AbstractUser
from urban_app.settings import AUTH_USER_MODEL
from django.contrib.gis.db import models


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


class Activity(models.Model):
    """
    Тип активности
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'activities'

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

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class UserActivityHistory(models.Model):
    """
        Связь многие-ко-многим, так как пользователь при каждом входе может выбирать новую активность и это нужно отслеживать
    """
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'user_activity'

    def __str__(self):
        return "{} - {}".format(self.activity.name, self.user.username)


class ObjectType(models.Model):
    """
    Типы игровых объектов (дерево, столб) и т.д.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'object-types'

    def __str__(self):
        return "{}".format(self.name)


class Mission(models.Model):
    """
    Миссии
    """
    name = models.TextField(max_length=255)
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    experience = models.IntegerField()
    money = models.IntegerField()
    description = models.TextField(max_length=255)


class MissionUser(models.Model):
    """
    Так как у миссии могут быть назначены многим пользователям
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    mission = models.ForeignKey(Mission, on_delete=models.PROTECT)
    isDone = models.BooleanField(default=False)


class Object(models.Model):
    """
    Городские объекты
    """
    location = models.PointField()
    address = models.CharField(max_length=255)
    state = models.IntegerField()
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ObjectType, on_delete=models.PROTECT)

    class Meta:
        db_table = 'objects'

    def __str__(self):
        return "{} - {}".format(str(self.id), self.name)


class ObjectHistory(models.Model):
    """
    История городских объектов городские объекты
    """
    timestamp = models.DateField(auto_created=True, auto_now=True)
    object = models.ForeignKey(Object, on_delete=models.PROTECT)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = 'objectshistory'

    def __str__(self):
        return "{} - {}".format(str(self.id), self.object.name)


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
