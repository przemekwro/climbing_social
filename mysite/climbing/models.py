from django.contrib.auth.models import AbstractUser, User
from django.db import models
from enum import Enum

# Create your models here.

class Terrain(models.Model):
    pion = 1
    połóg = 2
    przewieszenie = 3
    zaciecie = 4
    kant = 5


class Grade(models.Model):
    name = models.CharField(max_length=3, null=False, unique=True)


class Location(models.Model):
    city = models.CharField(max_length=20)
    rock = models.CharField(max_length=20)
    is_gym = models.BooleanField(default=False)


class Route(models.Model):
    is_inside = models.BooleanField(default=True)
    grade = models.ForeignKey(Grade, on_delete=models.ProtectedError)
    location = models.ForeignKey(Location, on_delete=models.ProtectedError)
    terrain = models.ForeignKey(Terrain, on_delete=models.ProtectedError)


class History(models.Model):
    route = models.ForeignKey(Route, on_delete=models.ProtectedError)
    belayer = models.ForeignKey(User, on_delete=models.ProtectedError, related_name="belayer")
    climber = models.ForeignKey(User, on_delete=models.ProtectedError, related_name="climber")


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    is_student = models.BooleanField('student status', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField(default=True)
    best_route = models.ForeignKey(Route, on_delete=models.ProtectedError)
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username+" "+self.name+" "+self.lastname;


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.ProtectedError)
    content = models.CharField(max_length = 250)
    route = models.ForeignKey(Route, on_delete=models.ProtectedError)




