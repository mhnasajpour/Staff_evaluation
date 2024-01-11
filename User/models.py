from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    national_code = models.CharField(unique=True, max_length=10)
    parent_id = models.ForeignKey('User', null=True, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Group)
