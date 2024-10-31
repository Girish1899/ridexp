from decimal import Decimal
import random
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login ,logout
import requests
from django.urls import reverse
from superadmin.models import Blogs, Brand, Category, Color,Enquiry, CommissionType, ContactUs, Customer, Model, PackageCategories, PackageName, PackageOrder, Packages, Pricing, Profile, RideDetails, Ridetype, Transmission, Vehicle,VehicleOwner, VehicleType, WebsitePackages
from datetime import date, datetime, time
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.utils.text import slugify
from django.core.cache import cache

from superadmin.views import adduser
from django.contrib.auth.models import User
from django.core.paginator import Paginator



TIME_SLOTS = [
    (time(0, 0), time(5, 59, 59), '12 am - 6 am'),
    (time(6, 0), time(11, 59, 59), '6 am - 12 pm'),
    (time(12, 0), time(17, 59, 59), '12 pm - 6 pm'),
    (time(18, 0), time(23, 59, 59), '6 pm - 12 am'),
]

def get_current_time_slot():
    """Determine the current time slot based on the current time."""
    now = timezone.now().time()
    print("now",now)
    for start_time, end_time, slot in TIME_SLOTS:
        if start_time <= now <= end_time:
            return slot
    return None

def home(request):
        
    categories = PackageCategories.objects.all()
    packages = Packages.objects.select_related('package_category', 'package_name')
    context = {
        'categories': categories,
        'packages': packages,
    }
    
    return render(request, 'website/main.html',context)

def our_rides(request):
    context = None
    return render(request, 'website/our_rides.html',context)

def packages(request):
    context = None
    return render(request, 'website/taxi.html',context)

class PackageDetailView(View):
    def get(self, request, title):
        package = None
        packages = WebsitePackages.objects.all()
        
        for p in packages:
            if slugify(p.title) == title or p.slug == title:
                package = p
                break

        if package is None:
            return render(request, '404.html')

        if slugify(package.title) != title and package.slug:
            return redirect('packages_detail', title=slugify(package.title))

        related_packages = WebsitePackages.objects.filter(status='active').exclude(slug=package.slug)[:3]

        top_attractions = package.top_attraction.split(',')
        package_highlights = package.package_highlights.split(',')

        return render(request, 'website/packages/Package_detail.html', {
            'package': package,
            'related_packages': related_packages,
            'top_attractions': top_attractions,
            'package_highlights': package_highlights
        })


def sitemap(request):
    context = None
    return render(request, 'sitemap.xml',context)


def banaglore_to_mysore(request):
    context = None
    return render(request, 'website/packages/bangalore_to_mysore.html',context)

def banaglore_to_coorg(request):
    context = None
    return render(request, 'website/packages/bangalore_to_coorg.html',context)

def banaglore_to_hampi(request):
    context = None
    return render(request, 'website/packages/bangalore_to_hampi.html',context)

def banaglore_to_munnar(request):
    context = None
    return render(request, 'website/packages/banaglore_to_munnar.html',context)

def banaglore_to_nandi_hills(request):
    context = None
    return render(request, 'website/packages/banaglore_to_nandi_hills.html',context)

def banaglore_to_kabini(request):
    context = None
    return render(request, 'website/packages/banaglore_to_kabini.html',context)

def banaglore_to_chikmagalur(request):
    context = None
    return render(request, 'website/packages/banaglore_to_chikmagalur.html',context)


def banaglore_to_ooty(request):
    context = None
    return render(request, 'website/packages/banaglore_to_ooty.html',context)

def bangalore_to_melukote(request):
    context = None
    return render(request, 'website/packages/bangalore_to_melukote.html',context)

def bangalore_to_brindavan_gardens(request):
    context = None
    return render(request, 'website/packages/bangalore_to_brindavan_gardens.html',context)

def bangalore_to_agumbe(request):
    context = None
    return render(request, 'website/packages/bangalore_to_agumbe.html',context)

def bangalore_to_sakleshpur(request):
    context = None
    return render(request, 'website/packages/bangalore_to_sakleshpur.html',context)

def bangalore_to_chikhaldara(request):
    context = None
    return render(request, 'website/packages/bangalore_to_chikhaldara.html',context)

def bangalore_to_kodaikanal(request):
    context = None
    return render(request, 'website/packages/bangalore_to_kodaikanal.html',context)

def bangalore_to_shimla(request):
    context = None
    return render(request, 'website/packages/bangalore_to_shimla.html',context)

def bangalore_to_tirupati(request):
    context = None
    return render(request, 'website/packages/bangalore_to_tirupati.html',context)

def bangalore_to_wayanad(request):
    context = None
    return render(request, 'website/packages/bangalore_to_wayanad.html',context)

def bangalore_to_shravanabelagola(request):
    context = None
    return render(request, 'website/packages/bangalore_to_shravanabelagola.html',context)

def bangalore_to_goa(request):
    context = None
    return render(request, 'website/packages/bangalore_to_goa.html',context)

def bangalore_to_darjeeling(request):
    context = None
    return render(request, 'website/packages/bangalore_to_darjeeling.html',context)



def Why_Choose_Local_Cab_Services(request):
    context = None
    return render(request, 'website/blog/1.html',context)


def top_reasons(request):
    context = None
    return render(request, 'website/blog/2.html',context)

def tips(request):
    context = None
    return render(request, 'website/blog/3.html',context)

def benefits(request):
    context = None
    return render(request, 'website/blog/4.html',context)

def how_to_choose(request):
    context = None
    return render(request, 'website/blog/5.html',context)

def essential_qualities(request):
    context = None
    return render(request, 'website/blog/6.html',context)

def save_money(request):
    context = None
    return render(request, 'website/blog/7.html',context)

def exploring_city(request):
    context = None
    return render(request, 'website/blog/8.html',context)

def luxury_taxi(request):
    context = None
    return render(request, 'website/blog/9.html',context)

def the_importance(request):
    context = None
    return render(request, 'website/blog/10.html',context)  

def why_taxis(request):
    context = None
    return render(request, 'website/blog/11.html',context)  

def how_taxis(request):
    context = None
    return render(request, 'website/blog/12.html',context)

def top_tips(request):
    context = None
    return render(request, 'website/blog/13.html',context)

def the_role(request):
    context = None
    return render(request, 'website/blog/14.html',context)

def family_travel(request):
    context = None
    return render(request, 'website/blog/15.html',context)

def eco_friendly(request):
    context = None
    return render(request, 'website/blog/16.html',context)

def taxi_improve(request):
    context = None
    return render(request, 'website/blog/17.html',context)

def the_future(request):
    context = None
    return render(request, 'website/blog/18.html',context)

def perfect_choice(request):
    context = None
    return render(request, 'website/blog/19.html',context)

def taxi_companies(request):
    context = None
    return render(request, 'website/blog/20.html',context)



def airport1(request):
    return render(request, 'website/blog/a1.html') 

def airport2(request):
    return render(request, 'website/blog/a2.html')  

def airport3(request):
    return render(request, 'website/blog/a3.html')  

def airport4(request):
    return render(request, 'website/blog/a4.html')    

def airport5(request):
    return render(request, 'website/blog/a5.html') 

def airport6(request):
    return render(request, 'website/blog/a6.html') 

def airport7(request):
    return render(request, 'website/blog/a7.html') 

def airport8(request):
    return render(request, 'website/blog/a8.html') 

def airport9(request):
    return render(request, 'website/blog/a9.html') 

def airport10(request):
    return render(request, 'website/blog/a10.html') 

def airport11(request):
    return render(request, 'website/blog/a11.html') 

def airport12(request):
    return render(request, 'website/blog/a12.html') 

def airport13(request):
    return render(request, 'website/blog/a13.html') 

def airport14(request):
    return render(request, 'website/blog/a14.html') 

def airport15(request):
    return render(request, 'website/blog/a15.html')

def airport16(request):
    return render(request, 'website/blog/a16.html')  

def airport17(request):
    return render(request, 'website/blog/a17.html')

def airport18(request):
    return render(request, 'website/blog/a18.html')

def airport19(request):
    return render(request, 'website/blog/a19.html')  

def airport20(request):
    return render(request, 'website/blog/a20.html')  

def airport21(request):
    return render(request, 'website/blog/a21.html')

def airport22(request):
    return render(request, 'website/blog/a22.html')  

def airport23(request):
    return render(request, 'website/blog/a23.html')

def airport24(request):
    return render(request, 'website/blog/a24.html') 

def airport25(request):
    return render(request, 'website/blog/a25.html')    


def local_future(request):
    context = None
    return render(request, 'website/blog/local1.html',context)

def better_environment(request):
    context = None
    return render(request, 'website/blog/local2.html',context)

def city_travel(request):
    context = None
    return render(request, 'website/blog/local3.html',context)

def electric_taxi(request):
    context = None
    return render(request, 'website/blog/local4.html',context)

def bestlocalcabs(request):
    context = None
    return render(request, 'website/blog/local5.html',context)

def affordable(request):
    context = None
    return render(request, 'website/blog/local6.html',context)

def urban_growth(request):
    context = None
    return render(request, 'website/blog/local7.html',context)

def ride_sharing(request):
    context = None
    return render(request, 'website/blog/local8.html',context)

def tech_savy(request):
    context = None
    return render(request, 'website/blog/local9.html',context)

def tourism(request):
    context = None
    return render(request, 'website/blog/local10.html',context)

def hybrid(request):
    context = None
    return render(request, 'website/blog/local11.html',context)

def mega_cities(request):
    context = None
    return render(request, 'website/blog/local12.html',context)

def benefits(request):
    context = None
    return render(request, 'website/blog/local13.html',context)

def fleets(request):
    context = None
    return render(request, 'website/blog/local14.html',context)

def public_transport(request):
    context = None
    return render(request, 'website/blog/local15.html',context)

def save_money(request):
    context = None
    return render(request, 'website/blog/local16.html',context)

def localcabs_leadingcharge(request):
    context = None
    return render(request, 'website/blog/local17.html',context)

def urban_transport(request):
    context = None
    return render(request, 'website/blog/local18.html',context)

def taxi_regulations_the_future(request):
    context = None
    return render(request, 'website/blog/local19.html',context)

def reducing_city_emissions(request):
    context = None
    return render(request, 'website/blog/local20.html',context)

def localcabs_support_corporate_travel(request):
    context = None
    return render(request, 'website/blog/local21.html',context)

def green_taxi_initiatives(request):
    context = None
    return render(request, 'website/blog/local22.html',context)

def sloution_for_miletransport(request):
    context = None
    return render(request, 'website/blog/local23.html',context)

def driverless_taxis(request):
    context = None
    return render(request, 'website/blog/local24.html',context)

def localcabs_best_for_airport(request):
    context = None
    return render(request, 'website/blog/local25.html',context)


def guide_to_outstation(request):
    context = None
    return render(request, 'website/blog/out1.html',context)

def reasons_to_choose_oustationcabs(request):
    context = None
    return render(request, 'website/blog/out2.html',context)

def best_oustation_services(request):
    context = None
    return render(request, 'website/blog/out3.html',context)

def essential_tips(request):
    context = None
    return render(request, 'website/blog/out4.html',context)

def cost_structure(request):
    context = None
    return render(request, 'website/blog/out5.html',context)

def planning_outstation_trip(request):
    context = None
    return render(request, 'website/blog/out6.html',context)

def pre_booking_outstation(request):
    context = None
    return render(request, 'website/blog/out7.html',context)

def travelling_with_family(request):
    context = None
    return render(request, 'website/blog/out8.html',context)

def comfortable_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/out9.html',context)

def booking_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/out10.html',context)

def reliable_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/out11.html',context)

def technology_in_outstation(request):
    context = None
    return render(request, 'website/blog/out12.html',context)

def budgeting_for_outstation(request):
    context = None
    return render(request, 'website/blog/out13.html',context)

def cater_to_business(request):
    context = None
    return render(request, 'website/blog/out14.html',context)

def environmental_impact_of_outstation(request):
    context = None
    return render(request, 'website/blog/out15.html',context)

def exploring_cultural_attraction(request):
    context = None
    return render(request, 'website/blog/out16.html',context)

def long_distance_journey(request):
    context = None
    return render(request, 'website/blog/out17.html',context)

def different_outstation_destination(request):
    context = None
    return render(request, 'website/blog/out18.html',context)

def safety_tips_for_outstation(request):
    context = None
    return render(request, 'website/blog/out19.html',context)

def offbeat_locations(request):
    context = None
    return render(request, 'website/blog/out20.html',context)

def family_travel_journeys(request):
    context = None
    return render(request, 'website/blog/out21.html',context)

def maximum_savings(request):
    context = None
    return render(request, 'website/blog/out22.html',context)

def outstation_taxi_fare(request):
    context = None
    return render(request, 'website/blog/out23.html',context)

def outstation_taxi_experience(request):
    context = None
    return render(request, 'website/blog/out24.html',context)  

def navigating_language_barriers(request):
    context = None
    return render(request, 'website/blog/out25.html',context)  

# shankar ####################################################################################

def the_ultimate_guide_to_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/1-title-the-ultimate-guide-to-airport-taxi-services.html', context)

def benefits_of_booking_a_round_trip_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-benefits-of-booking-a-round-trip-outstation-taxi-meta-title.html', context)

def key_advantages_of_prepaid_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-key-advantages-of-prepaid-outstation-taxi-services.html', context)

def key_features_to_look_for_in_a_reliable_outstation_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-key-features-to-look-for-in-a-reliable-outstation-taxi-service.html', context)

def mistakes_to_avoid_when_booking_an_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-mistakes-to-avoid-when-booking-an-outstation-taxi.html', context)

