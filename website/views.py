# website/views.py
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login as auth_login ,logout
import requests
from django.urls import reverse
from superadmin.models import Brand, Category, Customer, Model, Pricing, Profile, RideDetails, Ridetype

from datetime import date, datetime, time
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from django.views.decorators.csrf import csrf_exempt


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

def about(request):
    return render(request, 'website/about.html')

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

    if not source or not destination or not pickup_date:
        return HttpResponse("All fields are required.", status=400)

    # Construct the URL for the search based on ridetype
    if ridetype == 'airport':
        search_url = reverse('airportcabs_list')
    elif ridetype == 'local':
        search_url = reverse('localcabs_list')
    elif ridetype == 'localpackage':
        search_url = reverse('cabs_list')
    elif ridetype == 'outstation':
        search_url = reverse('outstationcabs_list')
    else:
        return HttpResponse("Invalid ride type.", status=400)

    # Construct the final URL with query parameters
    search_url += f"?location1={source}&location2={destination}&pickup_date={pickup_date}&pickup_time={pickup_time}&ridetype={ridetype}"

    # Redirect to the constructed URL
    return redirect(search_url)

def airportcabs_list(request):
    # Retrieve query parameters from the URL
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '')  # Capture car_type
    ridetype = 'airport'

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

def localcabs_list(request):
    # Retrieve query parameters from the URL
    source = request.GET.get('source', '')
    destination = request.GET.get('destination', '')
    pickup_date = request.GET.get('pickup_date', '')
    pickup_time = request.GET.get('pickup_time', '')
    car_type = request.GET.get('car_type', '')  # Capture car_type
    ridetype = 'local'

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


    return render(request, 'website/localcabs_list.html', context)


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

    # Debugging prints
    print("Price received in view:", price)
    print("car_type received in view:", car_type)
    print("----------", ridetype)

    # Fetch matching pricing instances
    pricing_instances = Pricing.objects.filter(
        category__category_name=category,
        ridetype__name=ridetype,
        car_type=car_type,
        slots=slots  # Pass time_slot to the template

    )

    # Handle cases where multiple instances are found
    if pricing_instances.count() == 1:
        pricing_instance = pricing_instances.first()
    else:
        # Handle the case where there are multiple or no instances
        # For example, choose the first instance or handle as needed
        pricing_instance = pricing_instances.first() if pricing_instances.exists() else None
        print("Multiple or no Pricing instances found.")

    return render(request, 'website/booking_list.html', {
        'source': source,
        'destination': destination,
        'pickup_date': pickup_date,
        'pickup_time': pickup_time,
        'category': category,
        'ridetype': ridetype,
        'car_type': car_type,
        'price': price,
        'pricing': pricing_instance,  # Associate the correct Pricing instance
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

def contact(request):
    return render(request, 'website/contact.html')

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
            # ridetype = request.POST['ridetype']
            category = request.POST['category']
            source = request.POST['source']
            destination = request.POST['destination']
            customer_phone_number = request.POST['phone_number']
            address = request.POST['address']
            customer_name = request.POST['customer_name']
            customer_email = request.POST['email']
            customer_notes = request.POST['customer_notes']
            total_fare=request.POST['total_fare']
            car_type = request.POST.get('car_type', '').strip()  # Fetch car_type (AC or Non-AC)
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
                    slots=slots

                )
            except Pricing.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Pricing information for the selected category, car type, and ride type does not exist."})

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
                        status="Active",
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
                ride_details.assigned_by=request.user
                ride_details.created_by=request.user
                ride_details.updated_by=request.user
                ride_details.pricing = pricing_instance  # Set the Pricing instance

                ride_details.save()
                print("source ^^^: ",request.POST['source'] )
                print("source ^^^: ", request.POST['destination'])
                whatsapp = {
                    "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ZWRiZWZhNTA0NzhkMjc0MGM0OWI2MyIsIm5hbWUiOiJEZWVwYW0gVGF4aSIsImFwcE5hbWUiOiJBaVNlbnN5IiwiY2xpZW50SWQiOiI2NGVkYmVmYTUwNDc4ZDI3NDBjNDliNWUiLCJhY3RpdmVQbGFuIjoiQkFTSUNfTU9OVEhMWSIsImlhdCI6MTY5MzMwMjUyMn0.-oNpicqPahvPSuR-hI9F7i3l2YMZVaPs5Z7Hqk0JjyU",
                    "campaignName": "newbooking_confirmation_local",
                    "destination": customer_phone_number,
                    "userName": "Deepam Taxi",
                    "templateParams": [
                        customer_name,
                        "WB" + time_str,
                        date.today(),
                        datetime.now().strftime('%H:%M'),
                        request.POST['source'],
                        request.POST['destination'],
                        pickup_date +'  ' +pickup_time,
                        total_fare
                    ],
                    "source": "new-landing-page form",
                    "media": {},
                    "buttons": [],
                    "carouselCards": [],
                    "location": {}
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