from datetime import date
from decimal import Decimal
import json
from django.shortcuts import render
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View
from rest_framework.response import Response
from rest_framework import status
from superadmin.models import  Blogs, Brand, Category, Enquiry, Model, PackageCategories, PackageCategoriesHistory, Profile, RideDetails,Pricing, RideDetailsHistory,User,Customer,Driver,Ridetype,Vehicle, WebsitePackages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.db import IntegrityError
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
import random
import requests
from datetime import date, datetime,time
from datetime import date, timedelta
from django.utils import timezone


@login_required(login_url='login')
def index(request):
    cust_count = Customer.objects.count()
    driver_count = Driver.objects.count()
    booking_count = RideDetails.objects.count()
    vehicle_count = Vehicle.objects.count()

    context = {
        'cust_count': cust_count,
        'driver_count': driver_count,
        'booking_count': booking_count,
        'vehicle_count': vehicle_count,
    }
    return render(request,'telecaller/index.html',context)


def call_history_view(request, ride_id):
    try:
        ride = RideDetails.objects.get(ride_id=ride_id) 
    except RideDetails.DoesNotExist:
        ride = None

    context = {
        'ride_id': ride_id,
        'ride': ride,  
    }
    return render(request, 'telecaller/callhistory.html', context)



def check_phonenumber(request):
    phone_number = request.GET.get('phone_number', None)
    ph = Customer.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)


