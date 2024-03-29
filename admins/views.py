from django.shortcuts import render, HttpResponse, redirect
from BloodBank.models import Donor, Requests, ContactUs
from BloodBank.forms import AskBloodForm, DonorForm
from accounts.models import Profile
from accounts.forms import ProfileForm
from admins.models import Stock
from admins.forms import StockForm
from django.contrib.auth.models import User
from django.contrib import messages
from . import forms, models
from django.db.models import Sum, Q
from django.views import View

from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
# Create your views here.

# def dashboard(request):
#     def __init__(self):
#         self.labels = []
#         self.data = []

#     def piechart(self, labels, data):
#         queryset = Stock.objects.order_by('-unit')
#         for stock in queryset:
#             self.labels.append(stock.bloodgroup)
#             self.data.append(stock.unit)
#         return self.labels, self.data
#     totalunit= models.Stock.objects.aggregate(Sum('unit'))
#     dict={
#         'totaldonors':Donor.objects.all().count(),
#         'totalbloodunit':totalunit['unit__sum'],
#         'totalrequest':Requests.objects.all().count(),
#         'totalapprovedrequest':Requests.objects.all().filter(status='Approved').count(),
#         'labels': self.labels,
#         'data': self.data
#     }
#     return render(request,'admins/dashboard.html',context= dict)


@login_required
@admin_only
def dashboard(request):
    labels_pie = []
    data_pie = []
    queryset = Stock.objects.order_by('-unit')
    for stock in queryset:
        labels_pie.append(stock.bloodgroup)
        data_pie.append(stock.unit)
    totalunit = models.Stock.objects.aggregate(Sum('unit'))

    data_bar = []
    labels_bar = []

    queryset = Requests.objects.values('bloodgroup', 'status').annotate(
        units=Sum('unit')).order_by('-units')
    for entry in queryset:
        if entry['status'] == 'Approved':
            labels_bar.append(entry['bloodgroup'])
            data_bar.append(entry['units'])

    dict = {
        'totaldonors': Donor.objects.all().count(),
        'totalbloodunit': totalunit['unit__sum'],
        'totalrequest': Requests.objects.all().count(),
        'totalapprovedrequest': Requests.objects.all().filter(status='Approved').count(),
        'labels_bar': labels_bar,
        'data_bar': data_bar,
        'labels_pie': labels_pie,
        'data_pie': data_pie,
    }

    return render(request, 'admins/dashboard.html', context=dict)


@login_required
@admin_only
def get_donorform(request):
    donation = Donor.objects.all().order_by('-id')
    context = {
        'donations': donation
    }
    return render(request, 'admins/get_donate_form.html', context)


@login_required
@admin_only
def get_requestform(request):
    req = Requests.objects.all().order_by('-id')
    context = {
        'reqs': req
    }
    return render(request, 'admins/get_requests_form.html', context)


@login_required
@admin_only
def get_contactform(request):
    con = ContactUs.objects.all()
    context = {
        'con': con
    }
    return render(request, 'admins/getcontactform.html', context)


@login_required
@admin_only
def get_stockform(request):
    s = Stock.objects.all()
    context = {
        'stock': s
    }
    return render(request, 'admins/get_stock_form.html', context)


@login_required
@admin_only
def get_user_profile(request):
    userprofile = Profile.objects.all()
    context = {
        'userprofile': userprofile
    }
    return render(request, 'admins/get_user_profile.html', context)


@login_required
@admin_only
def update_user_profile(request, user_id):
    user = Profile.objects.get(id=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/admins/getuserprofile')
    context = {
        'form': ProfileForm(instance=user)
    }
    return render(request, 'admins/update_user_profile.html', context)


@login_required
@admin_only
def delete_user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.add_message(request, messages.SUCCESS, 'User has been deleted')
    return redirect('/admins/getuserprofile')


def approve_donation_view(request, donor_id):
    donation = Donor.objects.get(id=donor_id)
    donation_blood_group = donation.bloodgroup
    donation_blood_unit = donation.unit

    stock, created = Stock.objects.get_or_create(
        bloodgroup=donation_blood_group)
    stock.unit = stock.unit+donation_blood_unit
    stock.save()

    donation.status = 'Approved'
    donation.save()
    return redirect('/admins/getdonorform')


def reject_donation_view(request, donor_id):
    donation = Donor.objects.get(id=donor_id)
    donation.status = 'Rejected'
    donation.save()
    return redirect('/admins/getdonorform')


def approve_request_view(request, requests_id):
    req = Requests.objects.get(id=requests_id)
    bloodgroup = req.bloodgroup
    unit = req.unit
    stock = Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit >= unit:
        stock.unit = stock.unit-unit
        stock.save()
        req.status = "Approved"
        req.save()
        messages.success(request,'Request approved successfully')
    else:
        messages.error(request,'Not enough blood units in stock')
    return redirect('/admins/getrequestform')


def reject_status_view(request, requests_id):
    req = Requests.objects.get(id=requests_id)
    req.status = "Rejected"
    req.save()
    return redirect('/admins/getrequestform')
