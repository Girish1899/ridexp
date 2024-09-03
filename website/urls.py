# website/urls.py
from django.urls import path
from . import views
from website import views
from website.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('bookride', views.bookride, name='bookride'),
    path('contact', views.contact, name='contact'),
    
    path('services', views.services, name='services'),
    path('airporttaxi', views.airporttaxi, name='airporttaxi'),
    path('outstationcabs', views.outstationcabs, name='outstationcabs'),
    path('localtaxi', views.localtaxi, name='localtaxi'),
    path('blog', views.blog, name='blog'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('login', views.login_page.as_view(), name='login'),
    path('login_view', views.login_view, name='login_view'),
    # path('cabs_list', views.cabs_list, name='cabs_list'),
    path('search_url', search_url, name='search_url'),
    path('airportcabs_list', views.airportcabs_list, name='airportcabs_list'),
    path('localcabs_list', views.localcabs_list, name='localcabs_list'),
    path('booking_list', booking_list, name='booking_list'),
    path('search_customer_phone_numbers/', search_phone_numbers, name='search_customer_phone_numbers'),
    path('get_customer_details/', get_customer_details, name='get_customer_details'),
    path('add_new_booking', AddNewBooking.as_view(), name='add_new_booking'),
    path('get_ride_pricing_details', GetRidePricingDetails.as_view(), name='get_ride_pricing_details'),
    
    path('logout/', views.logout_view, name='logout'),
    
]
