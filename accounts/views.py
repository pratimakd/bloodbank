from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from .auth import unauthenticated_user
from .models import Profile, User

 
# Create your views here.

@unauthenticated_user
def loginform(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.info(request, "Username or password is invalid")

    context={}       
    return render(request,'accounts/login_form.html', context)

@unauthenticated_user
def adminloginform(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_staff:
                login(request,user)
                return redirect('/home')
            elif user.is_staff:
                login(request, user)
                return redirect('/admins/dashboard')
        else:
            messages.info(request, "Username or password is invalid")

    context={}       
    return render(request,'accounts/admin_login_form.html', context)


@unauthenticated_user
def registerform(request):
    if request.method=="POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,username=user.username)
            messages.add_message(request, messages.SUCCESS, 'You are registered successfully')
            return redirect('/accounts/loginform')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to register')
            return render(request, 'accounts/register_form.html', {'form':form})
            
    context={'form':UserCreationForm}
    return render(request,'accounts/register_form.html', context)

def logoutuser(request):
    logout(request)
    return redirect('/accounts/loginform')

def user_account(request):
    profile = request.user.profile
    form= ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Update Successful for'+ str(request.user.profile))
            return redirect('/accounts/profile')
    context={'form':form}
    return render(request, 'accounts/profile.html',context)

