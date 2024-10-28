from datetime import date, timezone
import json
from django.shortcuts import render

import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from rest_framework.response import Response
from rest_framework import status
from superadmin.models import Brand, Category, Model, Profile, RideDetails,Customer,Driver, RideDetailsHistory,Ridetype,Vehicle,User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.decorators import method_decorator

@login_required(login_url='login')
def qindex(request):
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
    return render(request,'quality/index.html',context)


def global_fetch_customer_details(request):
    phone_number = request.GET.get('phone_number', None)
    if phone_number:
        try:
            customer = Customer.objects.get(phone_number=phone_number)
            print("customer:",customer)
            customer_details = {
                'id': customer.customer_id,  
                'name': customer.customer_name,
                'email': customer.email,
                'address': customer.address
            }
            return JsonResponse({'success': True, 'customer': customer_details})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

class AddRide(TemplateView):
    template_name = "quality/add_ride.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['customerlist'] = Customer.objects.all()
        context['ridetypelist'] = Ridetype.objects.all()
        context['catlist'] = Category.objects.filter(category_status='active')
        context['blist'] = Brand.objects.filter(status='active')
        context['modellist'] = Model.objects.filter(status='active')
        
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
            company_format = request.POST['company_format']
            ride_type_id = request.POST['ridetype']
            source = request.POST['source']
            destination = request.POST['destination']
            pickup_date = request.POST['pickup_date']
            pickup_time = request.POST['pickup_time']
            model_id = request.POST['model']
            total_fare = request.POST['total_fare']
            customer_id = request.POST['customer']
            customer_notes = request.POST['customer_notes']
            ride_status = request.POST['ride_status']
            phone_number = request.POST['phone_number']
            customer_name = request.POST['customer_name']
            email = request.POST['email']
            address = request.POST['address']

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
                    address=address,
                    status='active',
                    created_by=request.user,
                    updated_by=request.user
                )
                customer.save()
                customer_id = customer.customer_id

            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            model = Model.objects.get(model_id=model_id)

            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            next_company_format = self.get_context_data()['next_company_format']
            
            ride_details = RideDetails(
                company_format=next_company_format,
                customer=customer,
                ridetype=ridetype,
                model=model,
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
                updated_by=request.user
            )
            ride_details.save()
            
            return JsonResponse({'status': "Success", 'message': 'Ride details added successfully'})
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': f'Customer with ID {customer_id} does not exist.'})
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': str(e)})
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class RideList(ListView):
    model = RideDetails
    template_name = "quality/view_ride.html"

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
    template_name = "quality/advance_bookings.html"  

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
    template_name = "quality/pending_bookings.html"  

    def get_queryset(self):
        today = date.today()
        return RideDetails.objects.filter(ride_status='pendingbookings', pickup_date__lt=today)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "quality/assigned_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='assignbookings')).select_related('driver')

@method_decorator(login_required(login_url='login'), name='dispatch')
class OngoingRideList(ListView):
    model = RideDetails
    template_name = "quality/ongoing_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='ongoingbookings') 
    

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
    template_name = 'quality/edit_ride.html'
  
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
    template_name = 'superadmin/history_ride.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride_id = self.kwargs['ride_id']
        ride = get_object_or_404(RideDetails, ride_id=ride_id)
        history = RideDetailsHistory.objects.filter(ride_id=ride_id).order_by('updated_on')
        context['ride'] = ride
        context['history'] = history
        return context
    


@login_required
def quality_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='quality')
    return render(request, 'quality/app-profile.html', {'profile': profile})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
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
            ride.assigned_by=request.user
            ride.save()

            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Driver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "quality/completed_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='completedbookings') 
    
def quality_comments(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quality_comments = data.get('quality_comments')
        ride_id = data.get('ride_id')

        
        ride = RideDetails.objects.get(ride_id=ride_id)
        ride.quality_comments = quality_comments
        ride.verified_by =request.user
        ride.save()

        response_data = {
            'quality_comments': ride.quality_comments,
            'verified_by': ride.verified_by.username,  
            'verified_on': ride.verified_on.strftime('%Y-%m-%d') 
        }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "quality/view_cancelbookings.html"

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
            ride.cancelled_by =request.user
            ride.save()

            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'essage': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'essage': str(e)}, status=500)

    return JsonResponse({'status': 'failed'}, status=400)

class InvoiceView(DetailView):
    model = RideDetails
    template_name = 'quality/invoice.html'
    context_object_name = 'ride'
    
    def get_object(self):
        ride_id = self.kwargs.get("ride_id")
        return get_object_or_404(RideDetails, ride_id=ride_id)

