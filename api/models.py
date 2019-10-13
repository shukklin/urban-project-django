from django.contrib.auth.models import AbstractUser
from urban_app.settings import AUTH_USER_MODEL
from django.contrib.gis.db import models


class Corporation(models.Model):
    """
    Корпорации
    """
    name = models.CharField(max_length=255)
    experience = models.IntegerField()
    money = models.IntegerField()

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
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    experience = models.IntegerField()
    money = models.IntegerField()
    photo = models.URLField(null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class SubObjectType(models.Model):
    """
    Подтипы игровых объектов (хвойное, лиственное) и т.д.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sub-object-types'

    def __str__(self):
        return "{}".format(self.name)


class ObjectType(models.Model):
    """
    Типы игровых объектов (дерево, столб) и т.д.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'object-types'

    def __str__(self):
        return "{}".format(self.name)


class Object(models.Model):
    location = models.PointField()
    address = models.CharField(max_length=255)
    timestamp = models.DateField(auto_created=True, auto_now=True)
    state = models.IntegerField()
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)
    sub_type = models.ForeignKey(SubObjectType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'objects'

    def __str__(self):
        return "{} - {}".format(str(self.id), self.name)


class Photo(models.Model):
    url = models.ImageField()
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "photos"

    def __str__(self):
        return str(self.url)