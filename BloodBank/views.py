from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import ContactUs, Donor,Teams, Events
from .forms import AskBloodForm, DonorForm, TeamForm, EventForm, ContactUsForm
from BloodBank.filters import EventFilter
from . import forms,models
import os
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
# Create your views here.

def home(request):
    team= Teams.objects.all()
    context={
        'teams':team,
    }
    return render(request,'BloodBank/home.html', context)

def donate(request):
    donation_form = forms.DonorForm()
    if request.method == "POST":
        # print(request.POST)
        donation_form = forms.DonorForm(request.POST, request.FILES)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            user=models.User.objects.get(id=request.user.id)
            blood_donate.user=user
            blood_donate.save()
            messages.success(request,'Donation added successfully')
            return HttpResponseRedirect('/donateblood')
        else:
            messages.error(request,'Unable to add donation')
            return render(request, 'BloodBank/donate_form.html',{'form':donation_form})
        
            
    context = {'form':donation_form}
    return render(request,'BloodBank/donate_form.html',context)



def addbloodrequest(request):
    request_form=forms.AskBloodForm()
    if request.method == "POST":
        request_form = forms.AskBloodForm(request.POST)
        if request_form.is_valid():
            request_form.save()
            messages.success(request,'Request added successfully')
            return HttpResponseRedirect('/requestblood')
        else:
            messages.error(request,'Unable to make request')
            return render(request, 'BloodBank/request_form.html',{'form':request_form})

    context = {'form':request_form}      
    return render ( request, 'BloodBank/request_form.html',context)



def bloodbasics(request):
    return render(request,'BloodBank/bloodbasics.html')

def bloodbankinfo(request):
    return render(request,'BloodBank/bloodbankinfo.html')

    
def event(request):
    event= Events.objects.all()
    event_filter=EventFilter(request.GET, queryset=event)
    event_final= event_filter.qs
    context={
        'events':event_final,
        'event_filter':event_filter
    }
    return render(request,'BloodBank/event.html', context)

@login_required
@admin_only
def addEventForm(request):
    if request.method == "POST":
        form= EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Event added successfully')
            return redirect('/getEventForm')
        else:
            messages.add_message(request, messages.ERROR,'Unable to add event')
            return render(request, 'BloodBank/addEventForm.html',{'form':form})
    context={
        'form':EventForm
    }
    return render(request,'BloodBank/addEventForm.html',context)
@login_required
@admin_only
def getEventForm(request):
    event= Events.objects.all()
    context={
        'events': event
    }
    return render(request, 'BloodBank/getEventForm.html',context)
@login_required
@admin_only
def updateEventForm(request, event_id):
    event= Events.objects.get(id=event_id)
    if request.method =="POST":
        form= EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/getEventForm')
    context={
        'form':EventForm(instance=event),
        'activate_TeamMF':'active'
    }
    return render(request,'BloodBank/updateEventForm.html',context)
#     if request.method=="POST":
#         form=AskBlood(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             message.add_message(request, message.SUCCESS,"Blood requested successfully")
#             return redirect('/bloodrequest')
#         else:
#             message.add_message(request, message.ERROR, "Unable to request blood")
#             return render(request, 'BloodBank/request_form.html')
    
#     context={
#         'form':AskBlood
#     }
#     return render(request,'BloodBank/request_form.html',context)

# def getbloodrequest(request):
#     bloodrequests= AskBlood.objects.all()
#     context={
#         'bloodrequest': bloodrequests
        
#     }
#     return render(request, 'BloodBank/getbloodrequest.html',context)

@login_required
@admin_only
def addTeamForm(request):
    if request.method == "POST":
        form= TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,'Team added successfully')
            return redirect('/getTeamForm')
        else:
            messages.add_message(request, messages.ERROR,'Unable to add service')
            return render(request, 'BloodBank/addTeamMF.html',{'form':form})
    context={
        'form':TeamForm
    }
    return render(request,'BloodBank/addTeamMF.html',context)
@login_required
@admin_only
def getTeamForm(request):
    team= Teams.objects.all()
    context={
        'teams': team
    }
    return render(request, 'BloodBank/getTeamForm.html',context)
@login_required
@admin_only
def updateTeamForm(request, team_id):
    team= Teams.objects.get(id=team_id)
    if request.method =="POST":
        form= TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('/getTeamForm')
    context={
        'form':TeamForm(instance=team),
        'activate_TeamMF':'active'
    }
    return render(request,'BloodBank/updateTeamForm.html',context)
@login_required
@admin_only
def deleteTeamForm(request, team_id):
    team= Teams.objects.get(id=team_id)
    team.delete()
    return redirect('/getTeamForm')

def contact_form(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            subject = "Website Inquiry"
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'notes': form.cleaned_data['notes'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 'aneemes1@gmail.com', ['aneemes1@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent.")
            return redirect("/contactform")
        form = ContactUsForm()
    return render(request, "BloodBank/contactus.html", {
        "contactus": ContactUs.objects.all(), 'form': ContactUsForm})

def covid(request):
    return render(request,'BloodBank/corona.html')

