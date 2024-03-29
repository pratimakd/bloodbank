from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']



class LoginForm(UserCreationForm):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)


class AdminLoginForm(UserCreationForm):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields=["username", "firstname", "lastname","email","phone","profile_pic" ]