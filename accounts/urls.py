from django.urls import path
from . import views

urlpatterns=[
    path("registerform/",views.registerform, name="registerform"),
    path("loginform/",views.loginform, name="loginform"),
    path("adminloginform/",views.adminloginform, name="adminloginform"),
    path('logout/', views.logoutuser),
    path('profile/', views.user_account),

]