def check_email(request):
    email = request.GET.get('email', None)
    em = Customer.objects.filter(email=email)
    data = {
        'exists': em.count() > 0
    }
    return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addcustomer(TemplateView):
    template_name = "telecaller/add_customer.html"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            last_cust = Customer.objects.all().order_by('-customer_id').first()
            if last_cust:
                last_company_format = int(last_cust.company_format.replace('CUST', ''))
                next_company_format = f'CUST{last_company_format + 1:02}'
            else:
                next_company_format = 'CUST01'
            context['next_company_format'] = next_company_format
            return context

    def post(self, request):
        customer_name = request.POST['customer_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        status = request.POST['status']
        company_format = request.POST.get('company_format', '')

        cust = Customer(
            customer_name=customer_name,
            phone_number=phone_number,
            email=email,
            address=address,
            status=status,
            company_format=company_format,
            created_by=request.user,
            updated_by=request.user
        )
        cust.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = "telecaller/view_customer.html"


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditCustomer(TemplateView):
    template_name = 'telecaller/edit_customer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['customer_id'] = self.kwargs['id']
            customerlist = Customer.objects.filter(customer_id=context['customer_id'])
        except:
            customerlist = Customer.objects.filter(customer_id=context['customer_id'])
            
        context['customerlist']= list(customerlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateCustomer(APIView):  
    def post(self, request):
        customer_id = request.POST['customer_id']
        customer_name = request.POST['customer_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        status = request.POST['status']
        company_format = request.POST['company_format']

        cust = Customer.objects.get(customer_id=customer_id)
        cust.customer_name = customer_name
        cust.phone_number = phone_number
        cust.email = email
        cust.address = address
        cust.status = status
        cust.company_format = company_format
        cust.updated_by = request.user
        cust.save()

        return JsonResponse({'success': True}, status=200)


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

        ride_type_instance = Ridetype.objects.filter(ridetype_id=ridetype_id).first()
        if not ride_type_instance:
            return JsonResponse({'error': 'Invalid ridetype'}, status=400)

        print(f"Ride Type: {ride_type_instance.name}, Trip Type: {trip_type}, Toll Option: {toll_option}")

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
            car_type = price.car_type.lower() 

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
        from decimal import Decimal

        pickup_date_str = request.POST.get('pickup_date')
        pickup_time_str = request.POST.get('pickup_time')
        drop_date_str = request.POST.get('drop_date')
        drop_time_str = request.POST.get('drop_time')

        if not pickup_date_str or not pickup_time_str:
            return {"error": "Pickup date and time must be provided."}
        if not drop_date_str or not drop_time_str:
            return {"error": "Drop date and time must be provided."}

        pickup_datetime_str = f"{pickup_date_str} {pickup_time_str}"
        drop_datetime_str = f"{drop_date_str} {drop_time_str}"

        try:
            pickup_datetime = datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M")
            drop_datetime = datetime.strptime(drop_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError as e:
            return {"error": f"Invalid date/time format: {str(e)}"}

        num_days = self.calculate_days(pickup_datetime, drop_datetime)

        pricing_dict = {}

        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()
            toll_price = Decimal(str(price.toll_price))

            if 'mini' in category_name.lower() or 'sedan' in category_name.lower():
                daily_km_cap = 250 * num_days
            else:
                daily_km_cap = 300 * num_days

            print(f"Total allowed km for {num_days} day(s) for {category_name}: {daily_km_cap} km")

            applicable_distance = max(distance, daily_km_cap)
            print(f"Applicable distance for {category_name} based on days: {applicable_distance} km")

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            pricing_dict[category_name][car_type] = self.calculate_cost(
                applicable_distance, price, toll_price=toll_price, num_days=num_days
            )

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

class AddRide(TemplateView):
    template_name = "telecaller/add_ride.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['customerlist'] = Customer.objects.all()
        context['ridetypelist'] = Ridetype.objects.all()
        context['catlist'] = Category.objects.filter(category_status='active')
        
        last_ride = RideDetails.objects.all().order_by('-ride_id').first()
        if last_ride:
            try:
                last_company_format = int(last_ride.company_format.replace('RID', ''))
            except:
                last_company_format = int("0"+str(last_ride.ride_id) if last_ride.ride_id < 10 else last_ride.ride_id)
            next_company_format = f'RID{last_company_format + 1:02}'
        else:
            next_company_format = 'RID01'
        context['next_company_format'] = next_company_format
        
        return context
    
    def post(self, request):
        try:
            print("Fetching POST data")
            company_format = request.POST['company_format']
            ride_type_id = request.POST['ridetype']
            source = request.POST.get('source')
            destination = request.POST.get('destination')
            pickup_date = request.POST.get('pickup_date')
            pickup_time = request.POST.get('pickup_time')
            category = request.POST.get('category')
            total_fare = request.POST.get('total_fare')
            customer_id = request.POST['customer']
            customer_notes = request.POST['customer_notes']
            car_type = request.POST.get('car_type', '').strip()  
            slots = determine_time_slot(pickup_time)
            ride_status = request.POST['ride_status']
            phone_number = request.POST['phone_number']
            customer_name = request.POST['customer_name']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']

            print(f"Parsed data: {company_format}, {ride_type_id}, {source}, {destination}, {pickup_date}, {pickup_time}")

            try:
                customer = Customer.objects.get(phone_number=phone_number)
            except Customer.DoesNotExist:
                last_customer = Customer.objects.all().order_by('-customer_id').first()
                new_customer_id = last_customer.customer_id + 1 if last_customer else 1
                customer_company_format = f'CUST{new_customer_id:02}'
                customer = Customer(
                    customer_id=new_customer_id,
                    company_format=customer_company_format,
                    customer_name=customer_name,
                    phone_number=phone_number,
                    email=email,
                    password=password,
                    address=address,
                    status='active',
                    created_by=request.user,
                    updated_by=request.user
                )
                customer.save()
            print(f"Created new customer: {customer}")

            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            category_name = category.split('|')[0]
            car_type_name = category.split('|')[1]
            category_instance = Category.objects.get(category_name=category_name)

            try:
                if ridetype.name.lower() == 'local':
                    pricing_instance = Pricing.objects.get(
                        category=category_instance,
                        car_type=car_type_name,
                        ridetype=ridetype,
                        slots=slots,
                    )
                    
                else:
                    trip_type = request.POST.get('trip_type', '').strip()
                    print('trip_type from request:', trip_type)  
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
       



            print(f"Saving ride with details: {company_format}, {ridetype}, {category_instance}")

            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            next_company_format = self.get_context_data()['next_company_format']

            print(f'company_format: {next_company_format}')
            print(f'ridetype: {ridetype}')
            print(f'source: {source}')
            print(f'destination: {destination}')
            print(f'pickup_date: {pickup_date}')
            print(f'pickup_time: {pickup_time}')
            print(f'category: {category_instance}')
            print(f'total_fare: {total_fare}')
            print(f'customer: {customer}')
            print(f'customer_notes: {customer_notes}')
            print(f'pricing: {pricing_instance}')
            
        
            ride_details = RideDetails(
                company_format=next_company_format,
                customer=customer,
                ridetype=ridetype,
                category=category_instance,
                source=source,
                destination=destination,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                total_fare=total_fare,
                customer_notes=customer_notes,
                ride_status=ride_status,
                assigned_by=request.user,
                cancelled_by=request.user,
                created_by=request.user,
                updated_by=request.user,
                pricing = pricing_instance,  

            )
            ride_details.save()
            print("Ride details saved successfully.")
            
            whatsapp = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                "campaignName": "booking confirmation",
                "destination": customer.phone_number,
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
    pickup_time = datetime.strptime(pickup_time, '%H:%M').time()
    if time(0, 0) <= pickup_time < time(6, 0):
        return '12AM - 6AM'
    elif time(6, 0) <= pickup_time < time(12, 0):
        return '6AM - 12PM'
    elif time(12, 0) <= pickup_time < time(18, 0):
        return '12PM - 6PM'
    else:
        return '6PM - 12AM'

                
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class RideList(ListView):
    model = RideDetails
    template_name = "telecaller/view_ride.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.filter(verification_status='verified')
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='currentbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  
        
        return context

    def get_queryset(self):
        today = date.today()
        past_rides = RideDetails.objects.filter(pickup_date__lt=today, ride_status='currentbookings')
        past_rides.update(ride_status='pendingbookings')
    
        
        current_rides = RideDetails.objects.filter(ride_status='currentbookings', pickup_date=today)

        print(f"Current rides count: {current_rides.count()}")
        
        service_type = self.request.GET.get('service_type_id')
        if service_type:
            current_rides = current_rides.filter(ridetype_id=service_type)
        return current_rides


@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvanceBookingsList(ListView):
    model = RideDetails
    template_name = "telecaller/advance_bookings.html"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  
        return context

    def get_queryset(self):
        today = date.today()
        
        today_rides = RideDetails.objects.filter(pickup_date=today, ride_status='advancebookings')
        today_rides.update(ride_status='currentbookings')
        
        advance_rides = RideDetails.objects.filter(ride_status='advancebookings', pickup_date__gt=today)
        
        return advance_rides
    

def update_ride_status(request, ride_id):
    if request.method == 'POST':
        try:
            ride = RideDetails.objects.get(ride_id=ride_id)
            pickup_date = request.POST.get('pickup_date')

            if pickup_date:
                today = date.today().isoformat()

                if pickup_date > today:
                    ride.ride_status = 'advancebookings'
                else:
                    ride.ride_status = 'currentbookings'

                ride.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'pickup_date not provided'})

        except RideDetails.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ride not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "telecaller/assigned_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='assignbookings')).select_related('driver')


class OngoingRideList(ListView):
    model = RideDetails
    template_name = "telecaller/ongoing_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='ongoingbookings') 
    
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "telecaller/completed_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='completedbookings') 


def assign_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver_id = data.get('driver_id') 
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)  
            driver = Driver.objects.get(company_format=driver_id)  
            ride.driver = driver  
            ride.ride_status = 'assignbookings'
            
            ride.save()

            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Driver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)

