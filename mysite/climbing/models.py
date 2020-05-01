from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.

class Grade(models.Model):
    name = models.CharField(max_length=20)


class Location(models.Model):
    city = models.CharField(max_length=20)
    is_gym = models.BooleanField(default=False)



class Route(models.Model):
    is_inside = models.BooleanField(default=True)
    grade = models.ForeignKey(Grade, on_delete=models.ProtectedError)
    location = models.ForeignKey(Location, on_delete=models.ProtectedError)


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField('student status', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    best_route = models.ForeignKey(Route, on_delete=models.ProtectedError)

    def __str__(self):
        return self.username;

