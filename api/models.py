from django.contrib.auth.models import AbstractUser
from urban_app.settings import AUTH_USER_MODEL
from django.contrib.gis.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Tree(models.Model):
    location = models.PointField()

    class Meta:
        db_table = "trees"

    def __str__(self):
        return "{} - {}".format(str(self.id), self.location)


class Photo(models.Model):
    url = models.ImageField()
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "photos"

    def __str__(self):
        return str(self.url)


class ScientificName(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'scientific_tree_names'

    def __str__(self):
        return self.name


class CommonName(models.Model):
    name = models.CharField(max_length=40)
    name_ru = models.CharField(max_length=40)
    scientific_name = models.ForeignKey(ScientificName, on_delete=models.CASCADE)

    class Meta:
        db_table = 'common_tree_names'

    def __str__(self):
        return self.name


class SiteType(models.Model):
    name = models.CharField(max_length=20)
    name_ru = models.CharField(max_length=20)

    class Meta:
        db_table = 'site_types'

    def __str__(self):
        return self.name


class Record(models.Model):
    trunk_diameter = models.FloatField(null=True)
    height = models.FloatField(null=True)
    skeletal_branches_number = models.IntegerField(null=True)
    condition = models.CharField(max_length=100, null=True)
    nearest_address = models.CharField(max_length=255, null=True)
    date_input = models.DateField()
    date_planted = models.DateField(null=True)
    date_removed = models.DateField(null=True)
    common_name = models.ForeignKey(CommonName, on_delete=models.CASCADE)
    site_type = models.ForeignKey(SiteType, on_delete=models.SET_NULL, null=True)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'records'

    def __str__(self):
        return "{} - {}".format(str(self.id), self.common_name)
