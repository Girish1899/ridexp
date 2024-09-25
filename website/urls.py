# website/urls.py
from django.urls import path
from . import views
from website import views
from website.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('our_rides', views.our_rides, name='our_rides'),
    path('save-enquiry/', save_enquiry, name='save_enquiry'),
    path('bookride', views.bookride, name='bookride'),
    path('contact', AddContact.as_view(), name='contact'),
    path('taxi_services', views.services, name='services'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('airport_taxi', views.airporttaxi, name='airporttaxi'),
    path('outstationcabs', views.outstationcabs, name='outstationcabs'),
    path('localtaxi', views.localtaxi, name='localtaxi'),
    path('blog', views.blog, name='blog'),
    path('packages', views.packages, name='packages'),
    
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('login', views.login_page.as_view(), name='login'),
    path('register_vehicle', views.AddVehicle.as_view(), name='register_vehicle'),
    path('get_owner_details/', get_owner_details, name='get_owner_details'),
    path('check_vehicleno/',check_vehicleno,name='check_vehicleno'),
    path('login_view', views.login_view, name='login_view'),
    # path('cabs_list', views.cabs_list, name='cabs_list'),
    path('search_url', search_url, name='search_url'),
    path('airportcabs_list', views.airportcabs_list, name='airportcabs_list'),
    path('airport_ride_pricing_details', AirportGetRidePricingDetails.as_view(), name='airport_ride_pricing_details'),
    path('airport_roundtrip', views.airport_roundtrip, name='airport_roundtrip'),
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
    path('blog/why_taxis', views.why_taxis, name="why_taxis"),
    path('blog/how_taxis', views.how_taxis, name="how_taxis"),
    path('blog/top_tips', views.top_tips, name="top_tips"),
    path('blog/the_role', views.the_role, name="the_role"),
    path('blog/family_travel', views.family_travel, name="family_travel"),
    path('blog/eco_friendly', views.eco_friendly, name="eco_friendly"),
    path('blog/taxi_improve', views.taxi_improve, name="taxi_improve"),
    path('blog/the_future', views.the_future, name="the_future"),
    path('blog/perfect_choice', views.perfect_choice, name="perfect_choice"),
    path('blog/taxi_companies', views.taxi_companies, name="taxi_companies"),


    # airport blog ##############################################

    path('blog/reliable_rideshares', views.airport1, name="reliable_rideshares"),
    path('blog/airport_needs', views.airport2, name="airport_needs"),
    path('blog/prebooking_airport', views.airport3, name="prebooking_airport"),
    path('blog/airport_etiquette', views.airport4, name="airport_etiquette"),
    path('blog/easily_trust', views.airport5, name="easily_trust"),
    path('blog/flight_tracking', views.airport6, name="flight_tracking"),
    path('blog/airport_pickup', views.airport7, name="airport_pickup"),
    path('blog/airport_advantage', views.airport8, name="airport_advantage"),
    path('blog/ideal_business', views.airport9, name="ideal_business"),
    path('blog/savemoney_onairport', views.airport10, name="savemoney_onairport"),
    path('blog/common_mistakes', views.airport11, name="common_mistakes"),
    path('blog/modern_taxi', views.airport12, name="modern_taxi"),
    path('blog/go_green', views.airport13, name="go_green"),
    path('blog/major_global', views.airport14, name="major_global"),
    path('blog/passenger_safety', views.airport15, name="passenger_safety"),
    path('blog/affordable_transfer', views.airport16, name="affordable_transfer"),
    path('blog/luxury_travelers', views.airport17, name="luxury_travelers"),
    path('blog/avoid_scams', views.airport18, name="avoid_scams"),
    path('blog/booking_idea', views.airport19, name="booking_idea"),
    path('blog/your_needs', views.airport20, name="your_needs"),
    path('blog/handle_delays', views.airport21, name="handle_delays"),
    path('blog/ultimate_guide', views.airport22, name="ultimate_guide"),
    path('blog/ridesharing_apps', views.airport23, name="ridesharing_apps"),
    path('blog/cashless_payments', views.airport24, name="cashless_payments"),
    path('blog/safety_during_pandemic', views.airport25, name="safety_during_pandemic"),

#local_blogs #################################
    path('blog/local_future', views.local_future, name="local_future"),
    path('blog/better_environment', views.better_environment, name="better_environment"),
    path('blog/city_travel', views.city_travel, name="city_travel"),
    path('blog/electric_taxi', views.electric_taxi, name="electric_taxi"),
    path('blog/bestlocalcabs', views.bestlocalcabs, name="bestlocalcabs"),
    path('blog/affordable', views.affordable, name="affordable"),
    path('blog/urban_growth', views.urban_growth, name="urban_growth"),
    path('blog/ride_sharing', views.ride_sharing, name="ride_sharing"),
    path('blog/tech_savy', views.tech_savy, name="tech_savy"),
    path('blog/tourism', views.tourism, name="tourism"),
    path('blog/hybrid', views.hybrid, name="hybrid"),
    path('blog/mega_cities', views.mega_cities, name="mega_cities"),
    path('blog/benefits', views.benefits, name="benefits"),
    path('blog/fleets', views.fleets, name="fleets"),
    path('blog/public_transport', views.public_transport, name="public_transport"),
    path('blog/save_money', views.save_money, name="save_money"),

    path('blog/localcabs_leadingcharge', views.localcabs_leadingcharge, name="localcabs_leadingcharge"),
    path('blog/heroes_of_nighttime_urban_transport', views.urban_transport, name="heroes_of_nighttime_urban_transport"),
    path('blog/taxi_regulations_the_future', views.taxi_regulations_the_future, name="taxi_regulations_the_future"),
    path('blog/reducing_city_emissions', views.reducing_city_emissions, name="reducing_city_emissions"),
    path('blog/localcabs_support_corporate_travel', views.localcabs_support_corporate_travel, name="localcabs_support_corporate_travel"),
    path('blog/green_taxi_initiatives', views.green_taxi_initiatives, name="green_taxi_initiatives"),
    path('blog/sloution_for_miletransport', views.sloution_for_miletransport, name="sloution_for_miletransport"),
    path('blog/driverless_taxis', views.driverless_taxis, name="driverless_taxis"),
    path('blog/localcabs_best_for_airport', views.localcabs_best_for_airport, name="localcabs_best_for_airport"),


    path('packages/banaglore_to_mysore', views.banaglore_to_mysore, name="banaglore_to_mysore"),
    path('packages/banaglore_to_coorg', views.banaglore_to_coorg, name="banaglore_to_coorg"),
    path('packages/banaglore_to_hampi', views.banaglore_to_hampi, name="banaglore_to_hampi"),
    path('packages/banaglore_to_munnar', views.banaglore_to_munnar, name="banaglore_to_munnar"),
    path('packages/banaglore_to_nandi_hills', views.banaglore_to_nandi_hills, name="banaglore_to_nandi_hills"),
    path('packages/banaglore_to_kabini', views.banaglore_to_kabini, name="banaglore_to_kabini"),
    path('packages/banaglore_to_chikmagalur', views.banaglore_to_chikmagalur, name="banaglore_to_chikmagalur"),
    path('packages/banaglore_to_ooty', views.banaglore_to_ooty, name="banaglore_to_ooty"),



    # path('send_otp/', views.send_otp, name='send_otp'),
    # path('verify_otp/', views.verify_otp, name='verify_otp'),
]
