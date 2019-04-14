from datetime import date

from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth import get_user_model


class Dog(models.Model):
    '''
    This model represents a dog in the app.
    '''
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, blank=True, default="")
    age = models.IntegerField(null=True, default=None)  # in months
    gender = models.CharField(max_length=1)
    '''
    "m" for male, "f" for female, "u" for unknown
    '''
    size = models.CharField(max_length=255)
    '''
    "s" for small, "m" for medium, "l" for large, "xl" for extra,
    large = "u" for unknown
    '''
    # XC: Add additional data fields to the Models
    # which increase the application’s functionality.
    date_added = models.DateField(default=date.today)
    temperment = models.CharField(max_length=255, blank=True, default="")
    vaccinated = models.BooleanField(default=False)


class UserDog(models.Model):
    '''
    This model represents a link between a user an a dog
    '''
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    dog = models.ForeignKey(Dog, on_delete=models.PROTECT)
    # "l" for liked, "d" for disliked
    status = models.CharField(max_length=1)
    # XC: Add additional data fields to the Models
    # which increase the application’s functionality.
    rating = models.IntegerField(default=5)


class UserPref(models.Model):
    '''
    This model contains the user's preferences
    '''
    user = models.ForeignKey(
        User, related_name='preferences', on_delete=models.PROTECT)
    age = models.CharField(max_length=255, default="")
    '''
    "b" for baby, "y" for young, "a" for adult, # "s" for senior
    '''
    gender = models.CharField(max_length=255, default="")
    '''
    "m" for male, "f" for female
    '''
    size = models.CharField(max_length=255, default="")
    '''
    "s" for small, "m" for medium, "l" for large, "xl" for extralarge
    '''
    temperment = models.CharField(max_length=255, default="")

    '''
    NOTE:
     `age`, `gender`, and `size` can contain multiple, comma-separated values
    '''
