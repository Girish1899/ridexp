from django.urls import path
from customer.views import *

urlpatterns = [

    path('custlogin',custlogin.as_view(),name='custlogin'),
    path('custlogout', cuslogout_view, name='custlogout'),
    path('regcustomer', regcustomer.as_view(), name='regcustomer'),
    path('check_phonenumber',check_phonenumber, name='check_phonenumber'),
    path('', customer_profile, name='customer_profile'),
    path('previous', previous.as_view(), name='previous'),
    path('current', current.as_view(), name='current'),
    path('cusaddbooking', Addbookings.as_view(), name='cusaddbooking'),
    path('customerGetRidePricingDetails', customerGetRidePricingDetails.as_view(), name='customerGetRidePricingDetails'),
    path('cuscancel_ride', cancel_ride, name='cuscancel_ride'),
    

]