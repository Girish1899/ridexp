from datetime import date, datetime,time
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


# Create your views here.

class regcustomer(TemplateView):
    template_name = "customer/register.html"

    def post(self, request):
        # Fetch the last customer entry
        last_cust = Customer.objects.all().order_by('-customer_id').first()

        # Calculate the next company_format value
        if last_cust:
            last_company_format = int(last_cust.company_format.replace('CUST', ''))
            next_company_format = f'CUST{last_company_format + 1:02}'
        else:
            next_company_format = 'CUST01'

        # Retrieve form data
        customer_name = request.POST['customer_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        status = request.POST['status']

        # Create and save the new customer
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

class custlogin(TemplateView):
    template_name = "customer/custlogin.html"

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        print("Received phone number:", phone_number) 
        print("Received password:", password) 

        try:
            customer = Customer.objects.get(phone_number=phone_number)
            print("Customer found:", customer)  

            if password == customer.password:
                print("Password matched.")  # Debug: log password match
                request.session['customer_id'] = customer.customer_id
                redirect_url = reverse('cusaddbooking')
                return JsonResponse({'success': True, 'redirect_url': redirect_url})
            else:
                print("Password mismatch.")
                return JsonResponse({'success': False, 'message': 'Phone number or password does not match.'})

        except Customer.DoesNotExist:
            print("Customer does not exist.")  
            return JsonResponse({'success': False, 'message': 'Phone number or password does not match.'})
        
def cuslogout_view(request):
    logout(request)
    request.session.flush()
    return redirect('custlogin')


def customer_profile(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('custlogin')  # Redirect to login if customer is not logged in

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

            ride_type_id = request.POST.get('ridetype')
            source = request.POST.get('source')
            destination = request.POST.get('destination')
            pickup_date = request.POST.get('pickup_date')
            pickup_time = request.POST.get('pickup_time')
            category = request.POST.get('category')
            total_fare = request.POST.get('total_fare')
            ridetype_name = request.POST.get('ridetype', '').strip()
            slots = determine_time_slot(pickup_time)
            customer_notes = request.POST.get('customer_notes')

            # Split category_value to get the category name
            category_name = category.split('|')[0]
            try:
                category_id = Category.objects.get(category_name=category_name)
            except Category.DoesNotExist:
                return JsonResponse({'status': 'Error', 'message': f'Category {category_name} does not exist.'})

            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            car_type_name = category.split('|')[1]

            # Updated logic to include ridetype in pricing instance retrieval
            try:
                pricing_instance = Pricing.objects.get(
                    category=category_id,
                    car_type=car_type_name,
                    ridetype=ridetype,  # Include ridetype in the query
                    slots=slots,
                )
            except Pricing.DoesNotExist:
                return JsonResponse({"status": "Error", "message": "Pricing information for the selected category, car type, and ride type does not exist."})

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

            # Create and save ride details
            ride_details = RideDetails.objects.create(
                company_format=next_company_format,
                customer=customer,
                ridetype=ridetype,
                category=category_id,
                source=source,
                destination=destination,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                total_fare=total_fare,
                pricing = pricing_instance, # Set the Pricing instance
                customer_notes=customer_notes,
                ride_status=ride_status,
            )
            
            # Send WhatsApp notification
            whatsapp = {
                "apiKey": "",
                "campaignName": "newbooking_confirmation_local",
                "destination": customer.phone_number,
                "userName": "Deepam Taxi",
                "templateParams": [
                    customer.customer_name,
                    next_company_format,
                    date.today(),
                    datetime.now().strftime('%H:%M'),
                    source,
                    destination,
                    f"{pickup_date} {pickup_time}",
                    total_fare
                ],
                "source": "new-landing-page form",
                "media": {},
                "buttons": [],
                "carouselCards": [],
                "location": {}
            }
            
            gateway_url = "https://backend.aisensy.com/campaign/t1/api/v2"
            try:
                response = requests.post(gateway_url, json=whatsapp)
                if response.status_code == 200:
                    print("Message sent successfully")
                else:
                    print(f"Failed to send message. Status code: {response.status_code}")
                    print(response.text)  # Print response body for debugging
            except requests.RequestException as e:
                print(f"Error sending message: {e}")
            
            return JsonResponse({'status': 'Success', 'message': 'Ride details added successfully'})
    
        except IntegrityError as e:
            print("IntegrityError:", e)
            return JsonResponse({'status': 'Error', 'message': 'Failed to add ride details due to a data integrity error.'})
        
        except Exception as e:
            print(f"Exception: {e}")
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

class customerGetRidePricingDetails(APIView):
    def post(self, request):
        import googlemaps
        from decimal import Decimal
        from django.http import JsonResponse
        from datetime import datetime
        
        ridetype_id = request.POST['ridetype']
        source = request.POST['source']
        destination = request.POST['destination']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']
        time_slot = request.POST['time_slot']  # Get the time slot from the request
        
        try:
            ridetype = Ridetype.objects.get(ridetype_id=ridetype_id)
        except Ridetype.DoesNotExist:
            return Response({'error': 'Ride type not found'}, status=400)
        api_key = 'AIzaSyAXVR7rD8GXKZ2HBhLn8qOQ2Jj_-mPfWSo'
        
        # Initialize the Google Maps client with your API key
        gmaps = googlemaps.Client(key=api_key)

        try:
            result = gmaps.distance_matrix(
                origins=[source],
                destinations=[destination],
                mode="driving",
                departure_time=datetime.now()
            )
            print(result)

            # Check if the response status is OK
            if result['status'] == 'OK' and result['rows'][0]['elements'][0]['status'] == 'OK':
                distance = result['rows'][0]['elements'][0]['distance']['value'] / 1000
            else:
                # Handle cases where the distance is not found
                if result['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
                    return Response({'error': 'Address not found'}, status=404)
                else:
                    return Response({'error': 'Unable to retrieve distance'}, status=500)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
        if distance is None:
            return Response({'error': 'Unable to retrieve distance'}, status=500)

        print("distance: ", distance)

        # Initialize the costs dictionary
        pricing_dict = {}

        # Fetch all pricing details filtered by the selected time slot
        pricing_details = Pricing.objects.select_related('category').filter(
            ridetype=ridetype,  # Filter by ridetype
            slots=time_slot
        )
       
        # Organize pricing data by category and car type
        pricing_dict = {}
        for price in pricing_details:
            category_name = price.category.category_name  # Remove spaces and convert to lowercase
            car_type = price.car_type.lower()  # 'ac' or 'non ac'

            if category_name not in pricing_dict:
                pricing_dict[category_name] = {}

            # Calculate cost based on distance and pricing details
            price_per_km_decimal = Decimal(str(price.price_per_km))
            permit_decimal = Decimal(str(price.permit))
            toll_price_decimal = Decimal(str(price.toll_price))
            driver_beta_decimal = Decimal(str(price.driver_beta))

            temp_cost = Decimal(distance) * price_per_km_decimal
            temp_cost += permit_decimal + toll_price_decimal + driver_beta_decimal
            category_cost = round(temp_cost, 0)

            pricing_dict[category_name][car_type] = {
                'distance_km': distance,
                'cost': category_cost,
                'permit': permit_decimal,
                'toll': toll_price_decimal,
                'beta': driver_beta_decimal,
                'category': price.category.category_name,
            }
        
        print("Pricing Dict: ", pricing_dict)
        return JsonResponse({'costs': pricing_dict})

    