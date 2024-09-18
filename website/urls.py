# website/urls.py
from django.urls import path
from . import views
from website import views
from website.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('bookride', views.bookride, name='bookride'),
    path('contact', AddContact.as_view(), name='contact'),
    path('contactlist', ContactList.as_view(), name='contactlist'),    
    path('services', views.services, name='services'),
    path('airporttaxi', views.airporttaxi, name='airporttaxi'),
    path('outstationcabs', views.outstationcabs, name='outstationcabs'),
    path('localtaxi', views.localtaxi, name='localtaxi'),
    path('blog', views.blog, name='blog'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('login', views.login_page.as_view(), name='login'),
    path('regvehicle', views.AddVehicle.as_view(), name='regvehicle'),
    path('get_owner_details/', get_owner_details, name='get_owner_details'),
    path('check_vehicleno/',check_vehicleno,name='check_vehicleno'),
    path('login_view', views.login_view, name='login_view'),
    # path('cabs_list', views.cabs_list, name='cabs_list'),
    path('search_url', search_url, name='search_url'),
    path('airportcabs_list', views.airportcabs_list, name='airportcabs_list'),
    path('airport_ride_pricing_details', AirportGetRidePricingDetails.as_view(), name='airport_ride_pricing_details'),
    path('localcabs_list', views.localcabs_list, name='localcabs_list'),
    path('outstation_oneway', views.outstation_oneway, name='outstation_oneway'),
    path('outstation_roundtrip', views.outstation_roundtrip, name='outstation_roundtrip'),
    path('booking_list', booking_list, name='booking_list'),
    path('search_customer_phone_numbers/', search_phone_numbers, name='search_customer_phone_numbers'),
    path('get_customer_details/', get_customer_details, name='get_customer_details'),
    path('add_new_booking', AddNewBooking.as_view(), name='add_new_booking'),
    path('get_ride_pricing_details', GetRidePricingDetails.as_view(), name='get_ride_pricing_details'),
    path('oneway_ride_pricing_details', OnewayRidePricingDetails.as_view(), name='oneway_ride_pricing_details'),
    path('roundtrip_ride_pricing_details', RoundtripRidePricingDetails.as_view(), name='roundtrip_ride_pricing_details'),
    
    path('logout/', views.logout_view, name='logout'),
    path('blog/why_choose_local_cab_services', views.Why_Choose_Local_Cab_Services, name="Why_Choose_Local_Cab_Services"),
    path('blog/top_reasons', views.top_reasons, name="top_reasons"),
    path('blog/tips', views.tips, name="tips"),
    path('blog/benefits', views.benefits, name="benefits"),
    path('blog/how_to_choose', views.how_to_choose, name="how_to_choose"),
    path('blog/essential_qualities', views.essential_qualities, name="essential_qualities"),
    path('blog/save_money', views.save_money, name="save_money"),
    path('blog/exploring_city', views.exploring_city, name="exploring_city"),
    path('blog/luxury_taxi', views.luxury_taxi, name="luxury_taxi"),
    path('blog/the_importance', views.the_importance, name="the_importance"),

    # path('send_otp/', SendOtp.as_view(), name='send_otp'),
    # path('verify_otp/', VerifyOtp.as_view(), name='verify_otp'),
]
