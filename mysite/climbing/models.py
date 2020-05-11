from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings
from enum import Enum

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True,on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    is_student = models.BooleanField('student status', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    best_route = models.ForeignKey(Route, on_delete=models.ProtectedError, null=True)



    def __str__(self):
        return self.username+" "+self.name+" "+self.lastname;

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.ProtectedError)
    content = models.CharField(max_length = 500)
    route = models.ForeignKey(Route, on_delete=models.ProtectedError, null=True)
    added_date = models.DateTimeField(auto_now_add=True, blank=True)
    comment_counter = models.IntegerField(default=0, blank=True)
    like_counter = models.IntegerField(default=0, blank=True)


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.ProtectedError)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    added_date = models.DateTimeField(auto_now_add=True, blank=True)


class Followers(models.Model):
    follow_by = models.ForeignKey(User, on_delete=models.ProtectedError, related_name="follow_by")
    follow_to = models.ForeignKey(User, on_delete=models.ProtectedError, related_name="follow_to")





