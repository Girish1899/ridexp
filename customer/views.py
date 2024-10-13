from datetime import date, datetime,time
from decimal import Decimal
import random
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
from superadmin.models import RideDetails,Customer,Driver,Vehicle,Ridetype,Category,Brand,Model,Pricing
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login ,logout
# views.py
import json
from django.http import JsonResponse
# from .models import Attendance, Profile, User
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
import requests 
from rest_framework.response import Response
from django.core.cache import cache


# Create your views here.

class regcustomer(TemplateView):
    template_name = "customer/register.html"

    def post(self, request):
        last_cust = Customer.objects.all().order_by('-customer_id').first()

        if last_cust:
            last_company_format = int(last_cust.company_format.replace('CUST', ''))
            next_company_format = f'CUST{last_company_format + 1:02}'
        else:
            next_company_format = 'CUST01'

        customer_name = request.POST['customer_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        status = request.POST['status']

        cust = Customer(
            customer_name=customer_name,
            phone_number=phone_number,
            email=email,
            password=password,
            address=address,
            status=status,
            company_format=next_company_format,  # Corrected here
        )
        cust.save()

        # Return success response
        return JsonResponse({'status': "Success"})

def check_phonenumber(request):
    phone_number = request.GET.get('phone_number', None)
    ph = Customer.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)

# class custlogin(TemplateView):
#     template_name = "customer/custlogin.html"

#     def post(self, request, *args, **kwargs):
#         if request.method == "POST":
#             phone_number = request.POST.get('phone_number')
#             password = request.POST.get('password')

#             print("Received phone number:", phone_number) 
#             print("Received password:", password) 

#             try:
#                 customer = Customer.objects.get(phone_number=phone_number)
                
#                 if customer.password == password:  # Dummy password check
#                     # Redirect to booking page on successful login
#                     return JsonResponse({'success': True, 'redirect_url': 'customer_addbooking      '})
#                 else:
#                     return JsonResponse({'success': False, 'message': 'Invalid password.'})
#             except Customer.DoesNotExist:
#                 return JsonResponse({'success': False, 'message': 'Phone number not found. Please register.'})
        
#         return JsonResponse({'success': False, 'message': 'Invalid request method.'})

class custlogin(TemplateView):
    template_name = "customer/custlogin.html"

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        print("Received phone number:", phone_number) 
        print("Received password:", password)


        try:
            customer = Customer.objects.get(phone_number=phone_number)
            # Store customer ID in session after successful login
            request.session['customer_id'] = customer.customer_id

            if customer.password == password:  # Dummy password check
#            Redirect to booking page on successful login
                return JsonResponse({'success': True, 'redirect_url': 'customer_addbooking      '})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid password.'})

        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Phone number not found. Please register.'})

def cuslogout_view(request):
    logout(request)
    request.session.flush()
    return redirect('customer_login')


def customer_profile(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('customer_login')  # Redirect to login if customer is not logged in

    # Retrieve the customer's details
    customer = get_object_or_404(Customer, customer_id=customer_id)
    return render(request, 'customer/cusprofile.html', {'customer': customer})

class previous(ListView):
    model = RideDetails
    template_name = "customer/previous.html"

    def get_queryset(self):
        # Get the currently logged-in customer from the session or request
        customer = self.request.session.get('customer_id')  # Adjust as per how you store customer information in session
        
        # If customer is not found in session, return an empty queryset
        if not customer:
            return RideDetails.objects.none()

        # Filter for both completed and cancelled bookings for the logged-in customer
        return RideDetails.objects.filter(
            ride_status__in=['completedbookings', 'cancelledbookings'],
            customer=customer
        )

class current(ListView):
    model = RideDetails
    template_name = "customer/current.html"

    def get_queryset(self):
        # Get the currently logged-in customer from the session or request
        customer = self.request.session.get('customer_id')  # Adjust as per how you store customer information in session
        
        # If customer is not found in session, return an empty queryset
        if not customer:
            return RideDetails.objects.none()

        # Filter for both completed and cancelled bookings for the logged-in customer
        return RideDetails.objects.filter(
            ride_status__in=['assignlaterbookings', 'advancebookings','ongoingbookings','assignbookings','currentbookings'],
            customer=customer
        )
        
def cancel_ride(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comments = data.get('comments')
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)
            ride.comments = comments
            ride.ride_status = 'cancelledbookings'
            ride.save()

            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'essage': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'essage': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)

