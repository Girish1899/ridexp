from datetime import date
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render
from superadmin.models import Brand, BrandHistory,Category, CategoryHistory, CommissionHistory, CommissionType, CustomerHistory, DriverHistory,Model, ModelHistory, Pricing, PricingHistory, ProfileHistory, RideDetails,Profile, RidetypeHistory,User, VehicleHistory, VehicleOwnerHistory,VehicleType,Customer,Driver,VehicleOwner,Ridetype,Vehicle, VehicleTypeHistory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,View,DetailView
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse

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

# category#################################################
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


# brand ########################
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

# model ########################
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

# vehicletype ############################
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

# ridetype #########################################
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

# users###################################
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

# customer###################################
@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerList(ListView):
    model = Customer
    template_name = "adminuser/view_customer.html"

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

# owner ################################
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

# vehicle ######################
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

# driver ################################
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

# add bookings inside superadmin##########################################

class AddRide(TemplateView):
    template_name = "adminuser/add_ride.html"
    
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
                # Create new customer
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

            # Ensure objects exist in database before saving
            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            model = Model.objects.get(model_id=model_id)

            # Determine ride status based on pickup date
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            # Use the next company format for the ride
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
    template_name = "adminuser/view_ride.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        today = date.today()
        # Update ride status for rides with a past pickup date
        past_rides = RideDetails.objects.filter(pickup_date__lt=today, ride_status='currentbookings')
        past_rides.update(ride_status='pendingbookings')
        
        # Fetch rides with a pickup date of today and status as current bookings
        current_rides = RideDetails.objects.filter(ride_status='currentbookings', pickup_date=today)
        
        return current_rides

#################################### advance bookings ###########################################

@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvanceBookingsList(ListView):
    model = RideDetails
    template_name = "adminuser/advance_bookings.html"  # Ensure you create this template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        today = date.today()
        
        # Update ride status for rides where the pickup date is today
        today_rides = RideDetails.objects.filter(pickup_date=today, ride_status='advancebookings')
        today_rides.update(ride_status='currentbookings')
        
        # Fetch rides with a pickup date greater than today and status as advance bookings
        advance_rides = RideDetails.objects.filter(ride_status='advancebookings', pickup_date__gt=today)
        
        return advance_rides
    
##############################################################################################################   
@method_decorator(login_required(login_url='login'), name='dispatch')
class PendingBookingsList(ListView):
    model = RideDetails
    template_name = "adminuser/pending_bookings.html"  # Ensure you create this template

    def get_queryset(self):
        today = date.today()
        return RideDetails.objects.filter(ride_status='pendingbookings', pickup_date__lt=today)
    
# assigned ride list##################################################################################################
@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "adminuser/assigned_rides.html"

    def get_queryset(self):
        # Get only rides that are assigned
        return RideDetails.objects.filter(Q(ride_status='assignbookings')).select_related('driver')

# ongoing rides########################################################################################################
class OngoingRideList(ListView):
    model = RideDetails
    template_name = "adminuser/ongoing_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='ongoingbookings') 
    
# completed rides########################################################################################################
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "adminuser/completed_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='completedbookings') 
    
def completed_bookings_filter(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        bookings = RideDetails.objects.filter(booking_datetime__range=[start_date, end_date])
        data = serialize('json', bookings, use_natural_primary_keys=True, use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid date range'}, status=400)
    
# invoice rides########################################################################################################

class InvoiceView(DetailView):
    model = RideDetails
    template_name = 'adminuser/invoice.html'
    context_object_name = 'ride'
    
    def get_object(self):
        ride_id = self.kwargs.get("ride_id")
        return get_object_or_404(RideDetails, ride_id=ride_id)  

# @method_decorator(login_required(login_url='login'), name='dispatch')
# class profile(TemplateView):
#     template_name = 'adminuser/app-profile.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             user_id = self.request.session.get('user_id')
#             userlist = User.objects.filter(id=user_id)
#         except:
#             userlist = User.objects.filter(id=user_id)
            
#         context['userlist']= list(userlist)
#         return context

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
            # Simple validation
            if username and password:
                user.username = username
                user.set_password(password)
                user.save()
                #user = authenticate(username=user.username, password=password)
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
    
##################    cancel booking    #################################################################### 
@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "adminuser/view_cancelbookings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        # Pass a sample ride_id or adjust based on your logic
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='cancelledbookings') 