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
    path('cusaddbooking', Addbookings.as_view(), name='cusaddbooking'),
    path('customerGetRidePricingDetails', customerGetRidePricingDetails.as_view(), name='customerGetRidePricingDetails'),
    path('cuscancel_ride', cancel_ride, name='cuscancel_ride'),
    

]