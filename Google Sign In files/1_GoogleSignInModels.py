from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Area = models.CharField(max_length = 30)

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
