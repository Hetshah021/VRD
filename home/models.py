
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=False)
    birth_date = models.DateField(null=True, blank=True)
    pass_code = models.CharField(max_length=10, null=True, blank=True)

class CameraDetails(models.Model):
    cameranum = models.IntegerField(primary_key=True, default='00')
    location = models.CharField(null=True, blank=True, max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cameranum)

class VehicleDetails(models.Model):
    cameranum = models.ForeignKey(CameraDetails, null=True, on_delete= models.SET_NULL)
    vehicle_no = models.CharField(null=True, blank=True, max_length=13)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class vehicle_details(models.Model):
    cameranum = models.IntegerField(default='00')
    location = models.CharField(null=True, blank=True, max_length=100)
    vehicle_no = models.CharField(null=True, blank=True, max_length=13)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)