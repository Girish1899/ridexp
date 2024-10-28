import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as logout
from superadmin.models import Customer,Vehicle,Driver,RideDetails,Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt


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

class driverlogin(TemplateView):
    template_name = "driver/driver-login.html"

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        print("Received phone number:", phone_number) 
        print("Received password:", password)


        try:
            driver = Driver.objects.get(phone_number=phone_number)
            request.session['driver_id'] = driver.driver_id

            if driver.password == password:  
                return JsonResponse({'success': True, 'redirect_url': 'driverindex '})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid password.'})

        except Driver.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Phone number not found. Please register.'})

def driverlogout_view(request):
    logout(request)
    request.session.flush()
    return redirect('driver_login')


def assigned_rides_view(request):
        
    driver_id = request.session.get('driver_id')

    if driver_id:
        driver = Driver.objects.get(driver_id=driver_id)
        statuses = ['assignbookings', 'assignlaterbookings', 'ongoingbookings', 'completedbookings']
        assigned_rides = RideDetails.objects.filter(ride_status__in=statuses, driver=driver)
    else:
        assigned_rides = RideDetails.objects.none()

    context = {
        'assigned_rides': assigned_rides
    }
    return render(request, 'driver/driverassigned_rides.html', context)



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
            if customer:  
                customer.total_rides += 1
                customer.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'Customer not found.'}, status=404)

            ride.ride_status = 'completedbookings'
            ride.save()
            ride.ride_status = 'completedbookings'
            ride.save()
            return JsonResponse({'status': 'success'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ride not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        


def driver_profile_view(request):
    driver_id = request.session.get('driver_id')
    if not driver_id:
        return redirect('driver_login')  

    driver = get_object_or_404(Driver, driver_id=driver_id)
    return render(request, 'driver/app-profile.html', {'driver': driver})

