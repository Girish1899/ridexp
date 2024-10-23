from datetime import date, datetime, time, timezone
from decimal import Decimal
import json
import os
import zipfile
from django.core.cache import cache
import random
from django.db import IntegrityError
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from superadmin.models import Accounts, Brand, BrandHistory,Category, CategoryHistory, Color, ColorHistory, CommissionHistory, CommissionType, ContactUs, CustomerHistory, DailyVehicleComm, DriverHistory, Enquiry,Model, ModelHistory, PackageCategories, PackageCategoriesHistory, PackageName, PackageNameHistory, PackageOrder, PackageOrderHistory, Packages, PackagesHistory, Pricing, PricingHistory, ProfileHistory, RideDetails,Profile, RidetypeHistory, Transmission, TransmissionHistory,User, VehicleHistory, VehicleOwnerHistory,VehicleType,Customer,Driver,VehicleOwner,Ridetype,Vehicle, VehicleTypeHistory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,View,DetailView
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count
import requests
from rest_framework.views import APIView
from django.contrib import messages


@login_required(login_url='login')
def adminuser_index(request):
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
    return render(request, 'adminuser/index.html',context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = "adminuser/view_category.html"

class CategoryHistoryView(TemplateView):
    template_name = 'adminuser/history_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, category_id=category_id)
        history = CategoryHistory.objects.filter(category_id=category_id).order_by('-updated_on')
        context['category'] = category
        context['history'] = history
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class BrandListView(ListView):
    model = Brand
    template_name = "adminuser/view_brand.html"

class BrandHistoryView(TemplateView):
    template_name = 'adminuser/history_brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_id = self.kwargs['brand_id']
        brand = get_object_or_404(Brand, brand_id=brand_id)
        history = BrandHistory.objects.filter(brand_id=brand_id).order_by('-updated_on')
        context['brand'] = brand
        context['history'] = history
        return context  

@method_decorator(login_required(login_url='login'), name='dispatch')
class ModelListView(ListView):
    model = Model
    template_name = "adminuser/view_model.html"

class ModelHistoryView(TemplateView):
    template_name = 'adminuser/history_model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, model_id=model_id)
        history = ModelHistory.objects.filter(model_id=model_id).order_by('-updated_on')
        context['model'] = model
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class vehicletypeList(ListView):
    model = VehicleType
    template_name = "adminuser/view_vehicletype.html"

class VehicleTypeHistoryView(TemplateView):
    template_name = 'adminuser/history_vehicletype.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_type_id = self.kwargs['vehicle_type_id']
        vehicle_type = get_object_or_404(VehicleType, vehicle_type_id=vehicle_type_id)
        history = VehicleTypeHistory.objects.filter(vehicle_type_id=vehicle_type_id)
        context['vehicle_type'] = vehicle_type
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class ridetypeList(ListView):
    model = Ridetype
    template_name = "adminuser/view_ridetype.html"

class RidetypeHistoryView(TemplateView):
    template_name = 'adminuser/history_ridetype.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ridetype_id = self.kwargs['ridetype_id']
        ridetype = get_object_or_404(Ridetype, ridetype_id=ridetype_id)
        history = RidetypeHistory.objects.filter(ridetype_id=ridetype_id).order_by('-updated_on')
        context['ridetype'] = ridetype
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserList(ListView):
    model = Profile
    template_name = "adminuser/view_user.html"

class ProfileHistoryView(TemplateView):
    template_name = 'adminuser/history_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        profile = get_object_or_404(Profile, user_id=user_id)
        history = ProfileHistory.objects.filter(user_id=user_id)
        context['profile'] = profile
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UserEmpList(ListView):
    model = Profile
    template_name = "adminuser/view_useremp.html"    

@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = "adminuser/view_customer.html"
    def get_queryset(self):
        customers = Customer.objects.annotate(
            ride_count=Count('ridedetails')
        )

        completed_rides_totals = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('customer').annotate(
            total_fare=Sum('total_fare')
        ).values('customer', 'total_fare')

        fare_dict = {item['customer']: item['total_fare'] for item in completed_rides_totals}

        for customer in customers:
            customer.total_fare = fare_dict.get(customer.pk, 0.0)

        return customers

class CustomerHistoryView(TemplateView):
    template_name = 'adminuser/history_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(Customer, customer_id=customer_id)
        history = CustomerHistory.objects.filter(customer_id=customer_id).order_by('-updated_on')
        context['customer'] = customer
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerListView(ListView):
    model = VehicleOwner
    template_name = "adminuser/view_vehicleowner.html"

class VehicleOwnerHistoryView(TemplateView):
    template_name = 'adminuser/history_vehicleowner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_id = self.kwargs['owner_id']
        owner = get_object_or_404(VehicleOwner, owner_id=owner_id)
        history = VehicleOwnerHistory.objects.filter(owner_id=owner_id).order_by('-updated_on')
        context['owner'] = owner
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class VehicleList(ListView):
    model = Vehicle
    template_name = "adminuser/view_vehicle.html"

class VehicleHistoryView(TemplateView):
    template_name = 'adminuser/history_vehicle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
        history = VehicleHistory.objects.filter(vehicle_id=vehicle_id).order_by('-updated_on')
        context['vehicle'] = vehicle
        context['history'] = history
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = "adminuser/view_driver.html"

class DriverHistoryView(TemplateView):
    template_name = 'adminuser/history_driver.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_id = self.kwargs['driver_id']
        driver = get_object_or_404(Driver, driver_id=driver_id)
        history = DriverHistory.objects.filter(driver_id=driver_id)
        context['driver'] = driver
        context['history'] = history
        return context


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

        daily_km_cap = 250 * num_days
        applicable_distance = max(distance, daily_km_cap)

        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name
            car_type = price.car_type.lower()
            toll_price = Decimal(str(price.toll_price))
            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

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
    template_name = "adminuser/add_ride.html"

    def parse_date(self, date_str):
        """Helper function to parse dates in multiple formats"""
        for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date {date_str} is not in a recognized format.")
    
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
            drop_date_str = request.POST.get('drop_date', '')
            drop_time_str = request.POST.get('drop_time', '')

            drop_date = self.parse_date(drop_date_str) if drop_date_str else None
            drop_time = datetime.strptime(drop_time_str, '%H:%M').time() if drop_time_str else None

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
                drop_date=drop_date,
                drop_time=drop_time,
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
class RideList(ListView):
    model = RideDetails
    template_name = "adminuser/view_ride.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  
        return context

    def get_queryset(self):
        today = date.today()
        past_rides = RideDetails.objects.filter(pickup_date__lt=today, ride_status='currentbookings')
        past_rides.update(ride_status='pendingbookings')
        
        current_rides = RideDetails.objects.filter(ride_status='currentbookings', pickup_date=today)
        
        return current_rides


@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvanceBookingsList(ListView):
    model = RideDetails
    template_name = "adminuser/advance_bookings.html"  

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
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class PendingBookingsList(ListView):
    model = RideDetails
    template_name = "adminuser/pending_bookings.html"  

    def get_queryset(self):
        today = date.today()
        return RideDetails.objects.filter(ride_status='pendingbookings', pickup_date__lt=today)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "adminuser/assigned_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='assignbookings')).select_related('driver')

class OngoingRideList(ListView):
    model = RideDetails
    template_name = "adminuser/ongoing_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='ongoingbookings') 
    
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "adminuser/completed_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='completedbookings') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='completedbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all() 
        context['drivers'] = Driver.objects.all() 
        return context
    
def completed_bookings_filter(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        bookings = RideDetails.objects.filter(booking_datetime__range=[start_date, end_date])
        data = serialize('json', bookings, use_natural_primary_keys=True, use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid date range'}, status=400)
    

class InvoiceView(DetailView):
    model = RideDetails
    template_name = 'adminuser/invoice.html'
    context_object_name = 'ride'
    
    def get_object(self):
        ride_id = self.kwargs.get("ride_id")
        return get_object_or_404(RideDetails, ride_id=ride_id)  

@login_required
def adminuser_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='admin')
    return render(request, 'adminuser/app-profile.html', {'profile': profile})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.user:
            user = request.user
            print("^^^^^^^^^^^^^^^^^^^^^^^",user)
            if username and password:
                user.username = username
                user.set_password(password)
                user.save()
                print("user------------------------------------------------",user)
                if user is not None:
                    return JsonResponse({'status': 'success'}, status=200)
                return JsonResponse({'status': 'error', 'message': 'Authentication failed'}, status=400)
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



@method_decorator(login_required(login_url='login'), name='dispatch')
class PriceList(ListView):
    model = Pricing
    template_name = "adminuser/view_pricing.html"

class PricingHistoryView(TemplateView):
    template_name = 'adminuser/history_pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pricing_id = self.kwargs['pricing_id']
        pricing = get_object_or_404(Pricing, pricing_id=pricing_id)
        history = PricingHistory.objects.filter(pricing_id=pricing_id).order_by('updated_on')
        context['pricing'] = pricing
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CommissionList(ListView):
    model = CommissionType
    template_name = "adminuser/view_commissiontype.html"

class CommissionHistoryView(TemplateView):
    template_name = 'adminuser/history_commission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission_id = self.kwargs['commission_id']
        commission = get_object_or_404(CommissionType, commission_id=commission_id)
        history = CommissionHistory.objects.filter(commission_id=commission_id).order_by('updated_on')
        context['commission'] = commission
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "adminuser/view_cancelbookings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  
        return context

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='cancelledbookings') 
    

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
class TransmissionListView(ListView):
    model = Transmission
    template_name = "adminuser/view_transmission.html"    

class TransmissionHistoryView(TemplateView):
    template_name = 'adminuser/history_transmission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transmission_id = self.kwargs['transmission_id']
        transmission = get_object_or_404(Transmission, transmission_id=transmission_id)
        history = TransmissionHistory.objects.filter(transmission_id=transmission_id).order_by('updated_on')
        context['transmission'] = transmission
        context['history'] = history
        return context 

@method_decorator(login_required(login_url='login'), name='dispatch')
class colorList(ListView):
    model = Color
    template_name = "adminuser/view_color.html"

class ColorHistoryView(TemplateView):
    template_name = 'adminuser/history_color.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color_id = self.kwargs['color_id']
        color = get_object_or_404(Color, color_id=color_id)
        history = ColorHistory.objects.filter(color_id=color_id).order_by('updated_on')
        context['color'] = color
        context['history'] = history
        return context 

@method_decorator(login_required(login_url='login'), name='dispatch')
class VehicleBlockList(ListView):
    model = Vehicle
    template_name = "adminuser/view_vehicleblock.html"

    def get_queryset(self):
        return Vehicle.objects.filter(Q(vehicle_status='inactive'))  


class CustomerProfileHistoryView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, pk=customer_id)
        rides = RideDetails.objects.filter(customer=customer)
        current_bookings = rides.filter(ride_status='currentbookings')
        completed_bookings = rides.filter(ride_status='completedbookings')
        cancelled_bookings = rides.filter(ride_status='cancelledbookings')
        advanced_bookings = rides.filter(ride_status='advancebookings')
        assigned_bookings = rides.filter(ride_status='assignbookings')
        ongoing_booking = rides.filter(ride_status='ongoingbookings')

        context = {
            'customer': customer,
            'current_bookings': current_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'advanced_bookings': advanced_bookings,
            'assigned_bookings': assigned_bookings,
            'ongoing_booking': ongoing_booking,
        }
        return render(request, 'adminuser/customer_bookings.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerProfileList(ListView):
    model = Customer
    template_name = "adminuser/cust_profile_list.html" 

    def get_queryset(self):
        customers = Customer.objects.annotate(
            ride_count=Count('ridedetails')
        )

        completed_rides_totals = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('customer').annotate(
            total_fare=Sum('total_fare')
        ).values('customer', 'total_fare')

        fare_dict = {item['customer']: item['total_fare'] for item in completed_rides_totals}

        for customer in customers:
            customer.total_fare = fare_dict.get(customer.pk, 0.0)

        return customers   

class VehicleListView(ListView):
    model = Vehicle
    template_name = "adminuser/vehicle_list.html"

    def get_queryset(self):
        return Vehicle.objects.select_related('owner').prefetch_related('driver_set').all()
    
class VehicleDailySummaryView(ListView):
    model = DailyVehicleComm
    template_name = "adminuser/vehicle_daily_summary.html"

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        completed_rides_dates = RideDetails.objects.filter(
            driver__vehicle=vehicle,
            ride_status='completedbookings'
        ).values_list('pickup_date', flat=True).distinct()

        for date in completed_rides_dates:
            rides = RideDetails.objects.filter(
                driver__vehicle=vehicle,
                ride_status='completedbookings',
                pickup_date=date
            )

            total_fare = Decimal(0)
            total_driver_commission = Decimal(0)
            total_company_commission = Decimal(0)

            for ride in rides:
                driver_commission = self.calculate_driver_commission(ride)
                company_commission = ride.total_fare - driver_commission

                total_fare += ride.total_fare
                total_driver_commission += driver_commission
                total_company_commission += company_commission

            print(f"vehicle: {vehicle}, date: {date}")
            print(f"total_fare: {total_fare}, total_driver_commission: {total_driver_commission}, total_company_commission: {total_company_commission}")

            try:
                daily_summary, created = DailyVehicleComm.objects.update_or_create(
                    vehicle=vehicle,
                    date=date,
                    defaults={
                        'total_fare': total_fare,
                        'total_driver_commission': total_driver_commission,
                        'total_company_commission': total_company_commission
                    }
                )
            except Exception as e:
                import traceback
                print(f"Error updating or creating DailyVehicleComm: {e}")
                print(traceback.format_exc())

        return DailyVehicleComm.objects.filter(vehicle=vehicle).order_by('-date')

    def calculate_driver_commission(self, ride):
        if ride.driver and ride.driver.vehicle and ride.driver.vehicle.commission_type:
            vehicle_commission_percentage = Decimal(str(ride.driver.vehicle.commission_type.commission_percentage))
            vehicle_commission_amount = (ride.total_fare * vehicle_commission_percentage) / Decimal(100)
            driver_commission = ride.total_fare - vehicle_commission_amount
            return driver_commission
        return Decimal(0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_id'] = self.kwargs['vehicle_id']
        context['vehicle'] = Vehicle.objects.get(vehicle_id=self.kwargs['vehicle_id'])
        return context
    

class BookingDetailsView(ListView):
    model = RideDetails
    template_name = "adminuser/booking_details.html"

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        date = self.kwargs['date']
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        rides = RideDetails.objects.filter(
            driver__vehicle=vehicle,
            ride_status='completedbookings',
            pickup_date=date
        ).order_by('pickup_time')

        for ride in rides:
            ride.driver_commission = self.calculate_driver_commission(ride)
            ride.company_commission = ride.total_fare - ride.driver_commission

        return rides

    def calculate_driver_commission(self, ride):
        if ride.driver and ride.driver.vehicle and ride.driver.vehicle.commission_type:
            vehicle_commission_percentage = Decimal(str(ride.driver.vehicle.commission_type.commission_percentage))
            vehicle_commission_amount = (ride.total_fare * vehicle_commission_percentage) / Decimal(100)
            driver_commission = ride.total_fare - vehicle_commission_amount
            return driver_commission
        return Decimal(0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle'] = Vehicle.objects.get(vehicle_id=self.kwargs['vehicle_id'])
        context['date'] = self.kwargs['date']
        return context  

@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountsListView(ListView):
    model = Accounts
    template_name = "adminuser/view_accounts.html"  

class ContactList(ListView):
    model = ContactUs
    template_name = "adminuser/view_contact.html"   

class EnquiryList(ListView):
    model = Enquiry
    template_name = "adminuser/view_enquiry.html"  


@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageCategoryList(ListView):
    model = PackageCategories
    template_name = "adminuser/view_package_category.html"

class PackageCategoryHistoryView(TemplateView):
    template_name = 'adminuser/history_package_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_category_id = self.kwargs['package_category_id']
        package = get_object_or_404(PackageCategories, package_category_id=package_category_id)
        history = PackageCategoriesHistory.objects.filter(package_category_id=package_category_id).order_by('updated_on')
        context['package'] = package
        context['history'] = history
        return context    

@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageNameList(ListView):
    model = PackageName
    template_name = "adminuser/view_package_name.html"

class PackageNameHistoryView(TemplateView):
    template_name = 'adminuser/history_package_name.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_name_id = self.kwargs['package_name_id']
        package = get_object_or_404(PackageName, package_name_id=package_name_id)
        history = PackageNameHistory.objects.filter(package_name_id=package_name_id).order_by('updated_on')
        context['package'] = package
        context['history'] = history
        return context     

@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageList(ListView):
    model = Packages
    template_name = "adminuser/view_packages.html"

class PackagesHistoryView(TemplateView):
    template_name = 'adminuser/history_packages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs['package_id']
        package = get_object_or_404(Packages, package_id=package_id)
        history = PackagesHistory.objects.filter(package_id=package_id).order_by('updated_on')
        context['package'] = package
        context['history'] = history
        return context    

@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageOrderList(ListView):
    model = PackageOrder
    template_name = "adminuser/view_package_order.html" 

class PackageOrderHistoryView(TemplateView):
    template_name = 'adminuser/history_package_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        package_order = get_object_or_404(PackageOrder, order_id=order_id)
        history = PackageOrderHistory.objects.filter(order_id=order_id).order_by('updated_on')
        context['package_order'] = package_order
        context['history'] = history
        return context   
         

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
class AssignLaterList(ListView):
    model = RideDetails
    template_name = "adminuser/assign_later.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='assignlaterbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1) 
        return context

    def get_queryset(self):
        
        return RideDetails.objects.filter(Q(ride_status='assignlaterbookings')).select_related('driver')
    
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
            ride.assigned_by = request.user
            ride.save()

            message = f"""
            Hello {ride.customer.customer_name},

            Thank you for choosing Ridexpress!

            We’re happy to confirm your booking:

            Booking ID: {ride.company_format}
            Pickup Date & Time: {ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}
            Pickup Location: {ride.source}
            Drop-off Location: {ride.destination}
            Cab Details: {ride.driver.name} - {ride.driver.vehicle.Vehicle_Number} 

            If you have any changes or need further assistance, feel free to reach out to us at +91 6366463555 or reply to this message.

            We look forward to serving you!

            Best regards,
            Ridexpress
            support@ridexpress.in
            ridexpress.in
            """

            payload = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                "campaignName": "booking_update",
                "destination": ride.customer.phone_number,
                "userName": "Ridexpress",
                "templateParams": [
                    str(ride.customer.customer_name),
                    str(ride.company_format),
                    f"{ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}",
                    str(ride.source),
                    str(ride.destination),
                    f"{ride.driver.name} - {ride.driver.vehicle.Vehicle_Number}"  
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
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Driver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)

def advanceassign_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver_id = data.get('driver_id')  
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)  
            driver = Driver.objects.get(company_format=driver_id)  
            ride.driver = driver  
            ride.ride_status = 'assignlaterbookings'
            ride.assigned_by=request.user
            ride.save()
            message = f"""
            Hello {ride.customer.customer_name},

            Thank you for choosing Ridexpress!

            We’re happy to confirm your booking:

            Booking ID: {ride.company_format}
            Pickup Date & Time: {ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}
            Pickup Location: {ride.source}
            Drop-off Location: {ride.destination}
            Cab Details: {ride.driver.name} - {ride.driver.vehicle.Vehicle_Number} 

            If you have any changes or need further assistance, feel free to reach out to us at +91 6366463555 or reply to this message.

            We look forward to serving you!

            Best regards,
            Ridexpress
            support@ridexpress.in
            ridexpress.in
            """

            payload = {
                "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
                "campaignName": "booking_update",
                "destination": ride.customer.phone_number,
                "userName": "Ridexpress",
                "templateParams": [
                    str(ride.customer.customer_name),
                    str(ride.company_format),
                    f"{ride.pickup_date.strftime('%Y-%m-%d')} {ride.pickup_time.strftime('%H:%M')}",
                    str(ride.source),
                    str(ride.destination),
                    f"{ride.driver.name} - {ride.driver.vehicle.Vehicle_Number}"  
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
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Driver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)


def download_vehicle_documents(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    image_fields = [
        vehicle.registration_certificate,
        vehicle.fc_certificate,
        vehicle.insurance_policy,
        vehicle.tax_details,
        vehicle.permit_details,
        vehicle.emission_test,
    ]

    if not any(image_fields):
        messages.error(request, "No documents found for this owner.") 
        return HttpResponse(status=404)

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={vehicle.company_format}_documents.zip'
    
    folder_name = vehicle.company_format 

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field and os.path.exists(field.path):
                file_path = field.path
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, os.path.join(folder_name, file_name))
    
    return response

def download_owner_documents(request, owner_id):
    owner = get_object_or_404(VehicleOwner, pk=owner_id)

    image_fields = [
        owner.identity,
        owner.address_proof,
        owner.image,
    ]

    if not any(image_fields):
        messages.error(request, "No documents found for this owner.") 
        return HttpResponse(status=404)  

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={owner.company_format}_documents.zip'

    folder_name = owner.company_format  

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field and os.path.exists(field.path):
                file_path = field.path
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, os.path.join(folder_name, file_name))

    return response

def download_driver_documents(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)

    image_fields = [
        driver.profile_image,
        driver.address_proof,
        driver.police_clearance,
        driver.driving_license,
    ]

    if not any(image_fields):
        messages.error(request, "No documents found for this owner.") 
        return HttpResponse(status=404)  

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={driver.company_format}_documents.zip'
    
    folder_name = driver.company_format  

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field and os.path.exists(field.path):
                file_path = field.path
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, os.path.join(folder_name, file_name))
    
    return response

def verify_vehicle(request):
    vehicle_id = request.GET.get('vehicle_id')
    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    owner = vehicle.owner
    
    if owner.verification_status != 'verified':
        return JsonResponse({'verified': False, 'message': 'Owner is not verified'})

    if vehicle.verification_status != 'verified':
        vehicle.verification_status = 'verified'
        vehicle.verified_on = timezone.now()
        vehicle.save()
        message = f"""
        Hello {vehicle.owner.name},
        Thank you for choosing Ridexpress,
        We are pleased to inform you that your vehicle profile has been successfully verified!:
        Attachment ID: {vehicle.company_format}
        Cab Details: {vehicle.Vehicle_Number} - {vehicle.model.brand.category.category_name} - {vehicle.model.brand.brand_name} - {vehicle.model.model_name}

        If you have any changes or need further assistance, feel free to reach out to us at +91 6366463555 or reply to this message.

        We look forward to serving you!

        Best regards,
        Ridexpress
        support@ridexpress.in
        ridexpress.in
        """

        payload = {
            "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2ZTUxNDg4NzJjYjU0MGI2ZjA2YTRmYyIsIm5hbWUiOiJSaWRleHByZXNzIiwiYXBwTmFtZSI6IkFpU2Vuc3kiLCJjbGllbnRJZCI6IjY2ZTUxNDg3NzJjYjU0MGI2ZjA2YTRlZSIsImFjdGl2ZVBsYW4iOiJCQVNJQ19NT05USExZIiwiaWF0IjoxNzI2Mjg5MDMyfQ.vEzcFg1Iyt1Qt5zk7Bcsm_HwxLLJrcap_slve0OpOog",
            "campaignName": "attachment_details",
            "destination": vehicle.owner.phone_number,
            "userName": "Ridexpress",
            "templateParams": [
                str(vehicle.owner.name),
                str(vehicle.company_format),
                f"{vehicle.Vehicle_Number} - {vehicle.model.brand.category.category_name} - {vehicle.model.brand.brand_name} - {vehicle.model.model_name}"
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

        return JsonResponse({'verified': True})
    return JsonResponse({'verified': False})