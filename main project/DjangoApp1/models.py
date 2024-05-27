from pyexpat import model
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

class teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Area = models.CharField(max_length=30)

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class asset(models.Model):
    Name = models.CharField(max_length=25, default="some asset")
    Location = models.CharField(max_length=30, default="IT room")
    Subject = models.CharField(max_length=25, default = 'IT')
    Value = models.FloatField(default=1)
    LastUpdated = models.DateTimeField(auto_now=True)
    AssetImage = models.ImageField(upload_to='images/assets', default='/images/defaultImage.jpg')

class assetevent(models.Model):
    Assets = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    UsersInvolved = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    Description = models.CharField(max_length = 100, default = "")
    CreationTime = models.DateTimeField(auto_now_add=True) # auto update when added
    LoanExpiry = models.DateTimeField()