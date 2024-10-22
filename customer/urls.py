from django.urls import path
from customer.views import *

urlpatterns = [

    path('customer_login',custlogin.as_view(),name='customer_login'),
    path('customer_logout', cuslogout_view, name='customer_logout'),
    path('customer_register', regcustomer.as_view(), name='customer_register'),
    path('check_phonenumber',check_phonenumber, name='check_phonenumber'),
    path('', customer_profile, name='customer_profile'),
    path('previous', previous.as_view(), name='previous'),
    path('current', current.as_view(), name='current'),
    path('customer_addbooking', Addbookings.as_view(), name='customer_addbooking'),
    path('customerPricingDetails', customerGetRidePricingDetails.as_view(), name='customerPricingDetails'),
    path('cuscancel_ride', cancel_ride, name='cuscancel_ride'),
    
    path('send_otp_customer/', SendOtp.as_view(), name='send_otp_customer'),
    path('verify_otp_customer/', VerifyOtp.as_view(), name='verify_otp_customer'),

]