class AssignDriverView(ListView):
    model = Driver
    template_name = 'telecaller/view_ride.html'
    context_object_name = 'drivers'

    def get_queryset(self):
        return Driver.objects.filter(status='active')


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteRide(View):
    def get(self, request):
        ride_id = request.GET.get('ride_id', None)
        RideDetails.objects.get(ride_id=ride_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditRide(TemplateView):
    template_name = 'telecaller/edit_ride.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customerlist = Customer.objects.all()
        ridetypelist = Ridetype.objects.all()
        modellist = Model.objects.all()
        catlist = Category.objects.all()
        blist = Brand.objects.all()

        try:
            context['ride_id'] = self.kwargs['id']
            ride = RideDetails.objects.filter(ride_id=context['ride_id'])
        except:
            ride = RideDetails.objects.filter(ride_id=context['ride_id'])
            
        context = {
            'customerlist': list(customerlist),
            'ridetypelist': list(ridetypelist),
            'modellist': list(modellist),
            'catlist': list(catlist),
            'blist': list(blist),
            'ride': list(ride)

        }
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateRide(APIView):
    @csrf_exempt
    def post(self, request):
        
            ride_id = request.POST.get('ride_id')
            if not ride_id:
                return JsonResponse({'success': False, 'error': 'Missing ride_id'}, status=400)

            try:
                ride_id = int(ride_id)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid ride_id'}, status=400)
            
            try:
                ride = RideDetails.objects.get(ride_id=ride_id)
            except RideDetails.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Ride not found'}, status=404)
            
            customer_id = request.POST.get('customer', None)
            if customer_id:
                try:
                    customer_id = int(customer_id)
                    customer = Customer.objects.get(customer_id=customer_id)
                    ride.customer = customer
                except (ValueError, Customer.DoesNotExist):
                    return JsonResponse({'success': False, 'error': 'Invalid customer_id'}, status=400)
            
            ride.source = request.POST.get('source', ride.source)
            ride.destination = request.POST.get('destination', ride.destination)
            ride.pickup_date = request.POST.get('pickup_date', ride.pickup_date)
            ride.pickup_time = request.POST.get('pickup_time', ride.pickup_time)
            ride.total_fare = request.POST.get('total_fare', ride.total_fare)
            ride.customer_notes = request.POST.get('customer_notes', ride.customer_notes)
            ride.updated_by = request.user
            ride.save()

            RideDetailsHistory.objects.create(
                ride_id=ride.ride_id,
                company_format=ride.company_format,
                ridetype=ride.ridetype,
                source=ride.source,
                destination=ride.destination,
                pickup_date=ride.pickup_date,
                pickup_time=ride.pickup_time,
                model=ride.model,
                driver=ride.driver,
                assigned_by=ride.assigned_by.username if ride.assigned_by else None,
                cancelled_by=ride.cancelled_by.username if ride.cancelled_by else None,
                total_fare=ride.total_fare,
                customer=ride.customer,
                customer_notes=ride.customer_notes,
                ride_status=ride.ride_status,
                booking_datetime=ride.booking_datetime,
                created_on=ride.created_on,
                updated_on=ride.updated_on,
                created_by=ride.created_by.username if ride.created_by else None,
                updated_by=request.user.username,
                comments=ride.comments
            )

            return JsonResponse({'success': True}, status=200)
    
class RideDetailsHistoryView(TemplateView):
    template_name = 'telecaller/history_ride.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride_id = self.kwargs['ride_id']
        ride = get_object_or_404(RideDetails, ride_id=ride_id)
        history = RideDetailsHistory.objects.filter(ride_id=ride_id).order_by('updated_on')
        context['ride'] = ride
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class profile(TemplateView):
    template_name = 'telecaller/app-profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_id = self.request.session.get('user_id')
            userlist = User.objects.filter(id=user_id)
        except:
            userlist = User.objects.filter(id=user_id)
            
        context['userlist']= list(userlist)
        return context
    
@login_required
def telecaller_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='telecaller')
    return render(request, 'telecaller/app-profile.html', {'profile': profile})
    
