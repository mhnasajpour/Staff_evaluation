from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    personnel_code = models.CharField(max_length=10, unique=True, null=True)
    national_code = models.CharField(max_length=10, unique=True, null=True)

    def __str__(self):
        return self.get_full_name()


class Position(models.Model):
    title = models.CharField(max_length=255, null=True)
    unit = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='users')
    manager = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='managers')
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.unit + '-' + self.title
