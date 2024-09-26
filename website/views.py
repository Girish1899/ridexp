# website/views.py
import random
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login ,logout
import requests
from django.urls import reverse
from superadmin.models import Brand, Category, Color,Enquiry, CommissionType, ContactUs, Customer, Model, Pricing, Profile, RideDetails, Ridetype, Transmission, Vehicle,VehicleOwner, VehicleType
from datetime import date, datetime, time
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.core.cache import cache



# Define the time slots
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
        
    # last_ride = RideDetails.objects.all().order_by('-ride_id').first()
    # if last_ride:
    #     last_company_format = last_ride.company_format.replace('RID', '')
    #     next_company_format = f'RID{str(last_company_format) + 1:02}'
    # else:
    #     next_company_format = 'RID01'
    # context={
    #     'customerlist':Customer.objects.all(),
    #     'ridetypelist': Ridetype.objects.all(),
    #     'ridetypelist':Ridetype.objects.all(),
    #     'catlist':Category.objects.all(),
    #     'blist': Brand.objects.all(),
    #     'modellist' : Model.objects.all(),
    #     'next_company_format':next_company_format
    # }
    context = None
    
    return render(request, 'website/main.html',context)

def our_rides(request):
    context = None
    return render(request, 'website/our_rides.html',context)


def packages(request):
    context = None
    return render(request, 'website/taxi.html',context)

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


 # airport ####################3

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

###############################################################

# local blogs ###############################
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


######################################
def about(request):
    return render(request, 'website/about.html')

@csrf_exempt 
def save_enquiry(request):
    print("Received request:", request.method)  # Log the request method
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
            print("Error saving enquiry:", e)  # Log the error
            return JsonResponse({'error': 'Failed to save enquiry.'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


# def cabs_list(request):
#     # Retrieve query parameters from the URL
#     source = request.GET.get('source', '')
#     destination = request.GET.get('destination', '')
#     pickup_date = request.GET.get('pickup_date', '')
#     pickup_time = request.GET.get('pickup_time', '')

#     # Query the Category table to get all active categories
#     categories = Category.objects.filter(category_status='active')

#     # Prepare context with the retrieved values and categories
#     context = {
#         'source': source,
#         'destination': destination,
#         'pickup_date': pickup_date,
#         'pickup_time': pickup_time,
#         'categories': categories,  # Pass the categories to the template
#     }

#     # Render the template with the context data
#     return render(request, 'website/cabs_list.html', context)

def search_url(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    pickup_date = request.GET.get('pickup_date')
    pickup_time = request.GET.get('pickup_time')
    ridetype = request.GET.get('ridetype')
    trip_type = request.GET.get('trip_type')  # Get the trip type for outstation

    if not source or not destination or not pickup_date:
        return HttpResponse("All fields are required.", status=400)

    if ridetype == 'airport':
        if trip_type == 'one_way':
            search_url = reverse('airportcabs_list')  # Redirect to cabs_list for one way trip
        elif trip_type == 'round_trip':
            search_url = reverse('airport_roundtrip')  # Redirect to airport_roundtrip for round trip
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
    # Retrieve query parameters from the URL
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    # Initialize an empty dictionary to hold pricing information
    pricing_dict = {}

    if ride_type_instance:
        # Fetch all AC and non-AC pricing related to the 'airport' ride type
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        # Populate the dictionary with AC pricing
        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        # Populate the dictionary with non-AC pricing
        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    # Print pricing data for debugging
    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type,  # Pass car_type to the context
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }

    return render(request, 'website/cabs_list.html', context)

def airport_roundtrip(request):
    # Retrieve query parameters from the URL
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '') 
    ridetype = request.GET.get('ridetype', '')  

    ride_type_instance = Ridetype.objects.filter(name=ridetype).first()

    # Initialize an empty dictionary to hold pricing information
    pricing_dict = {}

    if ride_type_instance:
        # Fetch all AC and non-AC pricing related to the 'airport' ride type
        pricing_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='ac').select_related('category')
        pricing_non_ac = Pricing.objects.filter(ridetype=ride_type_instance, car_type='non_ac').select_related('category')

        # Populate the dictionary with AC pricing
        for price in pricing_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['ac'] = price

        # Populate the dictionary with non-AC pricing
        for price in pricing_non_ac:
            category_name = price.category.category_name.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {'ac': None, 'non_ac': None}
            pricing_dict[category_name]['non_ac'] = price

    # Print pricing data for debugging
    print("Filtered Pricing QuerySet:", pricing_dict)

    context = {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'car_type': car_type,  # Pass car_type to the context
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
        'car_type': car_type,  # Pass car_type to the context
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/localcabs_list.html', context)

# one way

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
        'car_type': car_type,  # Pass car_type to the context
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/outstation_oneway.html', context)

# roundtrip outstation

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
        'car_type': car_type,  # Pass car_type to the context
        'pricing_dict': pricing_dict,
        'ridetype':ridetype,
    }


    return render(request, 'website/outstation_roundtrip.html', context)