class UpdateUserView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.user:
            user = request.user            
            if username and password:
                user.username = username
                user.set_password(password)
                user.save()
                if user is not None:
                    return JsonResponse({'status': 'success'}, status=200)
                return JsonResponse({'status': 'error', 'message': 'Authentication failed'}, status=400)
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



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


@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "telecaller/view_cancelbookings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  
        return context

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='cancelledbookings') & Q(cancelled_by=self.request.user)).select_related('driver')

def cancel_ride(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comments = data.get('comments')
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)
            ride.comments = comments
            ride.ride_status = 'cancelledbookings'
            ride.cancelled_by = request.user
            ride.save()

            message = f"""
            Hello {ride.customer.customer_name},

            Thank you for choosing Ridexpress!

            We regret to inform you that your booking with Ridexpress has been cancelled:

            Booking ID: {ride.company_format}
            Pickup Date & Time: {ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}
            Pickup Location: {ride.source}
            Drop-off Location: {ride.destination}

            If you didn’t request this cancellation or if you need further assistance, please contact us at +91 6366463555 or reply to this email.

            We hope to serve you in the future!

            Best regards,
            Ridexpress
            """

            payload = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                "campaignName": "booking_cancellation",
                "destination": ride.customer.phone_number,
                "userName": "Ridexpress",
                "templateParams": [
                    str(ride.customer.customer_name),
                    str(ride.company_format),
                    f"{ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}",
                    str(ride.source),
                    str(ride.destination)
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
            response = requests.post(gateway_url, json=payload, headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                print("WhatsApp message sent successfully:", response.json())
            else:
                print("Failed to send WhatsApp message:", response.text)

            return JsonResponse({'status': 'success'})

        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)

        
@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = "telecaller/view_driver.html"
        

class EnquiryList(ListView):
    model = Enquiry
    template_name = "telecaller/view_enquiry.html"     
        

@login_required(login_url='login')   
def check_package_category(request):
    category_name = request.GET.get('category_name', None)
    cp = PackageCategories.objects.filter(category_name=category_name)
    data = {
        'exists': cp.count() > 0
    }
    return JsonResponse(data) 

@method_decorator(login_required(login_url='login'), name='dispatch')
class addpackagecategory(TemplateView):
    template_name = "telecaller/add_package_category.html"

    def post(self, request):
        category_name = request.POST['category_name']

        cl = PackageCategories(
            category_name=category_name,
            created_by=request.user,
            updated_by=request.user
        )
        cl.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageCategoryList(ListView):
    model = PackageCategories
    template_name = "telecaller/view_package_category.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletePackageCategory(View):
    def get(self, request):
        package_category_id = request.GET.get('package_category_id', None)
        PackageCategories.objects.get(package_category_id=package_category_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPackageCategory(TemplateView):
    template_name = 'telecaller/edit_package_category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['package_category_id'] = self.kwargs['id']
            plist = PackageCategories.objects.filter(package_category_id=context['package_category_id'])
        except:
            plist = PackageCategories.objects.filter(package_category_id=context['package_category_id'])
            
        context['plist']= list(plist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdatePackageCategory(APIView):
    def post(self, request):
        package_category_id = request.POST['package_category_id']
        package = PackageCategories.objects.get(package_category_id=package_category_id)

        package.category_name = request.POST['category_name']
        package.updated_by = request.user
        package.save()

        PackageCategoriesHistory.objects.create(
            package_category_id=package.package_category_id,
            category_name=package.category_name,
            created_on=package.created_on,
            updated_on=package.updated_on,
            created_by=package.created_by.username if package.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class PackageCategoryHistoryView(TemplateView):
    template_name = 'telecaller/history_package_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_category_id = self.kwargs['package_category_id']
        package = get_object_or_404(PackageCategories, package_category_id=package_category_id)
        history = PackageCategoriesHistory.objects.filter(package_category_id=package_category_id).order_by('updated_on')
        context['package'] = package
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class addwebpackages(TemplateView):
    template_name = "telecaller/add_webpackages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pclist = PackageCategories.objects.all()
        context = {'pclist': list(pclist)}
        return context

    def post(self, request):
        try:
            print("POST request received")

            title = request.POST.get('title')
            slug = slugify(title)
            package_category_id = request.POST.get('package_category')
            description = request.POST.get('description')
            top_attraction = request.POST.get('top_attraction')
            why_visit = request.POST.get('why_visit')
            package_highlights = request.POST.get('package_highlights')
            image = request.FILES.get('image')
            image_link = request.POST.get('image_link')
            facebook_link = request.POST.get('facebook_link')
            instagram_link = request.POST.get('instagram_link')
            whatsapp_link = request.POST.get('whatsapp_link')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            tags = request.POST.get('tags')
            h1tag = request.POST.get('h1tag')
            status = request.POST.get('status')

            print(f"Form data: title={title}, category_id={package_category_id}, description={description}")

            if not title or not package_category_id:
                print("Missing required fields: title or category")
                return JsonResponse({'status': "Failed", 'error': "Title and category are required."}, status=400)

            try:
                package_category = PackageCategories.objects.get(package_category_id=package_category_id)
            except PackageCategories.DoesNotExist:
                print(f"Package category not found: {package_category_id}")
                return JsonResponse({'status': "Failed", 'error': "Invalid package category."}, status=400)

            webpackage = WebsitePackages(
                title=title,
                slug=slug,
                package_category=package_category,
                description=description,
                top_attraction=top_attraction,
                why_visit=why_visit,
                package_highlights=package_highlights,
                image=image,
                image_link=image_link,
                facebook_link=facebook_link,
                instagram_link=instagram_link,
                whatsapp_link=whatsapp_link,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                tags=tags,
                h1tag=h1tag,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )

            webpackage.save()
            print("Package saved successfully")
            return JsonResponse({'status': "Success"})

        except Exception as e:
            print(f"Error saving package: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)
    
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class webPackageList(ListView):
    model = WebsitePackages
    template_name = "telecaller/view_webpackages.html"
    context_object_name = 'webpackages'
    
    def get_queryset(self):
        return WebsitePackages.objects.filter(created_by=self.request.user)

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletewebPackages(View):
    def get(self, request):
        webpackage_id = request.GET.get('webpackage_id', None)
        WebsitePackages.objects.get(webpackage_id=webpackage_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditwebPackages(TemplateView):
    template_name = 'telecaller/edit_webpackages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pclist = PackageCategories.objects.all()
        try:
            context['webpackage_id'] = self.kwargs['id']
            package = WebsitePackages.objects.filter(webpackage_id=context['webpackage_id'])
        except:
            package = WebsitePackages.objects.filter(webpackage_id=context['webpackage_id'])
        context = {'pclist': list(pclist), 'package': list(package)}
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdatewebPackages(APIView):
    def post(self, request):
        webpackage_id = request.POST['webpackage_id']
        title = request.POST['title']
        print("########",title)
        slug = slugify(title)
        package_category = request.POST['package_category']
        description = request.POST['description']
        top_attraction = request.POST['top_attraction']
        why_visit = request.POST['why_visit']
        package_highlights = request.POST['package_highlights']
        image = request.FILES.get('image')

        image_link = request.POST['image_link']
        facebook_link = request.POST['facebook_link']
        instagram_link = request.POST['instagram_link']
        whatsapp_link = request.POST['whatsapp_link']
        tags = request.POST['tags']
        meta_title = request.POST['meta_title']
        meta_description = request.POST['meta_description']
        meta_keywords = request.POST['meta_keywords']
        h1tag = request.POST['h1tag']
        status = request.POST['status']

        package_categoryIdobj = PackageCategories.objects.get(package_category_id=package_category)

        webpack = WebsitePackages.objects.get(webpackage_id=webpackage_id)


        webpack.title= title
        print("######## 2 ",title)
        webpack.slug=slug
        webpack.package_category= package_categoryIdobj
        webpack.description= description
        webpack.top_attraction= top_attraction
        webpack.why_visit= why_visit
        webpack.package_highlights= package_highlights
        webpack.image_link= image_link
        if image:
            webpack.image = image
        webpack.facebook_link= facebook_link
        webpack.instagram_link= instagram_link
        webpack.whatsapp_link= whatsapp_link
        webpack.tags= tags
        webpack.meta_title= meta_title
        webpack.meta_description= meta_description
        webpack.meta_keywords= meta_keywords
        webpack.h1tag= h1tag
        webpack.status=status
        webpack.updated_by = request.user
        webpack.save()
        
        return JsonResponse({'success': True}, status=200) 

    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddBlogView(TemplateView):
    template_name = "telecaller/add_blog.html"

    def post(self, request):
        try:
            print("POST request received")

            title = request.POST.get('title')
            slug = slugify(title)
            description = request.POST.get('description')
            image = request.FILES.get('image')
            image_link = request.POST.get('image_link')
            facebook = request.POST.get('facebook_link')
            instagram = request.POST.get('instagram_link')
            whatsapp = request.POST.get('whatsapp_link')
            tags = request.POST.get('tags')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            h1tag = request.POST.get('h1tag')
            backlink = request.POST.get('backlink')
            related_bloglink = request.POST.get('related_bloglink')

            blog = Blogs(
                title=title,
                slug=slug,
                description=description,
                image_link=image_link,
                facebook=facebook,
                instagram=instagram,
                whatsapp=whatsapp,
                tags=tags,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                h1tag=h1tag,
                backlink=backlink,
                related_bloglink=related_bloglink,
                created_by=request.user,
                updated_by=request.user
            )

            if image:
                try:
                    print(f"Processing image: {image.name}")
                    img = Image.open(image)
                    img = img.resize((880, 450), Image.LANCZOS)
                    file_extension = os.path.splitext(image.name)[1].lower()

                    format = 'JPEG' if file_extension in ['.jpg', '.jpeg'] else 'PNG' if file_extension == '.png' else 'GIF'

                    img_io = BytesIO()
                    img.save(img_io, format=format)
                    img_content = ContentFile(img_io.getvalue(), image.name)
                    blog.image.save(image.name, img_content, save=False)
                except Exception as img_error:
                    print(f"Error processing image: {img_error}")
                    return JsonResponse({'status': "Failed", 'error': "Error processing image."}, status=400)

            blog.save()
            print("Blogs saved successfully")
            return JsonResponse({'status': "Success"})

        except Exception as e:
            print(f"Error saving blogs: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)

@method_decorator(login_required(login_url='login'), name='dispatch')
class BlogListView(ListView):
    model = Blogs
    template_name = "telecaller/view_blog.html"
    context_object_name = 'blogs'
    
    def get_queryset(self):
        return Blogs.objects.filter(created_by=self.request.user)

@method_decorator(login_required(login_url='login'), name='dispatch')
class webDeleteBlogs(View):
    def get(self, request):
        blogs_id = request.GET.get('blogs_id', None)
        Blogs.objects.get(blogs_id=blogs_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditwebBlogs(TemplateView):
    template_name = 'telecaller/edit_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['blogs_id'] = self.kwargs['id']
            blog = Blogs.objects.filter(blogs_id=context['blogs_id'])
        except:
            blog = Blogs.objects.filter(blogs_id=context['blogs_id'])
        context = {'blog': list(blog)}
        return context 
    
class UpdatewebBlogs(APIView):
    def post(self, request):
        blogs_id = request.POST.get('blogs_id')
        title = request.POST.get('title')
        slug = slugify(title)
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image_link = request.POST.get('image_link')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        whatsapp = request.POST.get('whatsapp')
        backlink = request.POST.get('backlink')
        related_bloglink = request.POST.get('related_bloglink')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        h1tag = request.POST.get('h1tag')

        try:
            blog = Blogs.objects.get(blogs_id=blogs_id)
        except Blogs.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'}, status=404)

        blog.title = title
        blog.slug=slug
        blog.description = description
        if image:
            blog.image = image  
        blog.image_link = image_link
        blog.facebook = facebook
        blog.instagram = instagram
        blog.whatsapp = whatsapp
        blog.backlink = backlink
        blog.related_bloglink = related_bloglink
        blog.meta_title = meta_title
        blog.meta_description = meta_description
        blog.meta_keywords = meta_keywords
        blog.h1tag = h1tag

        blog.save()

        return JsonResponse({'success': True}, status=200)    