class Addbookings(TemplateView):
    template_name = "customer/addbooking.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ridetypelist'] = Ridetype.objects.all()
        context['catlist'] = Category.objects.filter(category_status='active')
        return context
    
    def post(self, request):
        try:
            last_ride = RideDetails.objects.all().order_by('-ride_id').first()
            if last_ride:
                try:
                    last_company_format = int(last_ride.company_format.replace('RID', ''))
                except ValueError:
                    last_company_format = last_ride.ride_id
                next_company_format = f'RID{last_company_format + 1:02}'
            else:
                next_company_format = 'RID01'

            ride_type_id = request.POST['ridetype']
            source = request.POST.get('source')
            destination = request.POST.get('destination')
            pickup_date = request.POST.get('pickup_date')
            pickup_time = request.POST.get('pickup_time')
            category = request.POST.get('category')
            total_fare = request.POST.get('total_fare')
            customer_notes = request.POST['customer_notes']
            car_type = request.POST.get('car_type', '').strip()  # Fetch car_type (AC or Non-AC)
            slots = determine_time_slot(pickup_time)
            ride_status = request.POST['ride_status']
            # Split category_value to get the category name
            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            category_name = category.split('|')[0]
            car_type_name = category.split('|')[1]
            category_instance = Category.objects.get(category_name=category_name)

            # Retrieve pricing instance
            # trip_type = request.POST.get('trip_type', '').strip()
            # print('trip_type from request:', trip_type)  # This should print the trip_type value

            try:
                if ridetype.name.lower() == 'local':
                    pricing_instance = Pricing.objects.get(
                        category=category_instance,
                        car_type=car_type_name,
                        ridetype=ridetype,
                        slots=slots,
                    )
                    
                else:
                # Exclude triptype filter for local rides
                    trip_type = request.POST.get('trip_type', '').strip()
                    print('trip_type from request:', trip_type)  # This should print the trip_type value
                    pricing_instance = Pricing.objects.get(
                        category=category_instance,
                        car_type=car_type_name,
                        ridetype=ridetype,
                        slots=slots,
                        trip_type=trip_type,  
                    )

                    print('after request trip type',trip_type)

            except Pricing.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Pricing information for the selected category, car type, and ride type does not exist."})

            print(f"Saving ride with details: {ridetype}, {category_instance}")

            # Retrieve customer from session
            customer_id = request.session.get('customer_id')  
            if not customer_id:
                return JsonResponse({'status': 'Error', 'message': 'Customer is not logged in.'})
            
            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return JsonResponse({'status': 'Error', 'message': f'Customer with ID {customer_id} does not exist.'})


            # Determine ride status based on pickup date
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            print(f'ridetype: {ridetype}')
            print(f'source: {source}')
            print(f'destination: {destination}')
            print(f'pickup_date: {pickup_date}')
            print(f'pickup_time: {pickup_time}')
            print(f'category: {category}')
            print(f'total_fare: {total_fare}')
            print(f'customer_notes: {customer_notes}')

            ride_details = RideDetails(
                company_format=next_company_format,
                ridetype=ridetype,
                customer=customer,
                category=category_instance,
                source=source,
                destination=destination,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                total_fare=total_fare,
                customer_notes=customer_notes,
                ride_status=ride_status,
                pricing = pricing_instance,  # Set the Pricing instance

            )
            ride_details.save()
            print("Ride details saved successfully.")
            
            whatsapp = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                "campaignName": "booking confirmation",
                "destination": customer.phone_number,
                "userName": "Ridexpress",
                "templateParams": [
                        customer.customer_name,
                        next_company_format,
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
            response = requests.post(gateway_url, json=whatsapp)

            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print(f"Failed to send message: {response.status_code}")
                print(response.text)

            return JsonResponse({'status': 'Success', 'message': 'Ride details added successfully'})

        except IntegrityError as e:
            print(f"IntegrityError occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': 'Data integrity error occurred.'})

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)})