def booking_list(request):
    # Get parameters from GET request
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    pickup_date = request.GET.get('pickup_date')
    pickup_time = request.GET.get('pickup_time')
    category = request.GET.get('category')
    ridetype = request.GET.get('ridetype')
    car_type = request.GET.get('car_type', '')  # Capture the car_type from the request
    price = request.GET.get('price')
    slots = request.GET.get('time_slot')
    trip_type = request.GET.get('trip_type')
    drop_date = request.GET.get('drop_date') 
    drop_time = request.GET.get('drop_time') 

    # Debugging prints
    print("Price received in view:", price)
    print("car_type received in view:", car_type)
    print("----------", ridetype)

    # Fetch matching pricing instances
    pricing_instances = Pricing.objects.filter(
        category__category_name=category,
        ridetype__name=ridetype,
        car_type=car_type,
        slots=slots,  # Pass time_slot to the template
        trip_type=trip_type
    )

    # Handle cases where multiple instances are found
    if pricing_instances.count() == 1:
        pricing_instance = pricing_instances.first()
    elif pricing_instances.count() > 1:
        # Log warning and choose the first instance (or apply more specific logic if needed)
        print("Multiple Pricing instances found. Choosing the first one.")
        pricing_instance = pricing_instances.first()  # Adjust this logic as needed
    else:
        # Handle the case where no instances are found
        pricing_instance = None
        print("No Pricing instances found.")
    
    # Pass the results to the template
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
    # if last_ride:
    #     last_company_format = int(last_ride.company_format.replace('RID', ''))
    #     next_company_format = f'RID{last_company_format + 1:02}'
    # else:
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

# def contact(request):
#     return render(request, 'website/contact.html')

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
    return render(request, 'website/blog.html')


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
                    # Handle superuser login without profile
                    redirect_url = '/superadmin/index'
                    request.session['user_type'] = "Superadmin"
                    request.session['user_id'] = user.id
                else:
                    return JsonResponse({'success': False, 'message': 'Profile does not exist for this user'})
            else:
                # Handle non-superuser login
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

            # Convert date and time
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            pickup_time = datetime.strptime(pickup_time_str, '%H:%M').strftime('%H:%M:%S')
            

            # Get current system time
            current_time = datetime.now()


            # Format the time as a string with hours, minutes, and seconds
            time_str = current_time.strftime('%H%M%S')
            company_format = "WB" + time_str
            bookings_from = "website"
            # ridetype = request.POST['ridetype']
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
            # drop_date=request.POST['drop_date']
            # drop_time=request.POST['drop_time']
            car_type = request.POST.get('car_type', '').strip()  # Fetch car_type (AC or Non-AC)
            trip_type = request.POST.get('trip_type', '').strip()  # Fetch car_type (AC or Non-AC)
            ridetype_name = request.POST.get('ridetype', '').strip()
            slots = determine_time_slot(pickup_time_str)  # Function to determine the slot based on pickup_time



            if not ridetype_name:
                return JsonResponse({"status": "Error", "message": "Ride type is required."})

            try:
                ridetype_instance = Ridetype.objects.get(name=ridetype_name)
            except Ridetype.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Ride type does not exist."})


            try:
                category_instance = Category.objects.get(category_name=category)
            except Category.DoesNotExist:
                # Handle the case where the Ridetype does not exist
                return JsonResponse({"status": "Error", "message": "Category does not exist."})
            
            # Updated logic to include ridetype in pricing instance retrieval
            try:
                pricing_instance = Pricing.objects.get(
                    category=category_instance,
                    car_type=car_type,
                    ridetype=ridetype_instance,  # Include ridetype in the query
                    slots=slots,
                    trip_type=trip_type,

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

            # Ensure objects exist in database before saving
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

            # Determine ride status based on pickup date
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
                ride_details.assigned_by=request.user
                ride_details.created_by=request.user
                ride_details.updated_by=request.user
                ride_details.pricing = pricing_instance 
                ride_details.drop_date = drop_date 
                ride_details.drop_time = drop_time 

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
                # Send the POST request
                gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
                try:
                    response = requests.post(gateway_url, data=whatsapp)
                    if response.status_code == 200:
                        print("Message sent successfully")
                    else:
                        print(f"Failed to send message. Status code: {response.status_code}")
                        print(response.text)  # Print response body for debugging
                except requests.RequestException as e:
                    print(f"Error sending message: {e}")
            except IntegrityError as e:
                # Log the specific IntegrityError
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
    # Determine the time slot based on pickup_time_str
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
            'image': owner.image.url if owner.image else None,  # Get URL for image
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
        
        # Fetching data for dropdowns
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

        # Ensure objects exist in database before saving
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
        return JsonResponse({'status': "Success"})

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
        print("Backend received toll option: ", toll_option)  # Debugging

        # Initialize the Google Maps client with your API key
        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        # Request directions via driving mode
        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        # Extract the distance in kilometers
        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print("Distance calculated: ", distance)  # Debugging

        # Initialize the costs dictionary
        costs = {}

        # Fetch the ridetype instance
        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        # Fetch all pricing details filtered by the selected time slot and ridetype
        pricing_details = Pricing.objects.select_related('category').filter(slots=time_slot, ridetype=ride_type_instance,trip_type=trip_type)

        # Organize pricing data by category and car type
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            toll_price = Decimal(str(price.toll_price)) if toll_option == 'add_toll' else Decimal(0)
            print(f"Toll option: {toll_option}, Toll price applied: {toll_price}")  # Check if this correctly shows 0 for no_toll

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price, toll_price)

        return JsonResponse({'costs': pricing_dict})

    def calculate_cost(self, distance, price, toll_price):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        # Convert all fields to Decimal before operations
        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        driver_beta_decimal = Decimal(str(price.driver_beta))

        temp_cost = Decimal(distance) * price_per_km_decimal
        temp_cost += permit_decimal + toll_price + driver_beta_decimal
        category_cost = round(temp_cost, 0)

        print(f"Calculated cost: {category_cost}, Permit: {permit_decimal}, Toll: {toll_price}, Beta: {driver_beta_decimal}")  # Debugging

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
        ridetype = request.POST['ridetype']  # Ensure the ridetype is fetched correctly

        # Initialize the Google Maps client with your API key
        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        # Request directions via driving mode
        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )

        # Extract the distance in kilometers
        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
        print("Distance calculated:", distance)

        # Initialize the costs dictionary
        costs = {}

        # Fetch the ridetype instance
        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        # Fetch all pricing details filtered by the selected time slot and ridetype
        pricing_details = Pricing.objects.select_related('category').filter(slots=time_slot, ridetype=ride_type_instance)

        # Debugging statement
        print("Fetched Pricing Details: ", pricing_details)

        # Organize pricing data by category and car type
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price)

        # Debugging statement to confirm pricing data
        print("Pricing Dict after calculation: ", pricing_dict)
        return JsonResponse({'costs': pricing_dict})
    
    def calculate_cost(self, distance, price):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        # Convert all fields to Decimal before operations
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
    

