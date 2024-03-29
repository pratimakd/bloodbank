from django.db import models
from .choices import*
from django.core import validators
from accounts.models import Profile
from django.contrib.auth.models import User
# Create your models here.




class Donor(models.Model):
    name = models.CharField(max_length=100, blank=False)
    age = models.CharField(max_length=20)
    phone = models.CharField(max_length=100, blank=False)
    address=models.CharField(max_length=60)
    gender = models.CharField(max_length=20, choices = GENDER_CHOICES)
    bloodgroup=models.CharField(max_length=20, choices = BLOODGROUP_CHOICES)
    unit=models.PositiveIntegerField(blank=False)
    status= models.CharField(max_length=20, default="Pending")
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self): 
        return self.user

    class Meta:
        db_table = "donorinfo"


class Events(models.Model):
    image=models.ImageField(upload_to="static/uploads",blank=False, null=True)
    date=models.CharField(max_length=10, null=True)
    eventname=models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=200, null=True)

class Teams(models.Model):
    image=models.ImageField(upload_to="static/uploads",blank=False, null=True)
    name= models.CharField(max_length = 50, validators=[validators.MinLengthValidator(2)])
    expert=models.CharField(max_length=100, null=True)

class Requests(models.Model):
    name= models.CharField(max_length=100, null=True)
    phone=models.CharField(max_length=20, null=True)
    email=models.EmailField(max_length=100, null=True)
    bloodgroup= models.CharField(max_length=20, choices= BLOODGROUP_CHOICES)
    note=models.CharField(max_length=200, blank=True)
    unit=models.PositiveIntegerField(blank=False, default=1)
    status= models.CharField(max_length=20, default="Pending")

class ContactUs(models.Model):
    name= models.CharField(max_length=100, null=True)
    email=models.EmailField(max_length=100, null=True)
    phone=models.CharField(max_length=20, null=True)
    notes=models.CharField(max_length=200, null=True)
    