from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    username=models.CharField(null=True, max_length=200)
    firstname=models.CharField(max_length=200, null=True)
    lastname= models.CharField(max_length=200, null=True)
    email= models.EmailField(unique=True, null=True)
    phone= models.CharField(max_length=10,null=True)
    profile_pic=models.FileField(upload_to='static/uploads',default='static/images/donating3.png')
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username