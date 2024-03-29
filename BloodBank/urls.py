from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.home),
    path("home",views.home),
    path("donateblood",views.donate),
    path("requestblood",views.addbloodrequest),

    path("bloodbasics",views.bloodbasics),
    path("bloodbankinfo",views.bloodbankinfo), 

    path('event', views.event),
    path("addEventForm",views.addEventForm),
    path("getEventForm", views.getEventForm),
    path('updateEventForm/<int:event_id>', views.updateEventForm),

    path('addTeamForm', views.addTeamForm),
    path('getTeamForm', views.getTeamForm),
    path('updateTeamForm/<int:team_id>', views.updateTeamForm),
    path('deleteTeamForm/<int:team_id>', views.deleteTeamForm),

    path('contactform', views.contact_form),
    path('covid', views.covid),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root= settings.STATIC_URL)