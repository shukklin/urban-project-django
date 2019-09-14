from django.contrib.auth.models import AbstractUser
from urban_app.settings import AUTH_USER_MODEL
from django.contrib.gis.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class ObjectType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'types'

    def __str__(self):
        return "{} - {}".format(self.name)


class Object(models.Model):
    location = models.PointField()
    address = models.CharField(max_length=255)
    timestamp = models.DateField(auto_now=True)
    state = models.IntegerField()
    name = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'items'

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