def determine_time_slot(pickup_time):
    # Determine the time slot based on pickup_time_str
    pickup_time = datetime.strptime(pickup_time, '%H:%M').time()
    if time(0, 0) <= pickup_time < time(6, 0):
        return '12AM - 6AM'
    elif time(6, 0) <= pickup_time < time(12, 0):
        return '6AM - 12PM'
    elif time(12, 0) <= pickup_time < time(18, 0):
        return '12PM - 6PM'
    else:
        return '6PM - 12AM'


###################################################        #

class SendOtp(View):
    def post(self, request):
        # Retrieve customer_id from session
        customer_id = request.session.get('customer_id')

        if not customer_id:
            return JsonResponse({'status': 'Error', 'message': 'Customer is not logged in.'})

        try:
            # Fetch the customer's phone number using the customer_id
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': f'Customer with ID {customer_id} does not exist.'})

        phone_number = customer.phone_number
        customer_name = customer.customer_name
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
        customer_id = request.session.get('customer_id')

        if not customer_id:
            return JsonResponse({'status': 'Error', 'message': 'Customer is not logged in.'})

        try:
            # Fetch the customer's phone number using the customer_id
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': f'Customer with ID {customer_id} does not exist.'})

        phone_number = customer.phone_number
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

class customerGetRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse
        from datetime import datetime
        print(request.POST)

        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        drop_date = request.POST.get('drop_date')
        drop_time = request.POST.get('drop_time')
        time_slot = request.POST['time_slot']
        ridetype_id = request.POST['ridetype']  
        trip_type = request.POST.get('trip_type')  
        toll_option = request.POST.get('toll_option') 

        if not source or not destination or not pickup_date or not pickup_time or not time_slot:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        gmaps = googlemaps.Client(key=api_key)

        result = gmaps.distance_matrix(
            origins=[source],
            destinations=[destination],
            mode="driving",
            departure_time=datetime.now()
        )
        distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000  
        print(f"Distance calculated: {distance} km")

        costs = {}

        # Fetch the ridetype instance
        ride_type_instance = Ridetype.objects.filter(ridetype_id=ridetype_id).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        print(f"Ride Type: {ride_type_instance.name}, Trip Type: {trip_type}, Toll Option: {toll_option}")

        # Call appropriate calculation function based on trip_type
        if ride_type_instance.name == 'outstation':
            pricing_details = self.get_outstation_pricing(time_slot, ridetype_id, trip_type)
            if trip_type == 'round_trip':
                result = self.calculate_outstation_roundtrip(request, pricing_details, distance)
            else:
                result = self.calculate_outstation_oneway(pricing_details, distance)
        elif ride_type_instance.name == 'local':
            pricing_details = self.get_local_pricing(time_slot, ridetype_id)
            result = self.calculate_local(pricing_details, distance)
        elif ride_type_instance.name == 'airport':
            pricing_details = self.get_airport_pricing(time_slot, ridetype_id,trip_type)
            result = self.calculate_airport(pricing_details, distance, toll_option)
        else:
            return JsonResponse({'error': 'Invalid ridetype or trip_type'}, status=400)

        return JsonResponse({'costs': result})

    def get_local_pricing(self, time_slot, ridetype_id):
        """Fetch pricing for local rides."""
        print(f"Fetching pricing for time slot: {time_slot}, ridetype_id: {ridetype_id}")
        return Pricing.objects.select_related('category').filter(
            slots=time_slot, ridetype_id=ridetype_id
        )

    def get_airport_pricing(self, time_slot, ridetype_id, trip_type):
        """Fetch pricing for airport rides with or without toll."""
        # You can modify this to include toll_option-based pricing if needed
        return Pricing.objects.select_related('category').filter(
            slots=time_slot, ridetype_id=ridetype_id,trip_type=trip_type
        )

    def get_outstation_pricing(self, time_slot, ridetype_id, trip_type):
        """Fetch pricing for outstation rides, considering trip type."""
        return Pricing.objects.select_related('category').filter(
            slots=time_slot, ridetype_id=ridetype_id, trip_type=trip_type
        )

    def calculate_local(self, pricing_details, distance):
        """Calculate pricing for local rides."""    
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            toll_price = Decimal(str(price.toll_price))

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price,toll_price)
        
        return pricing_dict

    def calculate_airport(self, pricing_details, distance, toll_option):
        """Calculate pricing for airport rides with toll and no toll options."""
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            toll_price = Decimal(str(price.toll_price)) if toll_option == 'add_toll' else Decimal(0)
            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price, toll_price)

        return pricing_dict

    def calculate_outstation_oneway(self, pricing_details, distance):
        """Calculate pricing for outstation one-way rides."""
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            toll_price = Decimal(str(price.toll_price))    

            pricing_dict[category_name][car_type] = self.calculate_cost(distance, price,toll_price)

        return pricing_dict

    def calculate_outstation_roundtrip(self, request, pricing_details, distance):
        """Calculate pricing for outstation roundtrip rides based on pickup and drop date."""
        from datetime import datetime

        # Parse the pickup and drop date/time from the request
        pickup_date_str = request.POST.get('pickup_date')
        pickup_time_str = request.POST.get('pickup_time')
        drop_date_str = request.POST.get('drop_date')
        drop_time_str = request.POST.get('drop_time')

        # Ensure that pickup and drop date/time are provided
        if not pickup_date_str or not pickup_time_str:
            return {"error": "Pickup date and time must be provided."}
        if not drop_date_str or not drop_time_str:
            return {"error": "Drop date and time must be provided."}

        # Combine pickup date and time for parsing
        pickup_datetime_str = f"{pickup_date_str} {pickup_time_str}"
        
        # Combine drop date and time for parsing
        drop_datetime_str = f"{drop_date_str} {drop_time_str}"

        try:
            # Convert to datetime objects
            pickup_datetime = datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M")
            drop_datetime = datetime.strptime(drop_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError as e:
            # Return a meaningful error message in case of parsing issues
            return {"error": f"Invalid date/time format: {str(e)}"}

        # Calculate the number of days based on pickup and drop dates
        num_days = self.calculate_days(pickup_datetime, drop_datetime)

        # Cap the distance based on the number of days (250 km per day)
        daily_km_cap = 250 * num_days
        applicable_distance = max(distance, daily_km_cap)

        # Calculate the pricing for each vehicle category and type
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()
            toll_price = Decimal(str(price.toll_price))
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            # Calculate the cost for the applicable distance and number of days
            pricing_dict[category_name][car_type] = self.calculate_cost(applicable_distance, price,toll_price=toll_price, num_days=num_days)

        return pricing_dict

    def calculate_days(self, pickup_datetime, drop_datetime):
        """Calculate the number of days for a round trip."""
        if drop_datetime.date() > pickup_datetime.date():
            num_days = 1
            end_of_pickup_day = pickup_datetime.replace(hour=23, minute=59, second=59)

            if drop_datetime > end_of_pickup_day:
                num_days += (drop_datetime.date() - pickup_datetime.date()).days
        else:
            num_days = 1

        print(f"Total days for the trip: {num_days}")

        return num_days

    def calculate_cost(self, distance, price, toll_price=Decimal(0), num_days=1):
        """Helper method to calculate cost based on distance and pricing details."""
        from decimal import Decimal

        price_per_km_decimal = Decimal(str(price.price_per_km))
        permit_decimal = Decimal(str(price.permit))
        toll_price_decimal = Decimal(str(toll_price))

        driver_beta_decimal = Decimal(str(price.driver_beta)) * Decimal(str(num_days))

        # Calculate total cost

        total_cost = (Decimal(distance) * price_per_km_decimal) + permit_decimal + toll_price_decimal + driver_beta_decimal
        total_cost = round(total_cost, 0)

        return {
            'distance_km': distance,
            'cost': total_cost,
            'permit': permit_decimal,
            'toll': toll_price_decimal,
            'beta': driver_beta_decimal,
            'category': price.category.category_name,
        }    