def reasons_why_outstation_taxis_are_safer_than_driving_your_own_car(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-reasons-why-outstation-taxis-are-safer-than-driving-your-own-car.html', context)

def things_to_consider_before_choosing_an_outstation_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-things-to-consider-before-choosing-an-outstation-taxi-service.html', context)

def tips_for_saving_money_on_outstation_taxi_bookings(request):
    context = None
    return render(request, 'website/blog/web_blogs/5-tips-for-saving-money-on-outstation-taxi-bookings.html', context)

def a_comprehensive_guide_to_outstation_taxi_etiquette(request):
    context = None
    return render(request, 'website/blog/web_blogs/a-comprehensive-guide-to-outstation-taxi-etiquette.html', context)

def advantages_of_calling_a_local_taxi_for_business_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/advantages-of-calling-a-local-taxi-for-business-travel.html', context)
# 11
def affordable_outstation_cab_options_near_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/affordable-outstation-cab-options-near-you.html', context)

def a_guide_to_booking_last_minute_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/a-guide-to-booking-last-minute-outstation-taxis.html', context)

def airport_taxi_etiquette_dos_and_donts(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-dos-and-donts.html', context)

def airport_taxi_services_for_business_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-business-travelers.html', context)

def airport_taxi_services_for_families(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-families.html', context)

def airport_taxi_vs_public_transport_a_comparative_analysis(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-vs-public-transport-a-comparative-analysis.html', context)

def benefits_of_carpooling_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-carpooling-with-outstation-taxis.html', context)

def benefits_of_choosing_local_cabs_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-choosing-local-cabs-for-outstation-travel.html', context)

def calling_a_local_cab_vs_booking_online_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/calling-a-local-cab-vs-booking-online-which-is-better.html', context)

def call_vs_book_which_is_better_for_local_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/call-vs-book-which-is-better-for-local-taxi-services.html', context)

# 21
def celebrating_special_occasions_with_our_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/celebrating-special-occasions-with-our-taxi-service.html', context)

def choosing_between_outstation_taxis_and_self_driving_rentals(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-between-outstation-taxis-and-self-driving-rentals.html', context)

def choosing_the_best_routes_for_your_outstation_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-best-routes-for-your-outstation-taxi-ride.html', context)

def comparing_local_cabs_near_you_for_outstation_journeys(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-local-cabs-near-you-for-outstation-journeys.html', context)

def cultural_experiences_accessible_via_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/cultural-experiences-accessible-via-outstation-taxis.html', context)

def customer_stories_memorable_rides_with_us(request):
    context = None
    return render(request, 'website/blog/web_blogs/customer-stories-memorable-rides-with-us.html', context)

def dealing_with_lost_items_in_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/dealing-with-lost-items-in-airport-taxis.html', context)

def eco_friendly_travel_the_rise_of_electric_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/eco-friendly-travel-the-rise-of-electric-outstation-taxis.html', context)

def environmental_considerations_of_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/environmental-considerations-of-taxi-services.html', context)

def essential_apps_for_booking_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/essential-apps-for-booking-outstation-taxis.html', context)

# 31

def essential_packing_tips_for_airport_taxi_users(request):
    context = None
    return render(request, 'website/blog/web_blogs/essential-packing-tips-for-airport-taxi-users.html', context)

def essential_tips_for_calling_a_local_cab_company_in_your_area(request):
    context = None
    return render(request, 'website/blog/web_blogs/essential-tips-for-calling-a-local-cab-company-in-your-area.html', context)

def essential_tips_for_calling_a_local_cab_in_a_new_city(request):
    context = None
    return render(request, 'website/blog/web_blogs/essential-tips-for-calling-a-local-cab-in-a-new-city.html', context)

def essential_tips_for_group_travel_using_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/essential-tips-for-group-travel-using-taxis.html', context)

def exploring_different_types_of_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-different-types-of-outstation-taxis.html', context)

def exploring_eco_friendly_outstation_taxi_options(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-eco-friendly-outstation-taxi-options.html', context)

def exploring_local_attractions_via_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-local-attractions-via-outstation-taxis.html', context)

def exploring_local_cultures_with_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-local-cultures-with-outstation-taxi-services.html', context)

def exploring_local_festivals_getting_there_with_our_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-local-festivals-getting-there-with-our-taxi-service.html', context)

def exploring_regional_cuisines_by_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-regional-cuisines-by-outstation-taxi.html', context)

# 41

def exploring_remote_areas_with_outstation_taxis_what_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-remote-areas-with-outstation-taxis-what-to-know.html', context)

def exploring_scenic_routes_with_our_local_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-scenic-routes-with-our-local-taxi-service.html', context)

def exploring_the_best_apps_for_booking_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-best-apps-for-booking-outstation-taxis.html', context)

def exploring_the_best_tourist_destinations_via_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-best-tourist-destinations-via-outstation-taxis.html', context)

def exploring_the_city_must_visit_places_accessible_by_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-city-must-visit-places-accessible-by-taxi.html', context)

def exploring_the_city_top_destinations_to_visit_by_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-city-top-destinations-to-visit-by-taxi.html', context)

def exploring_the_nightlife_safe_rides_with_our_local_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-nightlife-safe-rides-with-our-local-taxi-service.html', context)

def health_and_safety_protocols_in_outstation_taxi_services_post_covid(request):
    context = None
    return render(request, 'website/blog/web_blogs/health-and-safety-protocols-in-outstation-taxi-services-post-covid.html', context)

def the_environmental_impact_of_outstation_taxis_are_they_sustainable(request):
    context = None
    return render(request, 'website/blog/web_blogs/he-environmental-impact-of-outstation-taxis-are-they-sustainable.html', context)

def how_calling_a_local_cab_can_make_travel_easier(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-calling-a-local-cab-can-make-travel-easier.html', context)

# 51

def how_our_taxi_service_handles_lost_items(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-our-taxi-service-handles-lost-items.html', context)

def how_our_taxi_service_supports_local_events(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-our-taxi-service-supports-local-events.html', context)

def how_outstation_taxi_drivers_are_trained_for_long_distance_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxi-drivers-are-trained-for-long-distance-travel.html', context)

def how_outstation_taxis_are_adapting_to_post_pandemic_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-are-adapting-to-post-pandemic-travel.html', context)

def how_outstation_taxis_are_catering_to_the_needs_of_travelers_with_pets(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-are-catering-to-the-needs-of-travelers-with-pets.html', context)

def how_outstation_taxis_are_revolutionizing_rural_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-are-revolutionizing-rural-travel.html', context)

def how_outstation_taxis_contribute_to_sustainable_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-contribute-to-sustainable-travel.html', context)

def how_outstation_taxis_enhance_accessibility_for_all_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-enhance-accessibility-for-all-travelers.html', context)

def how_outstation_taxis_ensure_safety_on_night_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-ensure-safety-on-night-trips.html', context)

def how_outstation_taxi_services_make_corporate_travel_easier(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxi-services-make-corporate-travel-easier.html', context)

# 61  

def how_outstation_taxis_support_last_minute_travel_plans(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-support-last-minute-travel-plans.html', context)

def how_outstation_taxis_support_solo_female_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-support-solo-female-travelers.html', context)

def how_technology_is_revolutionizing_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-technology-is-revolutionizing-outstation-taxi-services.html', context)

def how_to_avoid_extra_charges_when_booking_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-extra-charges-when-booking-outstation-taxis.html', context)

def how_to_avoid_scams_when_booking_an_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-scams-when-booking-an-outstation-taxi.html', context)

def how_to_avoid_taxi_scams_during_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-taxi-scams-during-outstation-travel.html', context)

def how_to_book_an_outstation_taxi_for_a_multi_city_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-outstation-taxi-for-a-multi-city-trip.html', context)

def how_to_book_an_outstation_taxi_for_large_groups(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-outstation-taxi-for-large-groups.html', context)

def how_to_book_a_taxi_a_step_by_step_guide(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-taxi-a-step-by-step-guide.html', context)

def how_to_book_a_taxi_tips_for_a_hassle_free_experience(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-taxi-tips-for-a-hassle-free-experience.html', context)

# 71 

def how_to_book_outstation_cabs_for_weekend_getaways_near_me(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-outstation-cabs-for-weekend-getaways-near-me.html', context)

def how_to_call_a_local_cab_company_for_quick_and_convenient_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-call-a-local-cab-company-for-quick-and-convenient-service.html', context)

def how_to_call_a_local_cab_for_fast_reliable_transportation(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-call-a-local-cab-for-fast-reliable-transportation.html', context)

def how_to_call_a_local_taxi_quickly_and_easily(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-call-a-local-taxi-quickly-and-easily.html', context)

def how_to_choose_the_best_outstation_taxi_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-best-outstation-taxi-for-your-needs.html', context)

def how_to_choose_the_best_taxi_service_for_your_budget(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-best-taxi-service-for-your-budget.html', context)

def how_to_choose_the_right_airport_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-airport-taxi-service.html', context)

def how_to_choose_the_right_outstation_taxi_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-outstation-taxi-for-your-needs.html', context)

def how_to_choose_the_right_outstation_taxi_for_your_next_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-outstation-taxi-for-your-next-trip.html', context)

def how_to_choose_the_right_taxi_service_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-taxi-service-for-your-needs.html', context)

#81

def how_to_choose_the_right_vehicle_for_your_outstation_taxi_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-vehicle-for-your-outstation-taxi-trip.html', context)

def how_to_ensure_safety_during_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-ensure-safety-during-taxi-rides.html', context)

def how_to_find_reliable_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-reliable-outstation-taxi-services.html', context)

def how_to_find_reliable_outstation_taxi_services_online(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-reliable-outstation-taxi-services-online.html', context)

def how_to_find_the_best_cabs_near_me_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-best-cabs-near-me-for-outstation-travel.html', context)

def how_to_find_the_best_local_cab_company_to_call_in_your_area(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-best-local-cab-company-to-call-in-your-area.html', context)

def how_to_handle_emergencies_during_an_outstation_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-emergencies-during-an-outstation-taxi-ride.html', context)

def how_to_handle_emergencies_during_an_outstation_taxi_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-emergencies-during-an-outstation-taxi-trip.html', context)

def how_to_handle_long_distance_night_travel_by_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-long-distance-night-travel-by-outstation-taxi.html', context)

def how_to_handle_long_layovers_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-long-layovers-with-outstation-taxis.html', context)

# 91 

def how_to_handle_taxi_service_issues(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-taxi-service-issues.html', context)

def how_to_make_group_travel_easy_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-group-travel-easy-with-outstation-taxis.html', context)

def how_to_make_long_taxi_rides_enjoyable_for_kids(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-long-taxi-rides-enjoyable-for-kids.html', context)

def how_to_make_solo_travel_easy_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-solo-travel-easy-with-outstation-taxis.html', context)

def how_to_make_your_outstation_taxi_experience_hassle_free(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-your-outstation-taxi-experience-hassle-free.html', context)

def how_to_manage_long_distance_travel_fatigue_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-manage-long-distance-travel-fatigue-in-outstation-taxis.html', context)

def how_to_maximize_comfort_in_outstation_taxis_for_long_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-maximize-comfort-in-outstation-taxis-for-long-rides.html', context)

def how_to_maximize_comfort_on_long_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-maximize-comfort-on-long-outstation-taxi-rides.html', context)

def how_to_navigate_airport_taxi_pickup_locations(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-navigate-airport-taxi-pickup-locations.html', context)

def how_to_navigate_language_barriers_in_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-navigate-language-barriers-in-taxis.html', context)

# 101

def how_to_navigate_the_booking_process_for_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-navigate-the-booking-process-for-outstation-taxis.html', context)

def how_to_plan_a_multi_city_tour_with_an_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-plan-a-multi-city-tour-with-an-outstation-taxi.html', context)

def how_to_plan_a_scenic_road_trip_with_an_outstation_tax(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-plan-a-scenic-road-trip-with-an-outstation-tax.html', context)

def how_to_quickly_call_a_local_taxi_anytime(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-quickly-call-a-local-taxi-anytime.html', context)

def how_to_save_money_on_airport_taxi_fares(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-airport-taxi-fares.html', context)

def how_to_save_money_on_outstation_taxi_bookings(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-outstation-taxi-bookings.html', context)

def how_to_save_money_on_outstation_taxi_fares(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-outstation-taxi-fares.html', context)

def how_to_save_money_on_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-outstation-taxi-rides.html', context)

def how_to_save_time_by_pre_booking_an_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-time-by-pre-booking-an-outstation-taxi.html', context)

def how_to_stay_comfortable_during_long_outstation_taxi_journeys(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-stay-comfortable-during-long-outstation-taxi-journeys.html', context)

# 111

def how_to_stay_safe_in_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-stay-safe-in-airport-taxi.html', context)

def how_to_stay_safe_while_using_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-stay-safe-while-using-taxi-services.html', context)

def how_to_track_your_outstation_taxi_in_real_time(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-track-your-outstation-taxi-in-real-time.html', context)

def how_to_travel_sustainably_with_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-travel-sustainably-with-outstation-taxi-services.html', context)

def how_weather_conditions_impact_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-weather-conditions-impact-outstation-taxi-rides.html', context)

def tips_for_a_comfortable_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-a-comfortable-taxi-ride.html', context)

def local_taxi_services_a_convenient_solution_for_airport_transfers(request):
    context = None
    return render(request, 'website/blog/web_blogs/local-taxi-services-a-convenient-solution-for-airport-transfers.html', context)

def luxury_outstation_taxi_services_when_to_opt_for_premium_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/luxury-outstation-taxi-services-when-to-opt-for-premium-rides.html', context)

def luxury_outstation_taxi_services_worth_the_price(request):
    context = None
    return render(request, 'website/blog/web_blogs/luxury-outstation-taxi-services-worth-the-price.html', context)

def making_the_most_of_outstation_taxi_services_for_group_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/making-the-most-of-outstation-taxi-services-for-group-travel.html', context)

#121

def maximizing_comfort_during_long_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/maximizing-comfort-during-long-outstation-taxi-rides.html', context)

def meet_our_drivers_the_heart_of_our_local_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/meet-our-drivers-the-heart-of-our-local-taxi-service.html', context)

def navigating_airport_taxi_regulations(request):
    context = None
    return render(request, 'website/blog/web_blogs/navigating-airport-taxi-regulations.html', context)

def navigating_cross_country_travel_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/navigating-cross-country-travel-with-outstation-taxis.html', context)

def navigating_different_taxi_services_around_the_world(request):
    context = None
    return render(request, 'website/blog/web_blogs/navigating-different-taxi-services-around-the-world.html', context)

def navigating_taxi_scams_at_airports(request):
    context = None
    return render(request, 'website/blog/web_blogs/navigating-taxi-scams-at-airports.html', context)

def outstation_taxi_etiquette_what_passengers_should_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-etiquette-what-passengers-should-know.html', context)

def outstation_taxi_pooling_an_eco_friendly_and_affordable_option(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-pooling-an-eco-friendly-and-affordable-option.html', context)

def outstation_taxis_a_guide_to_choosing_the_right_vehicle_for_your_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxis-a-guide-to-choosing-the-right-vehicle-for-your-trip.html', context)

def outstation_taxi_services_a_comparison_of_popular_providers(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-a-comparison-of-popular-providers.html', context)

#131

def outstation_taxi_services_a_guide_for_solo_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-a-guide-for-solo-travelers.html', context)

def outstation_taxi_services_for_business_travel_best_practices(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-for-business-travel-best-practices.html', context)

def outstation_taxi_services_for_weekend_getaways_what_you_need_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-for-weekend-getaways-what-you-need-to-know.html', context)

def outstation_taxi_services_vs_self_drive_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-vs-self-drive-which-is-better.html', context)

def outstation_taxis_for_festival_travel_how_to_plan_your_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxis-for-festival-travel-how-to-plan-your-ride.html', context)

def outstation_taxis_vs_public_transport_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxis-vs-public-transport-which-is-better.html', context)

def outstation_taxi_travel_for_business_productivity_on_the_go(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-travel-for-business-productivity-on-the-go.html', context)

def outstation_taxi_travel_for_solo_women_safety_tips_and_best_practices(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-travel-for-solo-women-safety-tips-and-best-practices.html', context)

def outstation_taxi_travel_understanding_fare_estimations(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-travel-understanding-fare-estimations.html', context)

def outstation_taxi_vs_car_rental_which_is_better_for_your_next_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-vs-car-rental-which-is-better-for-your-next-trip.html', context)

#141

def outstation_taxi_vs_public_transport_whats_the_best_choice(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-vs-public-transport-whats-the-best-choice.html', context)

def planning_a_multi_destination_outstation_trip_tips_and_tricks(request):
    context = None
    return render(request, 'website/blog/web_blogs/planning-a-multi-destination-outstation-trip-tips-and-tricks.html', context)

def planning_a_scenic_road_trip_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/planning-a-scenic-road-trip-with-outstation-taxis.html', context)

def planning_for_special_needs_in_outstation_taxi_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/planning-for-special-needs-in-outstation-taxi-travel.html', context)

def preparing_for_taxi_rides_in_foreign_countries(request):
    context = None
    return render(request, 'website/blog/web_blogs/preparing-for-taxi-rides-in-foreign-countries.html', context)

def rideshare_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/rideshare-which-is-better.html', context)

def safety_first_how_our_taxi_service_prioritizes_passenger_well_being(request):
    context = None
    return render(request, 'website/blog/web_blogs/safety-first-how-our-taxi-service-prioritizes-passenger-well-being.html', context)

def safety_first_how_we_ensure_your_protection(request):
    context = None
    return render(request, 'website/blog/web_blogs/safety-first-how-we-ensure-your-protection.html', context)

def safety_measures_to_follow_while_traveling_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/safety-measures-to-follow-while-traveling-in-outstation-taxis.html', context)

def seasonal_demand_and_how_it_affects_outstation_taxi_pricing(request):
    context = None
    return render(request, 'website/blog/web_blogs/seasonal-demand-and-how-it-affects-outstation-taxi-pricing.html', context)

#151

def the_advantages_of_hiring_an_outstation_taxi_for_family_vacations(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-advantages-of-hiring-an-outstation-taxi-for-family-vacations.html', context)

def the_advantages_of_using_our_local_taxi_service_for_daily_commutes(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-advantages-of-using-our-local-taxi-service-for-daily-commutes.html', context)

def the_benefits_of_booking_an_outstation_taxi_in_advance(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-booking-an-outstation-taxi-in-advance.html', context)

def the_benefits_of_pre_booking_your_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-pre-booking-your-airport-taxi.html', context)

def the_benefits_of_pre_booking_your_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-pre-booking-your-taxi.html', context)

def the_benefits_of_using_airport_shuttle_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-using-airport-shuttle-services.html', context)

def the_benefits_of_using_local_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-using-local-taxis.html', context)

def the_benefits_of_using_outstation_taxis_for_family_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-benefits-of-using-outstation-taxis-for-family-travel.html', context)

def the_best_apps_for_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-best-apps-for-airport-taxi-services.html', context)

def the_best_apps_for_booking_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-best-apps-for-booking-outstation-taxis.html', context)

#161

def the_best_times_of_year_to_book_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-best-times-of-year-to-book-outstation-taxis.html', context)

def the_best_time_to_book_an_outstation_taxi_for_festivals(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-best-time-to-book-an-outstation-taxi-for-festivals.html', context)

def the_best_travel_accessories_for_outstation_taxi_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-best-travel-accessories-for-outstation-taxi-trips.html', context)

def the_economic_impact_of_choosing_local_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-economic-impact-of-choosing-local-taxi-services.html', context)

def the_economic_impact_of_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-economic-impact-of-taxi-services.html', context)

def the_environmental_impact_of_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-environmental-impact-of-airport-taxis.html', context)

def the_environmental_impact_of_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-environmental-impact-of-outstation-taxi-services.html', context)

def the_environmental_impact_of_using_local_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-environmental-impact-of-using-local-taxis.html', context)

def the_evolution_of_airports(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-evolution-of-airports.html', context)

def the_evolution_of_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-evolution-of-airport-taxi-services.html', context)


#171

def the_evolution_of_outstation_taxi_services_from_local_cabs_to_app_based_platforms(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-evolution-of-outstation-taxi-services-from-local-cabs-to-app-based-platforms.html', context)

def the_evolution_of_outstation_taxi_services_then_vs_now(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-evolution-of-outstation-taxi-services-then-vs-now.html', context)

def the_future_of_airport_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-future-of-airport-taxi-service.html', context)

def the_future_of_outstation_taxi_services_trends_to_watch(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-future-of-outstation-taxi-services-trends-to-watch.html', context)

def the_future_of_taxi_services_in_a_changing_world(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-future-of-taxi-services-in-a-changing-world.html', context)

def the_future_of_taxi_services_trends_to_watch(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-future-of-taxi-services-trends-to-watch.html', context)

def the_impact_of_covid_19_on_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-impact-of-covid-19-on-outstation-taxi-services.html', context)

def the_impact_of_ride_sharing_on_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-impact-of-ride-sharing-on-outstation-taxi-services.html', context)

def the_impact_of_ride_sharing_on_traditional_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-impact-of-ride-sharing-on-traditional-taxi-services.html', context)

def the_impact_of_traffic_on_outstation_taxi_travel_how_to_plan(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-impact-of-traffic-on-outstation-taxi-travel-how-to-plan.html', context)

# 181

def the_importance_of_booking_an_outstation_taxi_in_advance(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-importance-of-booking-an-outstation-taxi-in-advance.html', context)

def the_importance_of_customer_service_in_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-importance-of-customer-service-in-taxi-services.html', context)

def the_importance_of_local_knowledge_in_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-importance-of-local-knowledge-in-taxi-services.html', context)

def the_importance_of_travel_insurance_for_outstation_taxi_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-importance-of-travel-insurance-for-outstation-taxi-trips.html', context)

def the_pros_and_cons_of_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-pros-and-cons-of-airport-taxi-services.html', context)

def the_pros_and_cons_of_shared_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-pros-and-cons-of-shared-airport-taxis.html', context)

def the_role_of_gps_in_enhancing_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-gps-in-enhancing-outstation-taxi-services.html', context)

def the_role_of_gps_in_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-gps-in-outstation-taxi-services.html', context)

def the_role_of_gps_in_outstation_taxi_services_enhancing_safety_and_convenience(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-gps-in-outstation-taxi-services-enhancing-safety-and-convenience.html', context)

#191

def the_role_of_outstation_taxis_in_promoting_local_tourism(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-outstation-taxis-in-promoting-local-tourism.html', context)

def the_role_of_outstation_taxis_in_sustainable_tourism(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-outstation-taxis-in-sustainable-tourism.html', context)

def the_role_of_taxis_in_sustainable_urban_transportation(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-taxis-in-sustainable-urban-transportation.html', context)

def the_role_of_technology_in_modern_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-technology-in-modern-outstation-taxi-services.html', context)

def the_role_of_technology_in_modern_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-technology-in-modern-taxi-services.html', context)

def the_top_5_benefits_of_using_a_local_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-top-5-benefits-of-using-a-local-taxi.html', context)

def the_ultimate_guide_to_taxi_etiquette(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-ultimate-guide-to-taxi-etiquette.html', context)

def tips_for_calling_a_local_taxi_when_you_need_a_quick_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-calling-a-local-taxi-when-you-need-a-quick-ride.html', context)

def tips_for_first_time_travelers_using_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-first-time-travelers-using-outstation-taxis.html', context)

def tips_for_navigating_airport_taxi_fares(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-navigating-airport-taxi-fares.html', context)

#201

def tips_for_navigating_large_airports(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-navigating-large-airports.html', context)

def tips_for_smooth_communication_with_outstation_taxi_drivers(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-smooth-communication-with-outstation-taxi-drivers.html', context)

def tips_for_solo_travelers_using_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-solo-travelers-using-airport-taxis.html', context)

def tips_for_traveling_during_peak_seasons_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-traveling-during-peak-seasons-with-outstation-taxis.html', context)

def tips_for_traveling_with_children_in_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-traveling-with-children-in-taxis.html', context)

def tips_for_traveling_with_pets_in_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-traveling-with-pets-in-airport-taxis.html', context)

def tips_for_traveling_with_pets_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-traveling-with-pets-in-outstation-taxis.html', context)

def tips_for_using_taxis_during_peak_hours(request):
    context = None
    return render(request, 'website/blog/web_blogs/tips-for-using-taxis-during-peak-hours.html', context)

def top_5_destinations_perfect_for_an_outstation_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-5-destinations-perfect-for-an-outstation-taxi-ride.html', context)

def top_5_road_trip_destinations_perfect_for_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-5-road-trip-destinations-perfect-for-outstation-taxi-rides.html', context)

#211

def top_10_busiest_airports_in_the_world(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-10-busiest-airports-in-the-world.html', context)

def top_airport_taxi_apps_to_use_in_2024(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-airport-taxi-apps-to-use-in-2024.html', context)

def top_benefits_of_booking_an_outstation_taxi_online(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-benefits-of-booking-an-outstation-taxi-online.html', context)

def top_eco_friendly_outstation_taxi_services_to_consider(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-eco-friendly-outstation-taxi-services-to-consider.html', context)

def top_reasons_to_call_a_local_cab_for_your_next_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-reasons-to-call-a-local-cab-for-your-next-ride.html', context)

def top_safety_tips_for_long_distance_taxi_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-safety-tips-for-long-distance-taxi-travel.html', context)

def top_tourist_destinations_to_visit_by_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/top-tourist-destinations-to-visit-by-outstation-taxi.html', context)

def traveling_with_pets_heres_what_you_need_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/traveling-with-pets-heres-what-you-need-to-know.html', context)

def understanding_airport_taxi_fares_a_comprehensive_breakdown(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-airport-taxi-fares-a-comprehensive-breakdown.html', context)

def understanding_airport_taxi_insurance(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-airport-taxi-insurance.html', context)

#221

def understanding_outstation_taxi_cancellation_policies(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-outstation-taxi-cancellation-policies.html', context)

def understanding_outstation_taxi_insurance_what_you_need_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-outstation-taxi-insurance-what-you-need-to-know.html', context)

def understanding_taxi_fares_what_you_need_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-taxi-fares-what-you-need-to-know.html', context)

def understanding_taxi_meter_rates(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-taxi-meter-rates.html', context)

def understanding_taxi_regulations_what_you_should_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-taxi-regulations-what-you-should-know.html', context)

def understanding_taxi_service_ratings(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-taxi-service-ratings.html', context)

def understanding_the_different_pricing_models_for_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-the-different-pricing-models-for-outstation-taxis.html', context)

def understanding_the_pricing_models_of_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-the-pricing-models-of-outstation-taxis.html', context)

def understanding_the_safety_features_of_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/understanding-the-safety-features-of-outstation-taxis.html', context)

def unique_local_attractions_accessible_by_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/unique-local-attractions-accessible-by-taxi.html', context)

#231

def what_is_the_best_time_to_book_an_outstation_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/what-is-the-best-time-to-book-an-outstation-taxi.html', context)

def what_to_do_if_your_outstation_taxi_breaks_down(request):
    context = None
    return render(request, 'website/blog/web_blogs/what-to-do-if-your-outstation-taxi-breaks-down.html', context)

def what_to_expect_from_luxury_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/what-to-expect-from-luxury-outstation-taxi-services.html', context)

def what_to_look_for_in_a_reliable_outstation_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/what-to-look-for-in-a-reliable-outstation-taxi-service.html', context)

def what_you_need_to_know_about_interstate_travel_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/what-you-need-to-know-about-interstate-travel-with-outstation-taxis.html', context)

def why_calling_a_local_cab_company_is_the_best_choice_for_airport_transfers(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-calling-a-local-cab-company-is-the-best-choice-for-airport-transfers.html', context)

def why_calling_a_local_taxi_is_more_convenient_than_ride_hailing_apps(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-calling-a-local-taxi-is-more-convenient-than-ride-hailing-apps.html', context)

def why_calling_a_local_taxi_is_often_better_than_using_ride_share_apps(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-calling-a-local-taxi-is-often-better-than-using-ride-share-apps.html', context)

def why_choose_our_local_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-choose-our-local-taxi-service.html', context)

def why_local_taxis_are_perfect_for_nightlife_adventures(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-local-taxis-are-perfect-for-nightlife-adventures.html', context)

#241

def why_our_local_taxi_service_stands_out(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-our-local-taxi-service-stands-out.html', context)

def why_our_taxi_service_is_ideal_for_business_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-our-taxi-service-is-ideal-for-business-travel.html', context)

def why_outstation_taxis_are_ideal_for_family_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-ideal-for-family-trips.html', context)

def why_outstation_taxis_are_ideal_for_weekend_getaways(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-ideal-for-weekend-getaways.html', context)

def why_outstation_taxis_are_perfect_for_airport_transfers(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-perfect-for-airport-transfers.html', context)

def why_outstation_taxis_are_safer_than_self_driving(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-safer-than-self-driving.html', context)

def why_outstation_taxis_are_the_best_for_weekend_getaways(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-the-best-for-weekend-getaways.html', context)

def why_outstation_taxis_are_the_best_option_for_family_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-the-best-option-for-family-travel.html', context)

def why_outstation_taxis_are_the_best_option_for_group_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-the-best-option-for-group-travel.html', context)

def why_outstation_taxis_are_the_best_option_for_long_distance_travel_safe_reliable_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-outstation-taxis-are-the-best-option-for-long-distance-travel-safe-reliable-service.html', context)

#251 -56

def why_transparent_pricing_is_important_for_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-transparent-pricing-is-important-for-outstation-taxi-services.html', context)

def why_you_should_call_a_local_cab_company_instead_of_using_ride_share_apps(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-you-should-call-a-local-cab-company-instead-of-using-ride-share-apps.html', context)

def why_you_should_choose_local_for_your_next_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-you-should-choose-local-for-your-next-taxi-ride.html', context)

def why_you_should_choose_outstation_taxis_for_business_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-you-should-choose-outstation-taxis-for-business-travel.html', context)

def why_you_should_opt_for_round_trip_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/why-you-should-opt-for-round-trip-outstation-taxi-services.html', context)

def your_reliable_local_taxi_service_quick_rides_friendly_drivers(request):
    context = None
    return render(request, 'website/blog/web_blogs/your-reliable-local-taxi-service-quick-rides-friendly-drivers.html', context)



#### hareesh 
def airport_taxi_driver_training_what_it_involves(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-driver-training-what-it-involves.html',context)

def airport_taxi_etiquette_for_first_time_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-for-first-time-travelers.html',context)

def airport_taxi_etiquette_tips_for_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-tips-for-travelers.html',context)

def airport_taxi_etiquette_tips_for_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-tips-for-travelers.html', context)

def airport_taxi_safety_what_you_should_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-what-you-should-know.html', context)

def airport_taxi_safety_tips_for_women_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-tips-for-women-travelers.html', context)

def airport_taxi_safety_measures_for_solo_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-measures-for-solo-travelers.html', context)

def airport_taxi_safety_features_you_should_look_for(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-features-you-should-look-for.html', context)

def airport_taxi_etiquette_what_you_need_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-what-you-need-to-know.html', context)

def airport_taxi_services_for_ski_resorts_and_mountain_destinations(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-ski-resorts-and-mountain-destinations.html', context)

def airport_taxi_services_for_red_eye_flights(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-red-eye-flights.html', context)

def airport_taxi_services_for_music_festivals_and_major_events(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-music-festivals-and-major-events.html', context)

def airport_taxi_services_for_last_minute_flight_changes(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-last-minute-flight-changes.html', context)

def airport_taxi_services_for_frequent_flyers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-frequent-flyers.html', context)

def airport_taxi_services_for_elderly_passengers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-elderly-passengers.html', context)

def airport_taxi_services_for_early_morning_and_late_night_flights(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-early-morning-and-late-night-flights.html', context)

def airport_taxi_services_for_disabled_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-disabled-travelers.html', context)

def airport_taxi_services_for_city_layovers_exploring_your_options(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-city-layovers-exploring-your-options.html', context)

def airport_taxi_services_for_business_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-business-travelers.html', context)

def airport_taxi_services_a_sustainable_future(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-a-sustainable-future.html', context)

def benefits_of_pre_booking_your_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-pre-booking-your-airport-taxi.html', context)

def benefits_of_pre_booking_an_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-pre-booking-an-airport-taxi.html', context)

def benefits_of_hiring_a_car_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-hiring-a-car-for-outstation-travel.html', context)

def benefits_of_choosing_car_rentals_for_outstation_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-choosing-car-rentals-for-outstation-trips.html', context)

def benefits_of_booking_a_car_for_outstation_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-booking-a-car-for-outstation-trips.html', context)

def benefits_of_booking_a_car_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-booking-a-car-for-outstation-travel.html', context)

def airport_taxis_for_last_minute_travel_plans(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxis-for-last-minute-travel-plans.html', context)

def airport_taxi_vs_shuttle_service_which_is_right_for_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-vs-shuttle-service-which-is-right-for-you.html', context)

def airport_taxi_vs_public_transport_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-vs-public-transport-which-is-better.html', context)

def airport_taxi_tips_for_first_time_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-tips-for-first-time-travelers.html', context)

def airport_taxi_services_with_real_time_tracking(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-with-real-time-tracking.html', context)

def airport_taxi_services_with_language_assistance(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-with-language-assistance.html', context)

def airport_taxi_services_vs_hotel_shuttles(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-vs-hotel-shuttles.html', context)

def airport_taxi_services_vs_car_rentals_which_is_better(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-vs-car-rentals-which-is-better.html', context)

def airport_taxi_services_for_wheelchair_users(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-wheelchair-users.html', context)

def airport_taxi_services_for_vips_and_celebrities(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-vips-and-celebrities.html', context)

def airport_taxi_services_for_travelers_with_disabilities(request):
    context = None
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-travelers-with-disabilities.html', context)

def choosing_the_right_outstation_taxi_for_group_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-right-outstation-taxi-for-group-travel.html', context)

def choosing_the_right_car_service_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-right-car-service-for-outstation-travel.html', context)

def choosing_the_right_car_for_your_outstation_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-right-car-for-your-outstation-trip.html', context)

def choosing_the_right_car_cab_service_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-right-car-cab-service-for-your-needs.html', context)

def choosing_the_best_vehicle_for_long_outstation_taxi_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-best-vehicle-for-long-outstation-taxi-trips.html', context)

def choosing_the_best_airport_taxi_service_for_families(request):
    context = None
    return render(request, 'website/blog/web_blogs/choosing-the-best-airport-taxi-service-for-families.html', context)

def budgeting_for_your_outstation_taxi_travel_tips_and_tricks(request):
    context = None
    return render(request, 'website/blog/web_blogs/budgeting-for-your-outstation-taxi-travel-tips-and-tricks.html', context)

def booking_an_airport_taxi_for_business_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/booking-an-airport-taxi-for-business-travelers.html', context)

def booking_airport_taxis_in_high_traffic_tourist_destinations(request):
    context = None
    return render(request, 'website/blog/web_blogs/booking-airport-taxis-in-high-traffic-tourist-destinations.html', context)

def booking_airport_taxis_during_peak_holiday_seasons(request):
    context = None
    return render(request, 'website/blog/web_blogs/booking-airport-taxis-during-peak-holiday-seasons.html', context)

def best_tips_for_reducing_outstation_call_taxi_tariffs(request):
    context = None
    return render(request, 'website/blog/web_blogs/best-tips-for-reducing-outstation-call-taxi-tariffs.html', context)

def best_practices_for_airport_taxi_service_providers(request):
    context = None
    return render(request, 'website/blog/web_blogs/best-practices-for-airport-taxi-service-providers.html', context)

def best_cars_for_long_distance_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/best-cars-for-long-distance-outstation-travel.html', context)

def best_airport_taxi_services_for_pet_owners(request):
    context = None
    return render(request, 'website/blog/web_blogs/best-airport-taxi-services-for-pet-owners.html', context)

def best_airport_taxi_services_for_group_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/best-airport-taxi-services-for-group-travel.html', context)

def benefits_of_using_airport_taxi_services_for_international_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-using-airport-taxi-services-for-international-travelers.html', context)

def benefits_of_using_a_professional_car_cab_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-using-a-professional-car-cab-service.html', context)

def benefits_of_renting_a_car_for_outstation_trips_near_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-renting-a-car-for-outstation-trips-near-you.html', context)

def benefits_of_renting_a_car_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/benefits-of-renting-a-car-for-outstation-travel.html', context)

def cultural_etiquette_when_traveling_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/cultural-etiquette-when-traveling-with-outstation-taxis.html', context)

def comparing_the_cost_of_airport_taxis_vs_ride_sharing_apps(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-the-cost-of-airport-taxis-vs-ride-sharing-apps.html', context)

def comparing_outstation_taxi_services_what_to_look_for(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-outstation-taxi-services-what-to-look-for.html', context)

def comparing_outstation_car_booking_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-outstation-car-booking-services.html', context)

def comparing_local_vs_national_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-local-vs-national-airport-taxi-services.html', context)

def comparing_local_car_cab_services_for_your_travel_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-local-car-cab-services-for-your-travel-needs.html', context)

def comparing_airport_taxi_services_local_vs_ride_sharing_apps(request):
    context = None
    return render(request, 'website/blog/web_blogs/comparing-airport-taxi-services-local-vs-ride-sharing-apps.html', context)

def common_mistakes_to_avoid_when_renting_cars_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/common-mistakes-to-avoid-when-renting-cars-for-outstation-travel.html', context)

def common_mistakes_to_avoid_when_booking_outstation_cars(request):
    context = None
    return render(request, 'website/blog/web_blogs/common-mistakes-to-avoid-when-booking-outstation-cars.html', context)

def common_airport_taxi_myths_debunked(request):
    context = None
    return render(request, 'website/blog/web_blogs/common-airport-taxi-myths-debunked.html', context)

def exploring_the_most_popular_taxi_routes_in_your_city(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-most-popular-taxi-routes-in-your-city.html', context)

def exploring_the_different_types_of_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-the-different-types-of-airport-taxi-services.html', context)

def exploring_offbeat_destinations_with_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-offbeat-destinations-with-outstation-taxis.html', context)

def exploring_local_cuisine_with_outstation_taxis_foodies_guide(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-local-cuisine-with-outstation-taxis-foodies-guide.html', context)

def exploring_local_attractions_with_outstation_taxis_a_complete_guide(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-local-attractions-with-outstation-taxis-a-complete-guide.html', context)

def exploring_hidden_gems_outstation_taxi_trips_beyond_the_tourist_trail(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-hidden-gems-outstation-taxi-trips-beyond-the-tourist-trail.html', context)

def exploring_car_bazar_options_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/exploring-car-bazar-options-for-outstation-travel.html', context)

def electric_airport_taxis_the_future_of_sustainable_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/electric-airport-taxis-the-future-of-sustainable-travel.html', context)

def eco_friendly_taxi_services_going_green_on_the_road(request):
    context = None
    return render(request, 'website/blog/web_blogs/eco-friendly-taxi-services-going-green-on-the-road.html', context)

def eco_friendly_outstation_taxi_services_travel_sustainably(request):
    context = None
    return render(request, 'website/blog/web_blogs/eco-friendly-outstation-taxi-services-travel-sustainably.html', context)

def eco_friendly_airport_taxi_services_on_the_rise(request):
    context = None
    return render(request, 'website/blog/web_blogs/eco-friendly-airport-taxi-services-on-the-rise.html', context)

def eco_friendly_airport_taxi_options_for_green_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/eco-friendly-airport-taxi-options-for-green-travelers.html', context)

def green_airport_taxis_eco_friendly_transportation_options(request):
    context = None
    return render(request, 'website/blog/web_blogs/green-airport-taxis-eco-friendly-transportation-options.html', context)

def finding_the_best_outstation_car_booking_services_near_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/finding-the-best-outstation-car-booking-services-near-you.html', context)

def finding_the_best_car_rental_for_outstation_trips_near_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/finding-the-best-car-rental-for-outstation-trips-near-you.html', context)

def financing_your_outstation_car_purchase_from_car_bazar(request):
    context = None
    return render(request, 'website/blog/web_blogs/financing-your-outstation-car-purchase-from-car-bazar.html', context)

def family_friendly_features_of_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/family-friendly-features-of-outstation-taxi-services.html', context)

def the_impact_of_ride_hailing_apps_on_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-impact-of-ride-hailing-apps-on-airport-taxi-services.html', context)

def the_role_of_customer_reviews_in_choosing_an_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/the-role-of-customer-reviews-in-choosing-an-airport-taxi.html', context)

def how_airport_taxi_drivers_can_improve_customer_experience(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxi-drivers-can-improve-customer-experience.html', context)

def how_airport_taxi_drivers_handle_special_requests(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxi-drivers-handle-special-requests.html', context)

def how_airport_taxi_drivers_navigate_traffic_efficiently(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxi-drivers-navigate-traffic-efficiently.html', context)

def how_airport_taxi_services_are_evolving_with_technology(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxi-services-are-evolving-with-technology.html', context)

def how_airport_taxi_services_ensure_punctuality(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxi-services-ensure-punctuality.html', context)

def how_airport_taxis_are_adapting_to_pandemic_protocols(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-are-adapting-to-pandemic-protocols.html', context)

def how_airport_taxis_can_help_with_heavy_luggage(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-can-help-with-heavy-luggage.html', context)

def how_airport_taxis_can_improve_accessibility_for_all_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-can-improve-accessibility-for-all-travelers.html', context)

def how_airport_taxis_support_local_economies(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-support-local-economies.html', context)

def how_airport_taxis_provide_special_assistance_for_disabled_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-provide-special-assistance-for-disabled-travelers.html', context)

def how_airport_taxis_handle_international_flight_arrivals(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-airport-taxis-handle-international-flight-arrivals.html', context)

def how_outstation_taxis_are_supporting_local_economies(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-are-supporting-local-economies.html', context)

def how_outstation_taxis_promote_eco_friendly_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-outstation-taxis-promote-eco-friendly-travel.html', context)

def how_taxi_services_are_adapting_to_technology(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-taxi-services-are-adapting-to-technology.html', context)

def how_taxi_services_can_support_local_businesses(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-taxi-services-can-support-local-businesses.html', context)

def how_to_avoid_airport_taxi_scams(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-airport-taxi-scams.html', context)

def how_to_avoid_common_airport_taxi_scams(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-common-airport-taxi-scams.html', context)

def how_to_avoid_extra_charges_with_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-extra-charges-with-airport-taxi-services.html', context)

def how_to_avoid_hidden_charges_in_outstation_taxi_bookings(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-hidden-charges-in-outstation-taxi-bookings.html', context)

def how_to_avoid_long_wait_times_for_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-long-wait-times-for-airport-taxis.html', context)

def how_to_avoid_overpacking_for_outstation_taxi_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-overpacking-for-outstation-taxi-trips.html', context)

# 31/hareesh

def how_to_avoid_scams_when_using_airport_taxis_abroad(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-scams-when-using-airport-taxis-abroad.html', context)

def how_to_avoid_overpaying_for_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-overpaying-for-airport-taxis.html', context)

def how_to_avoid_taxi_scams_at_airports(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-taxi-scams-at-airports.html', context)

def how_to_avoid_traffic_hotspots_when_using_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-avoid-traffic-hotspots-when-using-outstation-taxis.html', context)

def how_to_book_a_car_cab_service_online(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-car-cab-service-online.html', context)

def how_to_book_a_car_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-car-for-outstation-travel.html', context)

def how_to_book_a_last_minute_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-last-minute-airport-taxi.html', context)

def how_to_book_an_airport_taxi_for_long_distance_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-airport-taxi-for-long-distance-rides.html', context)

def how_to_book_an_airport_taxi_for_private_events_and_special_occasions(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-airport-taxi-for-private-events-and-special-occasions.html', context)

def how_to_book_an_airport_taxi_for_vip_passengers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-airport-taxi-for-vip-passengers.html', context)

def how_to_book_an_airport_taxi_when_traveling_abroad(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-airport-taxi-when-traveling-abroad.html', context)


def how_to_book_an_outstation_car_near_you(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-outstation-car-near-you.html', context)

def how_to_book_an_outstation_taxi_for_a_multi_city_tour(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-an-outstation-taxi-for-a-multi-city-tour.html', context)

def how_to_book_a_taxi_for_cross_border_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-a-taxi-for-cross-border-outstation-travel.html', context)

def how_to_book_outstation_taxis_for_large_groups(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-outstation-taxis-for-large-groups.html', context)

def how_to_book_outstation_taxis_for_remote_destinations(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-book-outstation-taxis-for-remote-destinations.html', context)

def how_to_calculate_airport_taxi_fares_in_advance(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-calculate-airport-taxi-fares-in-advanc.html', context)

def how_to_choose_an_airport_taxi_for_large_groups(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-an-airport-taxi-for-large-groups.html', context)

def how_to_choose_a_reputable_airport_taxi_company(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-a-reputable-airport-taxi-company.html', context)

def how_to_choose_the_best_car_hire_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-best-car-hire-for-outstation-travel.html', context)

def how_to_choose_the_best_time_for_an_outstation_taxi_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-best-time-for-an-outstation-taxi-trip.html', context)

def how_to_choose_the_right_airport_taxi_service(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-airport-taxi-service.html', context)

def how_to_choose_the_right_outstation_taxi_service_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-outstation-taxi-service-for-your-needs.html', context)

def how_to_choose_the_right_taxi_service_for_your_needs(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-choose-the-right-taxi-service-for-your-needs.html', context)

def how_to_ensure_a_comfortable_ride_in_an_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-ensure-a-comfortable-ride-in-an-airport-taxi.html', context)

def how_to_ensure_privacy_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-ensure-privacy-in-outstation-taxis.html', context)

def how_to_find_budget_friendly_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-budget-friendly-airport-taxi-services.html', context)

def how_to_find_female_driven_outstation_taxis_for_solo_women_travelers(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-female-driven-outstation-taxis-for-solo-women-travelers.html', context)

def how_to_find_last_minute_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-last-minute-outstation-taxi-services.html', context)

def how_to_find_licensed_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-licensed-airport-taxi-services.html', context)

def how_to_find_reliable_airport_taxi_services_for_family_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-reliable-airport-taxi-services-for-family-travel.html', context)

def how_to_find_the_best_car_outstation_rental_deals(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-best-car-outstation-rental-deals.html', context)

def how_to_find_the_best_deals_on_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-best-deals-on-airport-taxi-services.html', context)

def how_to_find_the_best_deals_on_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-best-deals-on-outstation-taxis.html', context)

def how_to_find_the_nearest_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-find-the-nearest-airport-taxi-services.html', context)

def how_to_handle_emergencies_during_outstation_taxi_rides(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-emergencies-during-outstation-taxi-rides.html', context)

def how_to_handle_flight_delays_when_using_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-flight-delays-when-using-airport-taxis.html', context)

def how_to_handle_language_barriers_when_booking_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-language-barriers-when-booking-outstation-taxis.html', context)

def how_to_handle_long_rides_in_outstation_taxis_staying_comfortable(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-long-rides-in-outstation-taxis-staying-comfortable.html', context)

def how_to_handle_lost_items_in_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-lost-items-in-airport-taxis.html', context)

def how_to_handle_unexpected_flight_delays_with_your_airport_taxi(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-handle-unexpected-flight-delays-with-your-airport-taxi.html', context)

def how_to_make_a_complaint_about_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-a-complaint-about-airport-taxi-services.html', context)

def how_to_make_the_most_of_your_outstation_taxi_journey(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-make-the-most-of-your-outstation-taxi-journey.html', context)

def how_to_plan_an_outstation_taxi_trip_for_business_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-plan-an-outstation-taxi-trip-for-business-travel.html', context)

def how_to_prepare_for_a_long_taxi_ride(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-prepare-for-a-long-taxi-ride.html', context)

def how_to_prepare_for_an_outstation_trip_with_a_rental_car_near_me(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-prepare-for-an-outstation-trip-with-a-rental-car-near-me.html', context)

def how_to_prepare_for_long_distance_outstation_taxi_trips(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-prepare-for-long-distance-outstation-taxi-trips.html', context)


def how_to_prepare_your_car_for_an_outstation_trip(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-prepare-your-car-for-an-outstation-trip.html', context)

def how_to_prepare_your_car_for_outstation_trips_from_car_bazar(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-prepare-your-car-for-outstation-trips-from-car-bazar.html', context)

def how_to_rate_and_review_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-rate-and-review-airport-taxi-services.html', context)

def how_to_request_special_assistance_from_airport_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-request-special-assistance-from-airport-taxi-services.html', context)

def how_to_save_money_on_airport_taxi_fares(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-airport-taxi-fares.html', context)

def how_to_save_money_on_airport_taxi_services_during_peak_times(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-save-money-on-airport-taxi-services-during-peak-times.html', context)

def how_to_secure_the_best_deals_on_outstation_car_bookings(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-secure-the-best-deals-on-outstation-car-bookings.html', context)

def how_to_spot_a_reliable_taxi_service_for_outstation_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-spot-a-reliable-taxi-service-for-outstation-travel.html', context)

def how_to_spot_unlicensed_airport_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-spot-unlicensed-airport-taxis.html', context)

def how_to_stay_productive_while_traveling_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-stay-productive-while-traveling-in-outstation-taxis-meta-title.html', context)

def how_to_stay_safe_during_rainy_season_outstation_taxi_travel(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-stay-safe-during-rainy-season-outstation-taxi-travel.html', context)

def how_to_travel_with_pets_in_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-travel-with-pets-in-outstation-taxis.html', context)

def how_to_use_technology_to_enhance_your_airport_taxi_experience(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-to-use-technology-to-enhance-your-airport-taxi-experience.html', context)

def how_weather_impacts_airport_taxi_availability(request):
    context = None
    return render(request, 'website/blog/web_blogs/how-weather-impacts-airport-taxi-availability.html', context)

def local_car_booking_services_for_your_next_outstation_journey(request):
    context = None
    return render(request, 'website/blog/web_blogs/local-car-booking-services-for-your-next-outstation-journey.html', context)

def luxury_airport_taxi_services_worth_the_extra_cost(request):
    context = None
    return render(request, 'website/blog/web_blogs/luxury-airport-taxi-services-worth-the-extra-cost.html', context)

def luxury_outstation_taxis_traveling_in_style(request):
    context = None
    return render(request, 'website/blog/web_blogs/luxury-outstation-taxis-traveling-in-style.html', context)

def navigating_language_barriers_in_outstation_taxi_services(request):
    context = None
    return render(request, 'website/blog/web_blogs/navigating-language-barriers-in-outstation-taxi-services.html', context)

def outstation_taxi_etiquette_tips_for_passengers(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-etiquette-tips-for-passengers.html', context)

def outstation_taxis_and_accessibility_services_for_everyone(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxis-and-accessibility-services-for-everyone.html', context)

def outstation_taxi_services_during_natural_disasters_what_to_know(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-during-natural-disasters-what-to-know.html', context)

def outstation_taxi_services_for_road_trippers_how_to_plan_your_route(request):
    context = None
    return render(request, 'website/blog/web_blogs/outstation-taxi-services-for-road-trippers-how-to-plan-your-route.html', context)

def planning_a_day_trip_let_us_handle_the_transportation(request):
    context = None
    return render(request, 'website/blog/web_blogs/planning-a-day-trip-let-us-handle-the-transportation.html', context)

def planning_a_road_trip_why_you_should_consider_outstation_taxis(request):
    context = None
    return render(request, 'website/blog/web_blogs/planning-a-road-trip-why-you-should-consider-outstation-taxis.html', context)

def popular_outstation_destinations_accessible_by_car(request):
    return render(request, 'website/blog/web_blogs/popular-outstation-destinations-accessible-by-car-near-me.html')

def safety_tips_for_late_night_airport_taxi_rides(request):
    return render(request, 'website/blog/web_blogs/safety-tips-for-late-night-airport-taxi-rides.html')

def safety_tips_for_night_travel_in_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/safety-tips-for-night-travel-in-outstation-taxis.html')

def safety_tips_for_riding_in_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/safety-tips-for-riding-in-outstation-taxis.html')

def shared_airport_taxis_are_they_worth_it(request):
    return render(request, 'website/blog/web_blogs/shared-airport-taxis-are-they-worth-it.html')

def sustainable_practices_in_the_airport_taxi_industry(request):
    return render(request, 'website/blog/web_blogs/sustainable-practices-in-the-airport-taxi-industry.html')

def advantages_of_airport_taxi_pre_payment_options(request):
    return render(request, 'website/blog/web_blogs/the-advantages-of-airport-taxi-pre-payment-options.html')

def advantages_of_flat_rate_airport_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-advantages-of-flat-rate-airport-taxi-services.html')

def advantages_of_pre_booking_your_outstation_taxi(request):
    return render(request, 'website/blog/web_blogs/the-advantages-of-pre-booking-your-outstation-taxi.html')

def benefits_of_airport_taxis_with_child_car_seats(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-airport-taxis-with-child-car-seats.html')

def benefits_of_booking_a_taxi_in_advance(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-booking-a-taxi-in-advance.html')

def benefits_of_buying_a_car_from_car_bazar_for_outstation_trips(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-buying-a-car-from-car-bazar-for-outstation-trips.html')

def benefits_of_hiring_a_car_service_for_outstation_trips(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-hiring-a-car-service-for-outstation-trips.html')

def benefits_of_round_trip_outstation_taxi_packages(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-round-trip-outstation-taxi-packages.html')

def benefits_of_using_an_airport_taxi_over_ride_sharing_services(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-using-an-airport-taxi-over-ride-sharing-services.html')

def benefits_of_using_outstation_taxis_over_personal_vehicles(request):
    return render(request, 'website/blog/web_blogs/the-benefits-of-using-outstation-taxis-over-personal-vehicles.html')

def best_airport_taxi_apps_for_2024(request):
    return render(request, 'website/blog/web_blogs/the-best-airport-taxi-apps-for-2024.html')

def best_airport_taxi_services_for_long_distance_rides(request):
    return render(request, 'website/blog/web_blogs/the-best-airport-taxi-services-for-long-distance-rides.html')

def best_apps_for_booking_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/the-best-apps-for-booking-outstation-taxis-a-comprehensive-guide.html')

def best_payment_methods_for_airport_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-best-payment-methods-for-airport-taxi-services.html')

def best_times_to_book_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/the-best-times-to-book-outstation-taxis-a-seasonal-guide.html')

def best_time_to_book_an_airport_taxi_for_your_flight(request):
    return render(request, 'website/blog/web_blogs/the-best-time-to-book-an-airport-taxi-for-your-flight.html')

def best_ways_to_find_an_airport_taxi_quickly(request):
    return render(request, 'website/blog/web_blogs/the-best-ways-to-find-an-airport-taxi-quickly.html')

def complete_guide_to_car_outstation_rentals(request):
    return render(request, 'website/blog/web_blogs/the-complete-guide-to-car-outstation-rentals.html')

def convenience_of_247_airport_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-convenience-of-247-airport-taxi-services.html')

def convenience_of_cashless_payments_in_taxis(request):
    return render(request, 'website/blog/web_blogs/the-convenience-of-cashless-payments-in-taxis.html')

def cost_of_airport_taxi_services_around_the_world(request):
    return render(request, 'website/blog/web_blogs/the-cost-of-airport-taxi-services-around-the-world.html')

def environmental_impact_of_airport_taxis(request):
    return render(request, 'website/blog/web_blogs/the-environmental-impact-of-airport-taxis.html')

def environmental_impact_of_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-environmental-impact-of-outstation-taxi-services.html')

def evolution_of_airport_taxi_services_over_the_decades(request):
    return render(request, 'website/blog/web_blogs/the-evolution-of-airport-taxi-services-over-the-decades.html')

def future_of_airport_taxi_services_what_to_expect(request):
    return render(request, 'website/blog/web_blogs/the-future-of-airport-taxi-services-what-to-expect.html')

def future_of_car_cab_services_trends_to_watch(request):
    return render(request, 'website/blog/web_blogs/the-future-of-car-cab-services-trends-to-watch.html')

def future_of_car_services_for_outstation_travel(request):
    return render(request, 'website/blog/web_blogs/the-future-of-car-services-for-outstation-travel.html')

def future_of_outstation_car_rentals_trends_to_watch(request):
    return render(request, 'website/blog/web_blogs/the-future-of-outstation-car-rentals-trends-to-watch.html')

def future_of_outstation_taxi_services_trends_to_watch(request):
    return render(request, 'website/blog/web_blogs/the-future-of-outstation-taxi-services-trends-to-watch.html')

def future_of_taxi_services_trends_to_watch(request):
    return render(request, 'website/blog/web_blogs/the-future-of-taxi-services-trends-to-watch.html')

def impact_of_airport_expansion_on_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-impact-of-airport-expansion-on-taxi-services.html')

def importance_of_customer_feedback_in_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-importance-of-customer-feedback-in-outstation-taxi-services.html')

def importance_of_insurance_in_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-importance-of-insurance-in-outstation-taxi-services.html')

def importance_of_punctuality_in_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-importance-of-punctuality-in-taxi-services.html')

def pros_and_cons_of_using_airport_taxis_vs_rideshares(request):
    return render(request, 'website/blog/web_blogs/the-pros-and-cons-of-using-airport-taxis-vs-rideshares.html')

def role_of_airport_taxi_dispatch_systems(request):
    return render(request, 'website/blog/web_blogs/the-role-of-airport-taxi-dispatch-systems.html')

def role_of_gps_technology_in_modern_airport_taxis(request):
    return render(request, 'website/blog/web_blogs/the-role-of-gps-technology-in-modern-airport-taxis.html')

def role_of_taxi_services_in_emergency_situations(request):
    return render(request, 'website/blog/web_blogs/the-role-of-taxi-services-in-emergency-situations.html')

def role_of_technology_in_outstation_taxi_fare_calculation(request):
    return render(request, 'website/blog/web_blogs/the-role-of-technology-in-outstation-taxi-fare-calculation.html')

def role_of_technology_in_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/the-role-of-technology-in-outstation-taxi-services.html')

def ultimate_guide_to_outstation_car_booking(request):
    return render(request, 'website/blog/web_blogs/the-ultimate-guide-to-outstation-car-booking.html')

def tips_for_a_smooth_airport_taxi_ride_with_pets(request):
    return render(request, 'website/blog/web_blogs/tips-for-a-smooth-airport-taxi-ride-with-pets.html')

def tips_for_a_smooth_outstation_taxi_booking_experience(request):
    return render(request, 'website/blog/web_blogs/tips-for-a-smooth-outstation-taxi-booking-experience.html')

def tips_for_booking_a_car_service_for_outstation_travel(request):
    return render(request, 'website/blog/web_blogs/tips-for-booking-a-car-service-for-outstation-travel.html')

def tips_for_booking_airport_taxis_during_holiday_seasons(request):
    return render(request, 'website/blog/web_blogs/tips-for-booking-airport-taxis-during-holiday-seasons.html')

def tips_for_booking_outstation_taxis_during_festivals_and_holidays(request):
    return render(request, 'website/blog/web_blogs/tips-for-booking-outstation-taxis-during-festivals-and-holidays.html')

def tips_for_hassle_free_outstation_car_booking_near_me(request):
    return render(request, 'website/blog/web_blogs/tips-for-hassle-free-outstation-car-booking-near-me.html')

def tips_for_senior_citizens_traveling_via_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/tips-for-senior-citizens-traveling-via-outstation-taxis.html')

def tips_for_traveling_with_elderly_family_members_in_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/tips-for-traveling-with-elderly-family-members-in-outstation-taxis.html')

def top_5_cars_for_outstation_travel_from_car_bazar(request):
    return render(request, 'website/blog/web_blogs/top-5-cars-for-outstation-travel-from-car-bazar.html')

def top_5_outstation_taxi_myths_debunked(request):
    return render(request, 'website/blog/web_blogs/top-5-outstation-taxi-myths-debunked.html')

def top_5_reasons_to_use_our_taxi_service_for_airport_transfers(request):
    return render(request, 'website/blog/web_blogs/top-5-reasons-to-use-our-taxi-service-for-airport-transfers.html')

def top_airport_taxi_apps_for_quick_booking(request):
    return render(request, 'website/blog/web_blogs/top-airport-taxi-apps-for-quick-booking.html')

def top_airport_taxi_apps_you_should_try(request):
    return render(request, 'website/blog/web_blogs/top-airport-taxi-apps-you-should-try.html')

def top_airport_taxi_companies_around_the_world(request):
    return render(request, 'website/blog/web_blogs/top-airport-taxi-companies-around-the-world.html')

def top_airport_taxi_services_for_international_arrivals(request):
    return render(request, 'website/blog/web_blogs/top-airport-taxi-services-for-international-arrivals.html')

def top_car_rentals_for_outstation_travel_near_me(request):
    return render(request, 'website/blog/web_blogs/top-car-rentals-for-outstation-travel-near-me.html')

def top_destinations_for_outstation_car_hire(request):
    return render(request, 'website/blog/web_blogs/top-destinations-for-outstation-car-hire.html')

def top_destinations_for_outstation_car_trips(request):
    return render(request, 'website/blog/web_blogs/top-destinations-for-outstation-car-trips.html')

def top_luxury_airport_taxi_services_around_the_world(request):
    return render(request, 'website/blog/web_blogs/top-luxury-airport-taxi-services-around-the-world.html')

def top_reasons_to_pre_arrange_airport_taxi_services(request):
    return render(request, 'website/blog/web_blogs/top-reasons-to-pre-arrange-airport-taxi-services.html')

def top_safety_features_in_modern_airport_taxis(request):
    return render(request, 'website/blog/web_blogs/top-safety-features-in-modern-airport-taxis.html')

def top_scenic_routes_to_explore_with_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/top-scenic-routes-to-explore-with-outstation-taxis.html')

def top_tips_for_booking_outstation_cars(request):
    return render(request, 'website/blog/web_blogs/top-tips-for-booking-outstation-cars.html')

def top_tips_for_hassle_free_airport_taxi_bookings(request):
    return render(request, 'website/blog/web_blogs/top-tips-for-hassle-free-airport-taxi-bookings.html')

def top_tips_for_outstation_car_booking(request):
    return render(request, 'website/blog/web_blogs/top-tips-for-outstation-car-booking.html')


def top_tips_for_stress_free_airport_taxi_rides(request):
    return render(request, 'website/blog/web_blogs/top-tips-for-stress-free-airport-taxi-rides.html')

def traveling_alone_tips_for_using_outstation_taxis_safely(request):
    return render(request, 'website/blog/web_blogs/traveling-alone-tips-for-using-outstation-taxis-safely.html')

def traveling_with_kids_in_outstation_taxis_tips_for_a_smooth_journey(request):
    return render(request, 'website/blog/web_blogs/traveling-with-kids-in-outstation-taxis-tips-for-a-smooth-journey.html')

def ultimate_guide_to_car_hire_for_outstation_trips(request):
    return render(request, 'website/blog/web_blogs/ultimate-guide-to-car-hire-for-outstation-trips.html')

def understanding_airport_taxi_pricing_a_guide(request):
    return render(request, 'website/blog/web_blogs/understanding-airport-taxi-pricing-a-guide.html')

def understanding_airport_taxi_regulations_and_licensing(request):
    return render(request, 'website/blog/web_blogs/understanding-airport-taxi-regulations-and-licensing.html')

def understanding_local_regulations_for_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/understanding-local-regulations-for-outstation-taxi-services.html')

def understanding_outstation_car_booking_charges(request):
    return render(request, 'website/blog/web_blogs/understanding-outstation-car-booking-charges.html')

def understanding_outstation_taxi_insurance_what_you_need_to_know(request):
    return render(request, 'website/blog/web_blogs/understanding-outstation-taxi-insurance-what-you-need-to-know.html')

def understanding_taxi_charges_flat_rates_vs_metered_fare_for_outstation_travel(request):
    return render(request, 'website/blog/web_blogs/understanding-taxi-charges-flat-rates-vs-metered-fare-for-outstation-travel.html')

def understanding_taxi_fare_structures_what_you_need_to_know(request):
    return render(request, 'website/blog/web_blogs/understanding-taxi-fare-structures-what-you-need-to-know.html')

def understanding_taxi_service_ratings_and_reviews(request):
    return render(request, 'website/blog/web_blogs/understanding-taxi-service-ratings-and-reviews.html')

def understanding_the_costs_of_car_services_for_outstation_trips(request):
    return render(request, 'website/blog/web_blogs/understanding-the-costs-of-car-services-for-outstation-trips.html')

def understanding_the_costs_of_outstation_taxi_services_what_to_expect(request):
    return render(request, 'website/blog/web_blogs/understanding-the-costs-of-outstation-taxi-services-what-to-expect.html')

def understanding_the_different_types_of_outstation_taxi_services(request):
    return render(request, 'website/blog/web_blogs/understanding-the-different-types-of-outstation-taxi-services.html')

def using_airport_taxis_for_short_layovers_a_quick_guide(request):
    return render(request, 'website/blog/web_blogs/using-airport-taxis-for-short-layovers-a-quick-guide.html')

def utilizing_outstation_taxis_for_airport_transfers_a_complete_guide(request):
    return render(request, 'website/blog/web_blogs/utilizing-outstation-taxis-for-airport-transfers-a-complete-guide.html')

def utilizing_taxi_services_for_corporate_events(request):
    return render(request, 'website/blog/web_blogs/utilizing-taxi-services-for-corporate-events.html')

def ways_airport_taxis_improve_your_travel_experience(request):
    return render(request, 'website/blog/web_blogs/ways-airport-taxis-improve-your-travel-experience.html')

def what_happens_if_you_leave_something_in_an_airport_taxi(request):
    return render(request, 'website/blog/web_blogs/what-happens-if-you-leave-something-in-an-airport-taxi.html')

def what_to_do_if_your_airport_taxi_doesnt_show_up(request):
    return render(request, 'website/blog/web_blogs/what-to-do-if-your-airport-taxi-doesnt-show-up.html')

def what_to_do_if_your_airport_taxi_is_late(request):
    return render(request, 'website/blog/web_blogs/what-to-do-if-your-airport-taxi-is-late.html')

def what_to_do_when_your_airport_taxi_is_running_late(request):
    return render(request, 'website/blog/web_blogs/what-to-do-when-your-airport-taxi-is-running-late.html')

def what_to_expect_from_a_premium_airport_taxi_service(request):
    return render(request, 'website/blog/web_blogs/what-to-expect-from-a-premium-airport-taxi-service.html')

def what_to_expect_when_taking_a_taxi_for_the_first_time(request):
    return render(request, 'website/blog/web_blogs/what-to-expect-when-taking-a-taxi-for-the-first-time.html')

def what_to_look_for_in_a_kid_friendly_airport_taxi_service(request):
    return render(request, 'website/blog/web_blogs/what-to-look-for-in-a-kid-friendly-airport-taxi-service.html')

def what_to_look_for_when_hiring_an_outstation_taxi_driver(request):
    return render(request, 'website/blog/web_blogs/what-to-look-for-when-hiring-an-outstation-taxi-driver.html')

def what_travelers_expect_from_airport_taxi_services_in_2024(request):
    return render(request, 'website/blog/web_blogs/what-travelers-expect-from-airport-taxi-services-in-2024.html')

def why_airport_taxis_are_a_safer_option_for_solo_travelers(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-a-safer-option-for-solo-travelers.html')

def why_airport_taxis_are_a_stress_free_option_for_families(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-a-stress-free-option-for-families.html')

def why_airport_taxis_are_a_time_saver_for_frequent_flyers(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-a-time-saver-for-frequent-flyers.html')

def why_airport_taxis_are_the_best_choice_for_business_travelers(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-the-best-choice-for-business-travelers.html')

def why_airport_taxis_are_the_best_option_for_early_morning_flights(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-the-best-option-for-early-morning-flights.html')

def why_airport_taxis_are_the_most_reliable_choice_for_transfers(request):
    return render(request, 'website/blog/web_blogs/why-airport-taxis-are-the-most-reliable-choice-for-transfers.html')

def why_choose_local_car_booking_services_for_outstation_trips(request):
    return render(request, 'website/blog/web_blogs/why-choose-local-car-booking-services-for-outstation-trips.html')

def why_local_airport_taxi_services_are_still_popular(request):
    return render(request, 'website/blog/web_blogs/why-local-airport-taxi-services-are-still-popular.html')
def why_off_season_travel_is_the_best_time_to_book_outstation_taxis(request):
    return render(request, 'website/blog/web_blogs/why-off-season-travel-is-the-best-time-to-book-outstation-taxis.html')

def why_tipping_your_airport_taxi_driver_matters(request):
    return render(request, 'website/blog/web_blogs/why-tipping-your-airport-taxi-driver-matters.html')

def why_weekend_outstation_taxi_rates_are_higher_and_how_to_save(request):
    return render(request, 'website/blog/web_blogs/why-weekend-outstation-taxi-rates-are-higher-and-how-to-save.html')

def why_you_should_choose_a_taxi_over_rideshare(request):
    return render(request, 'website/blog/web_blogs/why-you-should-choose-a-taxi-over-rideshare.html')

def airport_taxi_driver_training_what_it_involves(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-driver-training-what-it-involves.html')

def airport_taxi_etiquette_for_first_time_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-for-first-time-travelers.html')

def airport_taxi_etiquette_tips_for_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-tips-for-travelers.html')

def airport_taxi_etiquette_what_you_need_to_know(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-etiquette-what-you-need-to-know.html')

def airport_taxi_safety_features_you_should_look_for(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-features-you-should-look-for.html')

def airport_taxi_safety_measures_for_solo_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-measures-for-solo-travelers.html')

def airport_taxi_safety_tips_for_women_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-tips-for-women-travelers.html')

def airport_taxi_safety_what_you_should_know(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-safety-what-you-should-know.html')

def airport_taxi_services_a_sustainable_future(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-a-sustainable-future.html')

def airport_taxi_services_for_business_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-business-travelers.html')

def airport_taxi_services_for_city_layovers_exploring_your_options(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-city-layovers-exploring-your-options.html')

def airport_taxi_services_for_disabled_travelers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-disabled-travelers.html')

def airport_taxi_services_for_early_morning_and_late_night_flights(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-early-morning-and-late-night-flights.html')

def airport_taxi_services_for_elderly_passengers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-elderly-passengers.html')

def airport_taxi_services_for_frequent_flyers(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-frequent-flyers.html')

def airport_taxi_services_for_last_minute_flight_changes(request):
    return render(request, 'website/blog/web_blogs/airport-taxi-services-for-last-minute-flight-changes.html')



#############

def about(request):
    return render(request, 'website/about.html')

@csrf_exempt 
def save_enquiry(request):
    print("Received request:", request.method)  
    if request.method == 'POST':
        cust_name = request.POST.get('cust_name')
        cust_phone_number = request.POST.get('cust_phone_number')
        cust_email = request.POST.get('cust_email')
        service = request.POST.get('service')
        cust_message = request.POST.get('cust_message')

        try:
            enquiry = Enquiry.objects.create(cust_name=cust_name, cust_phone_number=cust_phone_number, cust_email=cust_email, service=service, cust_message=cust_message)
            return JsonResponse({'success': 'Enquiry saved successfully!'})
        except Exception as e:
            print("Error saving enquiry:", e)  
            return JsonResponse({'error': 'Failed to save enquiry.'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



def search_url(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    pickup_date = request.GET.get('pickup_date')
    pickup_time = request.GET.get('pickup_time')
    ridetype = request.GET.get('ridetype')
    trip_type = request.GET.get('trip_type') 

    if not source or not destination or not pickup_date:
        return HttpResponse("All fields are required.", status=400)

    if ridetype == 'airport':
        if trip_type == 'one_way':
            search_url = reverse('airportcabs_list')  
        elif trip_type == 'round_trip':
            search_url = reverse('airport_roundtrip')  
        else:
            return HttpResponse("Invalid trip type for airport rides.", status=400)
    elif ridetype == 'local':
        search_url = reverse('localcabs_list')
    elif ridetype == 'localpackage':
        search_url = reverse('cabs_list')
    elif ridetype == 'outstation':
        if not trip_type:
            return HttpResponse("Trip type is required for outstation rides.", status=400)
        
        if trip_type == 'one_way':
            search_url = reverse('outstation_oneway')
        elif trip_type == 'round_trip':

            drop_date = request.GET.get('drop_date')
            drop_time = request.GET.get('drop_time')
            if not drop_date or not drop_time:
                return HttpResponse("Drop date and drop time are required for round trip.", status=400)
            search_url = reverse('outstation_roundtrip')
        else:
            return HttpResponse("Invalid trip type for outstation.", status=400)
    else:
        return HttpResponse("Invalid ride type.", status=400)

    search_url += f"?location1={source}&location2={destination}&pickup_date={pickup_date}&pickup_time={pickup_time}&ridetype={ridetype}&trip_type={trip_type}"

    if ridetype == 'outstation' and trip_type == 'round_trip':
        search_url += f"&drop_date={drop_date}&drop_time={drop_time}"

    return redirect(search_url)

def airportcabs_list(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    pricing_dict = {}

    if ride_type_instance:
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type,  
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }

    return render(request, 'website/cabs_list.html', context)

def airport_roundtrip(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    pricing_dict = {}

    if ride_type_instance:
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type, 
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }

    return render(request, 'website/airport_roundtrip.html', context)

def localcabs_list(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    pricing_dict = {}

    if ride_type_instance:
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type,  
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/localcabs_list.html', context)



def outstation_oneway(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    pricing_dict = {}

    if ride_type_instance:
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type,  
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/outstation_oneway.html', context)


def outstation_roundtrip(request):
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    pricing_dict = {}

    if ride_type_instance:
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type, 
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/outstation_roundtrip.html', context)


def booking_list(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    pickup_date = request.GET.get('pickup_date')
    pickup_time = request.GET.get('pickup_time')
    category = request.GET.get('category')
    ridetype = request.GET.get('ridetype')
    car_type = request.GET.get('car_type', '')  
    price = request.GET.get('price')
    slots = request.GET.get('time_slot')
    trip_type = request.GET.get('trip_type')
    drop_date = request.GET.get('drop_date') 
    drop_time = request.GET.get('drop_time') 

    print("Price received in view:", price)
    print("car_type received in view:", car_type)
    print("----------", ridetype)

    pricing_instances = Pricing.objects.filter(
        category__category_name=category,
        ridetype__name=ridetype,
        car_type=car_type,
        slots=slots,  
        trip_type=trip_type
    )

    if pricing_instances.count() == 1:
        pricing_instance = pricing_instances.first()
    elif pricing_instances.count() > 1:
        print("Multiple Pricing instances found. Choosing the first one.")
        pricing_instance = pricing_instances.first()  
    else:
        pricing_instance = None
        print("No Pricing instances found.")
    
    return render(request, 'website/booking_list.html', {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'category': category,
        'ridetype': ridetype,
        'car_type': car_type,
        'price': price,
        'pricing': pricing_instance, 
        'drop_date': drop_date, 
        'drop_time': drop_time, 
        'trip_type': trip_type,
    })



@csrf_exempt
def search_phone_numbers(request):
    phone_number = request.GET.get('phone_number', '')
    if phone_number:
        customers = Customer.objects.filter(phone_number__icontains=phone_number)
        customers_data = [{
            'phone_number': customer.phone_number,
            'customer_name': customer.customer_name,
            'customer_id': customer.customer_id
        } for customer in customers]
        return JsonResponse({'success': True, 'customers': customers_data})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def get_customer_details(request):
    phone_number = request.GET.get('phone_number')
    try:
        customer = Customer.objects.get(phone_number=phone_number)
        data = {
            'customer_id': customer.customer_id,
            'customer_name': customer.customer_name,
            'email': customer.email,
            'address': customer.address,
            'password': customer.password,
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    

def bookride(request):
    last_ride = RideDetails.objects.all().order_by('-ride_id').first()
    last_company_format = ''
    next_company_format = 'RID01'

    current_slot = get_current_time_slot()
    
    if current_slot:
        if current_slot == '12 am - 6 am':
            records = Pricing.objects.filter(slots="12AM - 6AM")
        elif current_slot == '6 am - 12 pm':
            records = Pricing.objects.filter(slots="6AM - 12PM")
        elif current_slot == '12 pm - 6 pm':
            records = Pricing.objects.filter(slots="12PM - 6PM")
        else:
            records = Pricing.objects.filter(slots="6PM - 12AM")
        
    
    context={
        'customerlist':Customer.objects.all(),
        'ridetypelist': Ridetype.objects.all(),
        'ridetypelist':Ridetype.objects.all(),
        'catlist':Category.objects.all(),
        'blist': Brand.objects.all(),
        'modellist' : Model.objects.all(),
        'next_company_format':next_company_format,
        'Pricing':records
    }
        
    return render(request, 'website/book-ride.html',context)


class AddContact(TemplateView):
    template_name = "website/contact.html"

    def post(self , request):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        cu = ContactUs()
        cu.name = name
        cu.email = email
        cu.subject = subject
        cu.message = message
        cu.save()
        return JsonResponse({'status':"Success"})


def services(request):
    return render(request, 'website/service.html')


def airporttaxi(request):
    return render(request, 'website/airporttaxi.html')


def outstationcabs(request):
    return render(request, 'website/outstationcabs.html')


def localtaxi(request):
    return render(request, 'website/localtaxi.html')

def blog(request):
    blogs = Blogs.objects.all()
    return render(request, 'website/blog.html', {'blogs': blogs})

class BlogDetailView(View):
    def get(self, request, title):
        blogs = Blogs.objects.all()
        blog = None

        for b in blogs:
            if slugify(b.title) == title:
                blog = b
                break

        if blog is None:
            return render(request, '404.html')

        if slugify(blog.title) != title and blog.slug:
            return redirect('blog_detail', title=slugify(blog.title))

        description = blog.description.split(',')

        return render(request, 'website/blog/blog_detail.html', {'blog': blog,'description': description})

    
def faq(request):
    return render(request, 'website/faq.html')

def terms(request):
    return render(request, 'website/terms.html')


class login_page(TemplateView,APIView):
    template_name = "website/login.html"

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                if user.is_superuser:
                    redirect_url = '/superadmin/index'
                    request.session['user_type'] = "Superadmin"
                    request.session['user_id'] = user.id
                else:
                    return JsonResponse({'success': False, 'message': 'Profile does not exist for this user'})
            else:
                if user.is_superuser:
                    redirect_url = '/superadmin/index'
                    request.session['user_type'] = "Superadmin"
                    request.session['user_id'] = profile.profile_id
                elif profile.type == 'admin':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/adminuser/adindex'
                elif profile.type == 'quality':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/quality/qindex'
                elif profile.type == 'telecaller':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/telecaller'
                elif profile.type == 'distributer':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/distributer/'
                elif profile.type == 'rescue':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/rescue/'
                elif profile.type == 'driver':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/driver/driverindex'
                elif profile.type == 'hr':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/hr/hrindex'
                elif profile.type == 'author':
                    request.session['user_type'] = profile.type
                    request.session['user_id'] = profile.profile_id
                    redirect_url = '/author/authorindex'
                else:
                    redirect_url = '/'
                
            return JsonResponse({'success': True, 'redirect_url': redirect_url})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'})
    return render(request, 'website/login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

class AddNewBooking(APIView):

    def parse_date(self, date_str):
        """Helper function to parse dates in multiple formats"""
        for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date {date_str} is not in a recognized format.")

    def post(self, request):
        try:
            pickup_date_str = request.POST.get('pickup_date', '')
            pickup_time_str = request.POST.get('pickup_time', '')

            if not pickup_date_str:
                return JsonResponse({'status': 'Error', 'message': 'Pickup date is required'})
            if not pickup_time_str:
                return JsonResponse({'status': 'Error', 'message': 'Pickup time is required'})

            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            pickup_time = datetime.strptime(pickup_time_str, '%H:%M').strftime('%H:%M:%S')
            

            current_time = datetime.now()


            time_str = current_time.strftime('%H%M%S')
            company_format = "WB" + time_str
            bookings_from = "website"
            category = request.POST['category']
            source = request.POST['source']
            destination = request.POST['destination']
            customer_phone_number = request.POST['phone_number']
            address = request.POST['address']
            customer_name = request.POST['customer_name']
            customer_email = request.POST['email']
            password = request.POST['password']
            customer_notes = request.POST['customer_notes']
            total_fare=request.POST['total_fare']
            car_type = request.POST.get('car_type', '').strip()  
            ridetype_name = request.POST.get('ridetype', '').strip()
            slots = determine_time_slot(pickup_time_str)  


            if not ridetype_name:
                return JsonResponse({"status": "Error", "message": "Ride type is required."})

            try:
                ridetype_instance = Ridetype.objects.get(name=ridetype_name)
            except Ridetype.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Ride type does not exist."})


            try:
                category_instance = Category.objects.get(category_name=category)
            except Category.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Category does not exist."})
            
            try:
                if ridetype_name.lower() == 'local':
                    pricing_instance = Pricing.objects.get(
                        category=category_instance,
                        car_type=car_type,
                        ridetype=ridetype_instance,  
                        slots=slots
                    )
                else:
                    trip_type = request.POST.get('trip_type', '').strip()
                    pricing_instance = Pricing.objects.get(
                        category=category_instance,
                        car_type=car_type,
                        ridetype=ridetype_instance,
                        slots=slots,
                        trip_type=trip_type
                    )
            except Pricing.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Pricing information for the selected category, car type, and ride type does not exist."})

            if ridetype_name == 'outstation' and pricing_instance.trip_type == 'round_trip':
                drop_date_str = request.POST.get('drop_date', '')
                drop_time_str = request.POST.get('drop_time', '')

                drop_date = self.parse_date(drop_date_str) if drop_date_str else None
                drop_time = datetime.strptime(drop_time_str, '%H:%M').time() if drop_time_str else None
            else:
                drop_date = None
                drop_time = None    

            customer_exits = Customer.objects.filter(phone_number=customer_phone_number).count()
            if customer_exits>0:
                customer = Customer.objects.get(phone_number=customer_phone_number)
                print(customer.email!=customer_email,customer.email,customer_email)
                if customer.email!=customer_email:
                    print("going back")
                    return JsonResponse({'status': 'Error', 'message': "Customer's email or phone number does not match"})
            else:
                last_cust = Customer.objects.all().order_by('-customer_id').first()
                if last_cust:
                    last_company_format = int(last_cust.company_format.replace('CUST', ''))
                    next_company_format = f'CUST{last_company_format + 1:02}'
                else:
                    next_company_format = 'CUST01'
                cust = Customer(
                        customer_name=customer_name,
                        phone_number=customer_phone_number,
                        email=customer_email,
                        address=address,
                        password=password,
                        status="active",
                        company_format=next_company_format,
                        )
                cust.save()
                customer = Customer.objects.get(phone_number=customer_phone_number)
                customer = Customer.objects.get(phone_number=customer_phone_number)
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'
            
            try:
                ride_details = RideDetails()
                ride_details.company_format=company_format
                ride_details.customer=Customer.objects.get(phone_number=customer_phone_number)
                ride_details.ridetype=ridetype_instance
                ride_details.category=category_instance
                ride_details.total_fare=total_fare
                ride_details.source=source
                ride_details.destination=destination
                ride_details.pickup_date=pickup_date
                ride_details.pickup_time=pickup_time
                ride_details.customer_notes=customer_notes
                ride_details.ride_status=ride_status
                ride_details.bookings_from=bookings_from

                ride_details.pricing = pricing_instance 
                ride_details.drop_date = drop_date 
                ride_details.drop_time = drop_time 

                if request.user.is_authenticated:
                    ride_details.assigned_by = request.user
                    ride_details.created_by = request.user
                    ride_details.updated_by = request.user

                ride_details.save()
                print("source ^^^: ",request.POST['source'] )
                print("source ^^^: ", request.POST['destination'])
                whatsapp = {
                    "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                    "campaignName": "booking confirmation",
                    "destination": customer_phone_number,
                    "userName": "Ridexpress",
                    "templateParams": [
                        customer_name,
                        company_format,
                        pickup_date +'  ' +pickup_time,    
                        source,
                        destination
                    ],
                    "source": "new-landing-page form",
                    "media": {},
                    "buttons": [],
                    "carouselCards": [],
                    "location": {},
                    "paramsFallbackValue": {
                        "FirstName": "user"
                    }
                    }
                gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
                try:
                    response = requests.post(gateway_url, data=whatsapp)
                    if response.status_code == 200:
                        print("Message sent successfully")
                    else:
                        print(f"Failed to send message. Status code: {response.status_code}")
                        print(response.text)  
                except requests.RequestException as e:
                    print(f"Error sending message: {e}")
            except IntegrityError as e:
                print("IntegrityError:", e)
            
            except Exception as e:
                print("Error ^^^: ", str(e))
            return JsonResponse({'status': "Success", 'message': 'Ride details added successfully'})
        except Customer.DoesNotExist:
            print(f"Customer with phone {customer_phone_number} does not exist.")
            return JsonResponse({'status': 'Error', 'message': f'Customer with phone {customer_phone_number} does not exist.'})
        except Exception as e:
            print("^^^^^^: ", str(e))
            print(f"Error saving ride details: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)})

def determine_time_slot(pickup_time_str):
    pickup_time = datetime.strptime(pickup_time_str, '%H:%M').time()
    if time(0, 0) <= pickup_time < time(6, 0):
        return '12AM - 6AM'
    elif time(6, 0) <= pickup_time < time(12, 0):
        return '6AM - 12PM'
    elif time(12, 0) <= pickup_time < time(18, 0):
        return '12PM - 6PM'
    else:
        return '6PM - 12AM'

def get_owner_details(request):
    phone_number = request.GET.get('phone_number')
    try:
        owner = VehicleOwner.objects.get(phone_number=phone_number)
        data = {
            'owner_id': owner.owner_id,
            'name': owner.name,
            'email': owner.email,
            'address': owner.address,
            'image': owner.image.url if owner.image else None,  
            'address_proof': owner.address_proof.url if owner.address_proof else None,
            'identity': owner.identity.url if owner.identity else None,
            'holdername': owner.holdername,
            'ac_number': owner.ac_number,
            'bankname': owner.bankname,
            'ifsc_code': owner.ifsc_code,
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'owner not found'}, status=404)

def check_vehicleno(request):
    Vehicle_Number = request.GET.get('Vehicle_Number', None)
    vehicleno = Vehicle.objects.filter(Vehicle_Number=Vehicle_Number)
    data = {
        'exists': vehicleno.count() > 0
    }
    return JsonResponse(data)

class AddVehicle(TemplateView):
    template_name = "website/addvehicle.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['catlist'] = Category.objects.filter(category_status='active')
        context['blist'] = Brand.objects.filter(status='active')
        context['ownerlist'] = VehicleOwner.objects.filter(status='active',verification_status='verified')
        context['modellist'] = Model.objects.filter(status='active')
        context['vtypelist'] = VehicleType.objects.all()
        context['ctypelist'] = CommissionType.objects.all()
        context['colorlist'] = Color.objects.all()
        context['tlist'] = Transmission.objects.all()
        
        return context
    
    def post(self, request):
        last_vehicle = Vehicle.objects.all().order_by('-vehicle_id').first()
        if last_vehicle:
            try:
                last_company_format = int(last_vehicle.company_format.replace('VEH', ''))
            except ValueError:
                last_company_format = last_vehicle.vehicle_id
            next_company_format = f'VEH{last_company_format + 1:02}'
        else:
            next_company_format = 'VEH01'

        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        image = request.FILES.get('image', None)
        address_proof = request.FILES.get('address_proof', None)
        identity = request.FILES.get('identity', None)
        holdername = request.POST['holdername']
        ac_number = request.POST['ac_number']
        bankname = request.POST['bankname']
        ifsc_code = request.POST['ifsc_code']

        vehicle_number = request.POST['Vehicle_Number']
        model_id = request.POST['model']
        year = request.POST['year']
        insurance_expiry = request.POST['insurance_expiry']
        car_type = request.POST['car_type']
        color_id = request.POST['color']
        transmission_id = request.POST['transmission']
        owner_id = request.POST['owner']
        vehicle_type_id = request.POST['vehicle_type']
        registration_certificate = request.FILES.get('registration_certificate')
        fc_certificate = request.FILES.get('fc_certificate')
        insurance_policy = request.FILES.get('insurance_policy')
        permit_details = request.FILES.get('permit_details')
        tax_details = request.FILES.get('tax_details')
        emission_test = request.FILES.get('emission_test')
        vehicle_status = "active"
        drive_status = request.POST['drive_status']
        company_format = next_company_format

        owner_exits = VehicleOwner.objects.filter(phone_number=phone_number).count()
        if owner_exits>0:
            owner = VehicleOwner.objects.get(phone_number=phone_number)
            print(owner.ac_number!=ac_number,owner.ac_number,ac_number)
            if owner.ac_number!=ac_number:
                print("going back")
                return JsonResponse({'status': 'Error', 'message': "Owner's account number or phone number does not match"})
        else:
            last_owner = VehicleOwner.objects.all().order_by('-owner_id').first()
            if last_owner:
                last_company_format = int(last_owner.company_format.replace('VO', ''))
                next_company_format = f'VO{last_company_format + 1:02}'
            else:
                next_company_format = 'VO01'

            owner = VehicleOwner(
                    name=name,
                    phone_number=phone_number,
                    email=email,
                    address=address,
                    image=image,
                    address_proof=address_proof,
                    identity=identity,
                    holdername=holdername,
                    bankname=bankname,
                    ac_number=ac_number,
                    ifsc_code=ifsc_code,
                    status="active",
                    company_format=next_company_format,
                    created_by=request.user,
                    updated_by=request.user)
            owner.save()
            owner = VehicleOwner.objects.get(phone_number=phone_number)

        vehicle = Vehicle(
            Vehicle_Number=vehicle_number,
            model=Model.objects.get(model_id=model_id),
            year=year,
            insurance_expiry=insurance_expiry,
            car_type=car_type,
            color=Color.objects.get(color_id=color_id),
            transmission=Transmission.objects.get(transmission_id=transmission_id),
            owner=VehicleOwner.objects.get(phone_number=phone_number),
            vehicle_type=VehicleType.objects.get(vehicle_type_id=vehicle_type_id),
            vehicle_status=vehicle_status,
            drive_status=drive_status,
            company_format=company_format,
        )

        if registration_certificate:
            vehicle.registration_certificate=registration_certificate
        if fc_certificate:
            vehicle.fc_certificate=fc_certificate
        if insurance_policy:
            vehicle.insurance_policy=insurance_policy
        if tax_details:
            vehicle.tax_details=tax_details
        if permit_details:
            vehicle.permit_details=permit_details
        if emission_test:
            vehicle.emission_test=emission_test

        vehicle.save()
        
        payload = {
            "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
            "campaignName": "pre_verification_vehicle",
            "destination": vehicle.owner.phone_number, 
            "userName": "Ridexpress",
            "templateParams": [
                vehicle.owner.name, 
                f"{vehicle.Vehicle_Number} - {vehicle.model.brand.category.category_name} - {vehicle.model.brand.brand_name} - {vehicle.model.model_name}"
                ], 
            "source": "new-landing-page form",
            "paramsFallbackValue": {
                 "FirstName": "user"
            }
        }
        gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
        response = requests.post(gateway_url, json=payload, headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            return JsonResponse({'status': "Success", 'message': "Your details have been submitted. Once the verification is done, you will get a WhatsApp message."})
        else:
            return JsonResponse({'status': "Error", 'message': "Vehicle added, but failed to send WhatsApp notification."})

class AirportGetRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse
        from datetime import datetime

        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        time_slot = request.POST['time_slot']
        ridetype = request.POST['ridetype']
        trip_type = request.POST['trip_type'] 
        toll_option = request.POST.get('toll_option')
        print("Backend received toll option: ", toll_option) 

        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print("Distance calculated: ", distance)  

        costs = {}

        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        pricing_details = Pricing.objects.select_related('category').filter(slots=time_slot, ridetype=ride_type_instance,trip_type=trip_type)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            toll_price = Decimal(str(price.toll_price)) if toll_option == 'add_toll' else Decimal(0)
            print(f"Toll option: {toll_option}, Toll price applied: {toll_price}")  

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price, toll_price)

        return JsonResponse({'costs': pricing_dict})

    def calculate_cost(self, distance, price, toll_price):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        driver_beta_decimal = Decimal(str(price.driver_beta))

        temp_cost = Decimal(distance) * price_per_km_decimal
        temp_cost += permit_decimal + toll_price + driver_beta_decimal
        category_cost = round(temp_cost, 0)

        print(f"Calculated cost: {category_cost}, Permit: {permit_decimal}, Toll: {toll_price}, Beta: {driver_beta_decimal}") 

        return {
            'distance_km': distance,
            'cost': category_cost,
            'permit': permit_decimal,
            'toll': toll_price,
            'beta': driver_beta_decimal,
            'category': price.category.category_name,
        }
        
class GetRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse
        from datetime import datetime

        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        time_slot = request.POST['time_slot']
        ridetype = request.POST['ridetype']  

        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print("Distance calculated:", distance)

        costs = {}

        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        pricing_details = Pricing.objects.select_related('category').filter(slots=time_slot, ridetype=ride_type_instance)

        print("Fetched Pricing Details: ", pricing_details)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower() 

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price)

        print("Pricing Dict after calculation: ", pricing_dict)
        return JsonResponse({'costs': pricing_dict})
    
    def calculate_cost(self, distance, price):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        toll_price_decimal = Decimal(str(price.toll_price))
        driver_beta_decimal = Decimal(str(price.driver_beta))

        temp_cost = Decimal(distance) * price_per_km_decimal
        temp_cost += permit_decimal + toll_price_decimal + driver_beta_decimal
        category_cost = round(temp_cost, 0)

        return {
            'distance_km': distance,
            'cost': category_cost,
            'permit': permit_decimal,
            'toll': toll_price_decimal,
            'beta': driver_beta_decimal,
            'category': price.category.category_name,
        }
    


class OnewayRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse
        from datetime import datetime

        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        time_slot = request.POST['time_slot']
        ridetype = request.POST['ridetype'] 
        trip_type = request.POST['trip_type'] 

        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print("Distance calculated:", distance)

        costs = {}

        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        pricing_details = Pricing.objects.select_related('category').filter(slots=time_slot, ridetype=ride_type_instance,trip_type=trip_type)

        print("Fetched Pricing Details: ", pricing_details)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price)

        print("Pricing Dict after calculation: ", pricing_dict)
        return JsonResponse({'costs': pricing_dict})
    
    def calculate_cost(self, distance, price):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        toll_price_decimal = Decimal(str(price.toll_price))
        driver_beta_decimal = Decimal(str(price.driver_beta))

        temp_cost = Decimal(distance) * price_per_km_decimal
        temp_cost += permit_decimal + toll_price_decimal + driver_beta_decimal
        category_cost = round(temp_cost, 0)

        return {
            'distance_km': distance,
            'cost': category_cost,
            'permit': permit_decimal,
            'toll': toll_price_decimal,
            'beta': driver_beta_decimal,
            'category': price.category.category_name,
        } 



class RoundtripRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse

        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date_str = request.POST['pickup_date']
        pickup_time_str = request.POST['pickup_time']
        drop_date_str = request.POST['drop_date']
        drop_time_str = request.POST['drop_time']
        time_slot = request.POST['time_slot']
        ridetype = request.POST['ridetype']
        trip_type = request.POST['trip_type']

        pickup_datetime = datetime.strptime(f"{pickup_date_str} {pickup_time_str}", "%m/%d/%Y %H:%M")
        drop_datetime = datetime.strptime(f"{drop_date_str} {drop_time_str}", "%m/%d/%Y %H:%M")

        if drop_datetime.date() > pickup_datetime.date():
            num_days = 1
            end_of_pickup_day = pickup_datetime.replace(hour=23, minute=59, second=59)

            if drop_datetime > end_of_pickup_day:
                num_days += (drop_datetime.date() - pickup_datetime.date()).days
        else:
            num_days = 1

        print(f"Total days for the trip: {num_days}")

        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print(f"Distance between {source} and {destination}: {distance} km")

        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        pricing_details = Pricing.objects.select_related('category').filter(
            slots=time_slot, ridetype=ride_type_instance, trip_type=trip_type
        )

        print("Fetched Pricing Details: ", pricing_details)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name.lower()
            car_type = price.car_type.lower()  

            if 'mini' in category_name or 'sedan' in category_name:
                daily_km_cap = 250 * num_days
            else:
                daily_km_cap = 300 * num_days

            print(f"Total allowed km for {num_days} day(s) for {category_name}: {daily_km_cap} km")

            applicable_distance = max(distance, daily_km_cap)
            print(f"Applicable distance for {category_name} based on days: {applicable_distance} km")

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            pricing_dict[category_name][car_type] = self.calculate_cost(applicable_distance, price, num_days)

        print("Pricing Dict after calculation: ", pricing_dict)
        return JsonResponse({'costs': pricing_dict})

    def calculate_cost(self, distance, price, num_days):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        toll_price_decimal = Decimal(str(price.toll_price))

        driver_beta_decimal = Decimal(str(price.driver_beta)) * Decimal(num_days)
        print(f"Driver beta for {num_days} day(s): {driver_beta_decimal}")

        temp_cost = Decimal(distance) * price_per_km_decimal
        temp_cost += permit_decimal + toll_price_decimal + driver_beta_decimal
        category_cost = round(temp_cost, 0)

        return {
            'distance_km': distance,
            'cost': category_cost,
            'permit': permit_decimal,
            'toll': toll_price_decimal,
            'beta': driver_beta_decimal,
            'category': price.category.category_name,
        }


class SendOtp(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        customer_name = request.POST.get('customer_name')
        otp = str(random.randint(100000, 999999))  

        cache.set(f'otp_{phone_number}', otp, timeout=300)

        whatsapp_payload = {
            "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
            "campaignName": "otp_verification",
            "destination": phone_number,
            "userName": "Ridexpress",
            "templateParams": [str(otp)],
            "source": "new-landing-page form",
            "buttons": [
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": 0,
                    "parameters": [
                        {
                            "type": "text",
                            "text": otp  
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post("https://backend.aisensy.com/campaign/t1/api/v2", json=whatsapp_payload)
            if response.status_code == 200:
                return JsonResponse({'status': 'Success', 'message': 'OTP sent successfully.'})
            else:
                return JsonResponse({'status': 'Error', 'message': 'Failed to send OTP.'})
        except requests.RequestException as e:
            return JsonResponse({'status': 'Error', 'message': f'Error sending OTP: {e}'})

class VerifyOtp(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        print(f"OTP verification attempt for phone number: {phone_number}, entered OTP: {otp}")

        cached_otp = cache.get(f'otp_{phone_number}')
        
        print(f"Cached OTP for phone number {phone_number}: {cached_otp}")

        if not cached_otp:
            print(f"No OTP found in cache for phone number: {phone_number}")
            return JsonResponse({'status': 'Error', 'message': 'OTP expired. Please request a new one.'})

        if cached_otp == otp:
            cache.delete(f'otp_{phone_number}')
            print(f"OTP verified successfully for phone number: {phone_number}")
            return JsonResponse({'status': 'Success', 'message': 'OTP verified successfully.'})
        else:
            print(f"Incorrect OTP entered for phone number: {phone_number}")
            return JsonResponse({'status': 'Error', 'message': 'Incorrect OTP.'})


class PackageBookingList(TemplateView):
    template_name = "website/package_booking_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package_category'] = self.request.GET.get('package_category')
        context['package_name'] = self.request.GET.get('package_name')
        context['price'] = self.request.GET.get('price')
        context['description'] = self.request.GET.get('description')
        context['source'] = self.request.GET.get('source')
        context['destination'] = self.request.GET.get('destination')
        context['pickup_date'] = self.request.GET.get('pickup_date')
        context['pickup_time'] = self.request.GET.get('pickup_time')
        return context  


class AddPackageOrder(APIView):

    def parse_date(self, date_str):
        """Helper function to parse dates in multiple formats"""
        for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date {date_str} is not in a recognized format.")

    def post(self, request):
        try:
            pickup_date_str = request.POST.get('pickup_date', '')
            pickup_time_str = request.POST.get('pickup_time', '')

            if not pickup_date_str:
                return JsonResponse({'status': 'Error', 'message': 'Pickup date is required'})
            if not pickup_time_str:
                return JsonResponse({'status': 'Error', 'message': 'Pickup time is required'})

            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            pickup_time = datetime.strptime(pickup_time_str, '%H:%M').strftime('%H:%M:%S')
            package_id = request.POST['package']
            total_amount = Decimal(request.POST.get('total_amount', '0') or '0')
            payment_method = request.POST['payment_method']
            status = request.POST['status']
            source = request.POST['source']
            destination = request.POST['destination']
            customer_phone_number = request.POST['phone_number']
            address = request.POST['address']
            customer_name = request.POST['customer_name']
            customer_email = request.POST['email']
            password = request.POST['password']

            customer_exits = Customer.objects.filter(phone_number=customer_phone_number).count()
            if customer_exits>0:
                customer = Customer.objects.get(phone_number=customer_phone_number)
                print(customer.email!=customer_email,customer.email,customer_email)
                if customer.email!=customer_email:
                    print("going back")
                    return JsonResponse({'status': 'Error', 'message': "Customer's email or phone number does not match"})
            else:
                last_cust = Customer.objects.all().order_by('-customer_id').first()
                if last_cust:
                    last_company_format = int(last_cust.company_format.replace('CUST', ''))
                    next_company_format = f'CUST{last_company_format + 1:02}'
                else:
                    next_company_format = 'CUST01'
                cust = Customer(
                        customer_name=customer_name,
                        phone_number=customer_phone_number,
                        email=customer_email,
                        address=address,
                        password=password,
                        status="active",
                        company_format=next_company_format,
                        created_by=request.user,
                        updated_by=request.user)
                cust.save()
                customer = Customer.objects.get(phone_number=customer_phone_number)

            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'
            
            try:
                ride_details = PackageOrder()
                ride_details.customer=Customer.objects.get(phone_number=customer_phone_number)
                ride_details.package=Packages.objects.get(package_id=package_id)
                ride_details.total_amount=total_amount
                ride_details.payment_method=payment_method
                ride_details.source=source
                ride_details.destination=destination
                ride_details.pickup_date=pickup_date
                ride_details.pickup_time=pickup_time
                ride_details.status=status

                ride_details.save()
                order_id = ride_details.order_id

                print("source ^^^: ",request.POST['source'] )
                print("source ^^^: ", request.POST['destination'])
                whatsapp = {
                    "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                    "campaignName": "booking confirmation",
                    "destination": customer_phone_number,
                    "userName": "Ridexpress",
                    "templateParams": [
                        customer_name,
                        order_id,  
                        pickup_date +'  ' +pickup_time,    
                        source,   
                        destination
                    ],
                    "source": "new-landing-page form",
                    "media": {},
                    "buttons": [],
                    "carouselCards": [],
                    "location": {},
                    "paramsFallbackValue": {
                        "FirstName": "user"
                    }
                    }
                gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
                try:
                    response = requests.post(gateway_url, data=whatsapp)
                    if response.status_code == 200:
                        print("Message sent successfully")
                    else:
                        print(f"Failed to send message. Status code: {response.status_code}")
                        print(response.text) 
                except requests.RequestException as e:
                    print(f"Error sending message: {e}")
            except IntegrityError as e:
                print("IntegrityError:", e)
            
            except Exception as e:
                print("Error ^^^: ", str(e))
            return JsonResponse({'status': "Success", 'message': 'Ride details added successfully'})
        except Customer.DoesNotExist:
            print(f"Customer with phone {customer_phone_number} does not exist.")
            return JsonResponse({'status': 'Error', 'message': f'Customer with phone {customer_phone_number} does not exist.'})
        except Exception as e:
            print("^^^^^^: ", str(e))
            print(f"Error saving ride details: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)})


class AddBlogView(TemplateView):
    template_name = "website/add_blog.html"

    def post(self, request):
        title = request.POST['title']
        description = request.POST['description']
        image = request.POST.get('image')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        whatsapp = request.POST.get('whatsapp')
        backlink = request.POST.get('backlink')
        related_bloglink = request.POST.get('related_bloglink')
        tags = request.POST.get('tags')
        author = request.POST.get('author')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        h1tag = request.POST.get('h1tag')

        blog = Blogs(
            title=title,
            description=description,
            image=image,
            facebook=facebook,
            instagram=instagram,
            whatsapp=whatsapp,
            backlink=backlink,
            related_bloglink=related_bloglink,
            tags=tags,
            author=author,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            h1tag=h1tag,
        )
        blog.save()
        return JsonResponse({'status': "Success"}) 

class AddwebPackages(TemplateView):
    template_name = "website/add_webpackages.html"

    def post(self, request):
        if request.method == "POST":
            title = request.POST.get('title')
            category = request.POST.get('category')
            description = request.POST.get('description')
            top_attraction = request.POST.get('top_attraction')
            why_visit = request.POST.get('why_visit')
            package_highlights = request.POST.get('package_highlights')
            facebook_link = request.POST.get('facebook_link')
            instagram_link = request.POST.get('instagram_link')
            whatsapp_link = request.POST.get('whatsapp_link')
            author = request.POST.get('author')
            
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            h1tag = request.POST.get('h1tag')

        package = WebsitePackages(
            title=title,
            category=category,
            description=description,
            top_attraction=top_attraction,
            why_visit=why_visit,
            package_highlights=package_highlights,
            facebook_link=facebook_link,
            instagram_link=instagram_link,
            whatsapp_link=whatsapp_link,
            author=author,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            h1tag=h1tag,
        )
        package.save()
        return JsonResponse({'status': "Success"})

class webPackageList(ListView):
    model = WebsitePackages
    template_name = "website/view_webpackages.html"  