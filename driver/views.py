import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from superadmin.models import Customer,Vehicle,Driver,RideDetails,Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# @login_required(login_url='login')

@login_required(login_url='login')
def driverindex(request):
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
    return render(request,'driver/index.html',context)



@login_required(login_url='login')
def assigned_rides_view(request):
    try:
        # Get the profile associated with the logged-in user
        profile = Profile.objects.get(user=request.user)
        
        if profile.type == 'driver':
            # Get the driver that matches the profile's phone number, email, etc.
            driver = Driver.objects.get(phone_number=profile.phone_number, email=request.user.email)
            
            # Filter rides assigned to this driver
            statuses = ['assignbookings', 'assignlaterbookings', 'ongoingbookings', 'completedbookings']
            assigned_rides = RideDetails.objects.filter(ride_status__in=statuses, driver=driver)
        else:
            assigned_rides = RideDetails.objects.none()
    except (Profile.DoesNotExist, Driver.DoesNotExist):
        # If the profile or driver doesn't exist, return no rides
        assigned_rides = RideDetails.objects.none()

    context = {
        'assigned_rides': assigned_rides
    }
    return render(request, 'driver/driverassigned_rides.html', context)


# class assigned_rides_view(ListView):
#     model = RideDetails
#     template_name = "driver/driverassigned_rides.html"

#     def get_queryset(self):
#         # Get only rides that are assigned
#         return RideDetails.objects.filter(ride_status='assignbookings').select_related('driver')
# 
#  
@login_required(login_url='login')
@csrf_exempt
def start_ride(request):
    if request.method == 'POST':  

        try:
            data = json.loads(request.body)
            ride_id = data.get('ride_id')

            ride = RideDetails.objects.get(ride_id=ride_id)
            driver = ride.driver
            driver.driver_status = 'occupied'
            driver.save()
            ride.ride_status = 'ongoingbookings'
            ride.save()
            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

@login_required(login_url='login')
def stop_ride(request):
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
            ride_id = data.get('ride_id')
            ride = RideDetails.objects.get(ride_id=ride_id)
            driver = ride.driver
            driver.number_of_rides += 1
            driver.driver_status = 'free'
            driver.save()
            customer = ride.customer
            if customer:  # Ensure customer exists
                customer.total_rides += 1
                customer.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'Customer not found.'}, status=404)

            ride.ride_status = 'completedbookings'
            ride.save()
            # driver.save(update_fields=['number_of_rides', 'driver_status'])
            ride.ride_status = 'completedbookings'
            ride.save()
            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        

# @login_required
# def driver_profile_view(request):
#     # Get the driver profile for the logged-in user
#     profile = get_object_or_404(Profile, user=request.user, type='driver')
    
#     # Get the driver details associated with the logged-in user
#     drivers = get_object_or_404(Driver, email=request.user.email)  # Assuming email is used to link User and Driver

#     context = {
#         'profile': profile,
#         'drivers': drivers,  # Pass the single driver instance to the context
#     }

#     return render(request, 'driver/driverprofile.html', context)

@login_required
def driver_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='driver')
    return render(request, 'driver/app-profile.html', {'profile': profile})

