from django.urls import path
from .import views

urlpatterns=[
    path('dashboard/',views.dashboard),
    path('getuserprofile/',views.get_user_profile),
    path('updateuserprofile/<int:user_id>',views.update_user_profile),
    path('deleteuserprofile/<int:user_id>',views.delete_user_profile),
    
    path('getdonorform/',views.get_donorform),
    path('getrequestform/',views.get_requestform),
    path('getstockform/',views.get_stockform),
    path('getcontactform/',views.get_contactform),

    path('approve-donation/<int:donor_id>', views.approve_donation_view, name="approve-donation"),
    path('reject-donation/<int:donor_id>', views.reject_donation_view, name="reject-donation"),

    path('approve-request/<int:requests_id>', views.approve_request_view, name="approve-request"),
    path('reject-request/<int:requests_id>', views.reject_status_view, name="reject-request"),

]