# one way outstation

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
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

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


# round trip

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

        daily_km_cap = 250 * num_days
        print(f"Total allowed km for {num_days} day(s): {daily_km_cap} km")

        applicable_distance = max(distance, daily_km_cap)
        print(f"Applicable distance based on days: {applicable_distance} km")

        ride_type_instance = Ridetype.objects.filter(name=ridetype).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        pricing_details = Pricing.objects.select_related('category').filter(
            slots=time_slot, ridetype=ride_type_instance, trip_type=trip_type
        )

        print("Fetched Pricing Details: ", pricing_details)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

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
    

# otp 

# otp_store = {}

# def send_otp(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         customer_name = request.POST.get('customer_name')

#         otp = random.randint(100000, 999999)
#         otp_store[phone_number] = otp  # Store the OTP

#         whatsapp = {
#             "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
#             "campaignName": "booking confirmation",
#             "destination": phone_number,
#             "userName": "Ridexpress",
#             "templateParams": [str(otp)],
#             "source": "new-landing-page form",
#         }
#         gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
#         try:
#             response = requests.post(gateway_url, data=whatsapp)
#             if response.status_code == 200:
#                 return JsonResponse({'status': 'Success', 'message': 'OTP sent successfully'})
#             else:
#                 return JsonResponse({'status': 'Error', 'message': 'Failed to send OTP'})
#         except requests.RequestException as e:
#             return JsonResponse({'status': 'Error', 'message': str(e)})

# def verify_otp(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         entered_otp = request.POST.get('otp')

#         if phone_number in otp_store and str(otp_store[phone_number]) == entered_otp:
#             del otp_store[phone_number]  # Clear OTP after verification
#             return JsonResponse({'status': 'Success', 'message': 'OTP verified successfully'})
#         else:
#             return JsonResponse({'status': 'Error', 'message': 'Incorrect OTP'})


class SendOtp(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        customer_name = request.POST.get('customer_name')
        otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP

        # Store OTP in cache with a 5-minute expiration
        cache.set(f'otp_{phone_number}', otp, timeout=300)

        # WhatsApp API payload for OTP
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
                            "text": otp  # Send OTP in the message
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

        # Retrieve the OTP from the cache
        cached_otp = cache.get(f'otp_{phone_number}')

        if cached_otp and cached_otp == otp:
            # OTP matches, remove it from cache
            cache.delete(f'otp_{phone_number}')
            return JsonResponse({'status': 'Success', 'message': 'OTP verified successfully.'})
        else:
            return JsonResponse({'status': 'Error', 'message': 'Incorrect OTP.'})