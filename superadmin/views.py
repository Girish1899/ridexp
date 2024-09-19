from datetime import date, datetime,time
from decimal import Decimal
import json
import os
from django.http import JsonResponse
from django.db import IntegrityError
import requests
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from .models import Accounts, Brand, BrandHistory,Category, CategoryHistory, DailyVehicleComm,Color, ColorHistory, CommissionHistory, CommissionType, CustomerHistory, DriverHistory,Model, ModelHistory, Pricing, PricingHistory, Profile, ProfileHistory, RideDetails, RideDetailsHistory, RidetypeHistory, Transmission, TransmissionHistory,User, VehicleHistory, VehicleOwnerHistory,VehicleType,Customer,Driver,VehicleOwner,Ridetype,Vehicle, VehicleTypeHistory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.core.exceptions import ObjectDoesNotExist
from django.urls import path
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import date, timedelta
import zipfile
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import logging
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models import OuterRef, Subquery, Max
from rest_framework.response import Response

def report(request):
    report_type = request.GET.get('report_type', 'daily')
    selected_date_str = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
    daily_data = []

    # Determine the date format based on the report type
    if report_type == 'monthly':
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m').date()
        except ValueError:
            selected_date = date.today().replace(day=1)  # default to first day of current month
    elif report_type == 'yearly':
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y').date()
        except ValueError:
            selected_date = date.today().replace(month=1, day=1)  # default to first day of current year
    else:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()

    rides = RideDetails.objects.none()
    total_fare = 0
    total_rides = 0
    completed = 0
    cancelled = 0
    outstation = 0
    airportpickup = 0
    airportdrop = 0
    daily_data = []

    if report_type == 'daily':
        rides = RideDetails.objects.filter(pickup_date=selected_date)
    elif report_type == 'weekly':
        # Get start and end dates of the week
        week_start = selected_date - timedelta(days=selected_date.weekday())
        week_end = week_start + timedelta(days=6)
        rides = RideDetails.objects.filter(pickup_date__range=[week_start, week_end])
         # Group rides by day and calculate ride status counts
        daily_data = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_rides = rides.filter(pickup_date=day)

            # Initialize counters
            day_outstation = 0
            day_airportpickup = 0
            day_airportdrop = 0

            for ride in day_rides:
                ridetype_name = ride.ridetype.name.lower().replace(' ', '')
                if ridetype_name == 'outstation':
                    day_outstation += 1
                elif ridetype_name == 'airportpickup':
                    day_airportpickup += 1
                elif ridetype_name == 'airportdrop':
                    day_airportdrop += 1

            day_data = {
                'date': day,
                'total_rides': day_rides.count(),
                'completed_rides': day_rides.filter(ride_status='completedbookings').count(),
                'cancelled_rides': day_rides.filter(ride_status='cancelledbookings').count(),
                'ongoing_rides': day_rides.filter(ride_status='ongoingbookings').count(),
                'outstation': day_outstation,
                'airportpickup': day_airportpickup,
                'airportdrop': day_airportdrop,
            }
            daily_data.append(day_data)

    elif report_type == 'monthly':
        # Get start and end dates of the month
        month_start = selected_date.replace(day=1)
        next_month = (month_start + timedelta(days=31)).replace(day=1)
        month_end = next_month - timedelta(days=1)
        rides = RideDetails.objects.filter(pickup_date__range=[month_start, month_end])
    elif report_type == 'yearly':
        # Get start and end dates of the year
        year_start = selected_date.replace(month=1, day=1)
        year_end = selected_date.replace(month=12, day=31)
        rides = RideDetails.objects.filter(pickup_date__range=[year_start, year_end])

    total_fare = rides.aggregate(total_fare=Sum('total_fare'))['total_fare'] or 0
    total_rides = rides.count()
    completed = rides.filter(ride_status='completedbookings').count()
    cancelled = rides.filter(ride_status='cancelledbookings').count()
    
    # Calculate the counts for outstation, airportpickup, and airportdrop for non-weekly reports
    if report_type != 'weekly':
        for ride in rides:
            ridetype_name = ride.ridetype.name.lower().replace(' ', '')
            if ridetype_name == 'outstation':
                outstation += 1
            elif ridetype_name == 'airportpickup':
                airportpickup += 1
            elif ridetype_name == 'airportdrop':
                airportdrop += 1

    return render(request, 'superadmin/report.html', {
        'rides': rides,
        'total_fare': total_fare,
        'completed' : completed,
        'cancelled' : cancelled,
        'total_rides': total_rides,
        'selected_date': selected_date_str,
        'report_type': report_type,
        'daily_data': daily_data,
        'outstation' : outstation,
        'airportpickup' : airportpickup,
        'airportdrop' : airportdrop,
    })

@login_required(login_url='login')
def index(request):
    cust_count = Customer.objects.count()
    driver_count = Driver.objects.count()
    booking_count = RideDetails.objects.count()
    vehicle_count = Vehicle.objects.count()
    # today_entries = Ridetype.objects.filter(YOUR_DATE_FIELD__date=timezone.now().date())
    # today_booking_count = RideDetails.objects.filter(YOUR_DATE_FIELD__date=timezone.now().date()).count()

    context = {
        'cust_count': cust_count,
        'driver_count': driver_count,
        'booking_count': booking_count,
        'vehicle_count': vehicle_count,
    }
    return render(request,'superadmin/index.html', context)

def get_weekly_data(request):
    # Sample data, replace this with actual database query and calculations
    weekly_data = [
        {"day": "Mon", "total_after_gst": 1000, "company_share": 200},
        {"day": "Tue", "total_after_gst": 1500, "company_share": 300},
        {"day": "Wed", "total_after_gst": 900, "company_share": 180},
        {"day": "Thu", "total_after_gst": 1100, "company_share": 220},
        {"day": "Fri", "total_after_gst": 1600, "company_share": 320},
        {"day": "Sat", "total_after_gst": 1300, "company_share": 260},
        {"day": "Sun", "total_after_gst": 1400, "company_share": 280}
    ]

    # Calculate profit
    for data in weekly_data:
        data['profit'] = data['total_after_gst'] - data['company_share']

    return JsonResponse(weekly_data, safe=False)


# login #####################################
class login(TemplateView,APIView):
    template_name = "login.html" 


class forgot_password(TemplateView):
    template_name = "website/forgot-password.html" 


class robots(TemplateView):
    template_name = "robots.txt" 



class sitemap(TemplateView):
    template_name = "sitemap.xml" 



class about_blog(TemplateView):
    template_name = "website/about.html" 




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
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

    
# brand ########################
# @method_decorator(login_required(login_url='login'), name='dispatch')
# def check_brand(request):
#     brand_name = request.GET.get('brand_name')
#     category_id = request.GET.get('category')

#     if not brand_name or not category_id:
#         return JsonResponse({'error': 'Both brand_name and category are required.'}, status=400)

#     try:
#         category = Category.objects.get(pk=category_id)
#     except Category.DoesNotExist:
#         return JsonResponse({'error': 'Invalid category ID.'}, status=400)

#     # Check if a brand with the same name exists in the specified category
#     brand_exists = Brand.objects.filter(brand_name=brand_name, category=category).exists()
#     data = {'exists': brand_exists}

#     return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addbrand(TemplateView):
    template_name = "superadmin/add_brand.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')
        brands = Brand.objects.all().values('category_id', 'brand_name')
        context['catlist'] = catlist
        context['brands'] = brands
        return context

    def post(self, request):
        user_type = self.request.session.get('user_type')
        if user_type != "Superadmin":
            return redirect('login')
        
        category = request.POST['category']
        brand_name = request.POST['brand_name']
        status = request.POST['status']

        brand = Brand()
        brand.category = Category.objects.get(category_id=category)
        brand.brand_name = brand_name
        brand.status = status
        brand.created_by = request.user
        brand.updated_by = request.user
        brand.save()
        return JsonResponse({'status': "Success"})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class BrandListView(ListView):

    model = Brand
    template_name = "superadmin/view_brand.html"

    def get(self, request, *args, **kwargs):
        user_typ = self.request.session.get('user_type')
        if user_typ !="Superadmin":
            return redirect('login')
        else:
            return super().get(request, *args, **kwargs)
        

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteBrand(View):
    def  get(self, request):
        
        brand_id = request.GET.get('brand_id', None)
        Brand.objects.get(brand_id=brand_id).delete()
        data = {
            'deleted': True
            }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')   
class EditBrand(TemplateView):
    template_name = 'superadmin/edit_brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')  # Filter only active categories
        try:
            context['brand_id'] = self.kwargs['id']
            brandlist = Brand.objects.filter(brand_id=context['brand_id'])
        except:
            brandlist = Brand.objects.filter(brand_id=context['brand_id'])

        brands = Brand.objects.all().values('category_id', 'brand_name')

        context.update({
            'brandlist': list(brandlist),
            'catlist': list(catlist),
            'brands': brands
        })
        return context    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateBrand(APIView):  
    def post(self, request):
        brand_id = request.POST['brand_id']
        brand = get_object_or_404(Brand, brand_id=brand_id)
        original_brand_status = brand.status

        # Update the brand with new data
        brand.brand_name = request.POST['brand_name']
        brand.category_id = request.POST['category']
        brand.status = request.POST['status']
        brand.updated_by = request.user
        brand.save()

        # Create a BrandHistory entry after updating the brand
        BrandHistory.objects.create(
            brand_id=brand.brand_id,
            category=brand.category,
            brand_name=brand.brand_name,
            status=brand.status,
            created_on=brand.created_on,
            updated_on=brand.updated_on,
            created_by=brand.created_by.username if brand.created_by else None,
            updated_by=request.user.username
        )

        if original_brand_status != brand.status:
            models = brand.models.all() 
            for model in models:
                if model.status != brand.status:
                    model.status = brand.status
                    model.save()

                    vehicles = model.vehicles.all() 
                    for vehicle in vehicles:
                        if vehicle.vehicle_status != brand.status:
                            vehicle.vehicle_status = brand.status
                            vehicle.save()

        return JsonResponse({'success': True}, status=200)

class BrandHistoryView(TemplateView):
    template_name = 'superadmin/history_brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_id = self.kwargs['brand_id']
        brand = get_object_or_404(Brand, brand_id=brand_id)
        history = BrandHistory.objects.filter(brand_id=brand_id).order_by('updated_on')
        context['brand'] = brand
        context['history'] = history
        return context  
    
@csrf_exempt
def toggle_brand_status(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        new_status = request.POST.get('status')
        try:
            brand = Brand.objects.get(pk=brand_id)
            brand.status = new_status
            brand.save()
            BrandHistory.objects.create(
            brand_id=brand.brand_id,
            category=brand.category,
            brand_name=brand.brand_name,
            status=brand.status,
            created_on=brand.created_on,
            updated_on=brand.updated_on,
            created_by=brand.created_by.username if brand.created_by else None,
            updated_by=request.user.username
        )
            return JsonResponse({'success': True})
        except Brand.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Brand not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})  

class ViewBrand(View):
    template_name = 'superadmin/detailview_brand.html'

    def get(self, request, brand_id):
        brandlist = get_object_or_404(Brand, pk=brand_id)
        return render(request, self.template_name, {'brandlist': brandlist})  
    
# category#################################################
@login_required(login_url='login')
def check_category(request):
    category_name = request.GET.get('category_name', None)
    categories = Category.objects.filter(category_name=category_name)
    data = {
        'exists': categories.count() > 0
    }
    return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addcategory(TemplateView):
    template_name = "superadmin/add_category.html"

    def post(self, request):
        category_name = request.POST['category_name']
        seats = request.POST['seats']
        image = request.FILES.get('image')
        category_status = request.POST['category_status']
        cat = Category(
            category_name=category_name,
            seats = seats,
            category_status=category_status,
            created_by=request.user,
            updated_by=request.user
        )
        if image:
            # Open the uploaded image
            img = Image.open(image)
            
            # Resize image to 880x350 pixels
            img = img.resize((880, 450), Image.LANCZOS)

            # Get the file extension and set the appropriate format
            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg']:
                format = 'JPEG'
            elif file_extension == '.png':
                format = 'PNG'
            elif file_extension == '.gif':
                format = 'GIF'
            else:
                format = 'JPEG'  # Default format if none of the above match

            # Save the image to an in-memory file
            img_io = BytesIO()
            img.save(img_io, format=format)
            img_content = ContentFile(img_io.getvalue(), image.name)

            # Assign the resized image to the category object
            cat.image.save(image.name, img_content, save=False)

        cat.save()
        return JsonResponse({'status': "Success"})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = "superadmin/view_category.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteCategory(View):
    def get(self, request):
        category_id = request.GET.get('category_id', None)
        Category.objects.get(category_id=category_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')   
class EditCategory(TemplateView):
    template_name = 'superadmin/edit_category.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['category_id'] = self.kwargs['id']
            catlist = Category.objects.filter(category_id=context['category_id'])
        except:
            catlist = Category.objects.filter(category_id=context['category_id'])
            
        context['catlist']= list(catlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateCategory(APIView):
    def post(self, request):
        category_id = request.POST['category_id']
        category = get_object_or_404(Category, category_id=category_id)
        original_category_status = category.category_status

        # Update the category with new data
        category.category_name = request.POST['category_name']
        category.seats = request.POST['seats']
        if 'image' in request.FILES:
            # Handle image resizing before saving
            image = request.FILES['image']
            img = Image.open(image)
            
            # Resize image to 880x350 pixels
            img = img.resize((880, 450), Image.LANCZOS)

            # Get the file extension and set the appropriate format
            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg']:
                format = 'JPEG'
            elif file_extension == '.png':
                format = 'PNG'
            elif file_extension == '.gif':
                format = 'GIF'
            else:
                format = 'JPEG'  # Default format if none of the above match

            # Save the image to an in-memory file
            img_io = BytesIO()
            img.save(img_io, format=format)
            img_content = ContentFile(img_io.getvalue(), image.name)

            # Assign the resized image to the category object
            category.image.save(image.name, img_content, save=False)
        category.category_status = request.POST['category_status']
        category.updated_by = request.user
        category.save()

        # Create a CategoryHistory entry after updating the category
        CategoryHistory.objects.create(
            category_id=category.category_id,
            category_name=category.category_name,
            seats=category.seats,
            image=category.image,
            category_status=category.category_status,
            created_on=category.created_on,
            updated_on=category.updated_on,
            created_by=category.created_by.username if category.created_by else None,
            updated_by=request.user.username
        )

        if original_category_status != category.category_status:
            brands = category.brands.all() 
            for brand in brands:
                if brand.status != category.category_status:
                    brand.status = category.category_status
                    brand.save()

                    models = brand.models.all()  
                    for model in models:
                        if model.status != category.category_status:
                            model.status = category.category_status
                            model.save()

                            vehicles = model.vehicles.all() 
                            for vehicle in vehicles:
                                if vehicle.vehicle_status != category.category_status:
                                    vehicle.vehicle_status = category.category_status
                                    vehicle.save()

        return JsonResponse({'success': True}, status=200)

class CategoryHistoryView(TemplateView):
    template_name = 'superadmin/history_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, category_id=category_id)
        history = CategoryHistory.objects.filter(category_id=category_id).order_by('updated_on')
        context['category'] = category
        context['history'] = history
        return context
    
@require_POST
def toggle_category_status(request):
    category_id = request.POST.get('category_id')
    new_status = request.POST.get('new_status')
    
    try:
        category = Category.objects.get(pk=category_id)
        category.category_status = new_status
        category.save()
        CategoryHistory.objects.create(
            category_id=category.category_id,
            category_name=category.category_name,
            seats=category.seats,
            image=category.image,
            category_status=category.category_status,
            created_on=category.created_on,
            updated_on=category.updated_on,
            created_by=category.created_by.username if category.created_by else None,
            updated_by=request.user.username
        )
        return JsonResponse({'success': True})
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Category not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})  

    # detail view category 
class ViewCategory(View):
    template_name = 'superadmin/detailview_category.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return render(request, self.template_name, {'category': category})

        

# model ########################
@method_decorator(login_required(login_url='login'), name='dispatch')
class addmodel(TemplateView):
    template_name = "superadmin/add_model.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')
        blist = Brand.objects.filter(status='active')
        models = Model.objects.all()
        context = {'catlist': list(catlist), 'blist': list(blist), 'models': models}
        return context

    def post(self, request):
        brand = request.POST['brand']
        model_name = request.POST['model_name']
        status = request.POST['status']

        model = Model(
            brand=Brand.objects.get(brand_id=brand),
            model_name=model_name,
            status=status,
            created_by=request.user,
            updated_by=request.user
        )
        model.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ModelListView(ListView):
    model = Model
    template_name = "superadmin/view_model.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteModel(View):
    def get(self, request):
        model_id = request.GET.get('model_id', None)
        Model.objects.get(model_id=model_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class EditModel(TemplateView):
    template_name = 'superadmin/edit_model.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')
        blist = Brand.objects.filter(status='active')
        try:
            context['model_id'] = self.kwargs['id']
            mlist = Model.objects.filter(model_id=context['model_id'])
        except:
            mlist = Model.objects.filter(model_id=context['model_id'])

        models = Model.objects.all().values('brand_id', 'model_name')
    
        context.update({
            'blist': list(blist),
            'catlist': list(catlist),
            'mlist': list(mlist),
            'models': models
        })
        return context    
        # context = {'blist':list(blist),'catlist':list(catlist),'mlist':list(mlist)}
        # return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateModel(APIView):
    def post(self, request):
        model_id = request.POST['model_id']
        model_name = request.POST['model_name']
        brand_id = request.POST['brand']
        status = request.POST['status']

        # Check if a model with the same name exists for the selected brand, excluding the current model
        if Model.objects.filter(brand_id=brand_id, model_name=model_name).exclude(model_id=model_id).exists():
            return JsonResponse({'success': False, 'message': "Model already exists for the selected brand."}, status=400)

        model = get_object_or_404(Model, model_id=model_id)
        original_model_status = model.status

        # Update the model with new data
        model.model_name = model_name
        model.brand_id = brand_id
        model.status = status
        model.updated_by = request.user
        model.save()

        # Create a ModelHistory entry after updating the model
        ModelHistory.objects.create(
            model_id=model.model_id,
            brand=model.brand,
            model_name=model.model_name,
            status=model.status,
            created_on=model.created_on,
            updated_on=model.updated_on,
            created_by=model.created_by.username if model.created_by else None,
            updated_by=request.user.username
        )

        # Update corresponding vehicles if the status has changed
        if original_model_status != model.status:
            vehicles = model.vehicles.all()  # Assuming vehicles is the related name for Vehicle in Model
            for vehicle in vehicles:
                if vehicle.vehicle_status != model.status:
                    vehicle.vehicle_status = model.status
                    vehicle.save()

        return JsonResponse({'success': True}, status=200)

class ModelHistoryView(TemplateView):
    template_name = 'superadmin/history_model.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_id = self.kwargs['model_id']
        model = get_object_or_404(Model, model_id=model_id)
        history = ModelHistory.objects.filter(model_id=model_id).order_by('updated_on')
        context['model'] = model
        context['history'] = history
        return context
    
@require_POST
def toggle_model_status(request):
    model_id = request.POST.get('model_id')
    new_status = request.POST.get('status')

    try:
        model = Model.objects.get(model_id=model_id)
        if new_status not in dict(Model.STATUS_CHOICES).keys():
            return JsonResponse({'success': False, 'message': 'Invalid status'}, status=400)

        # Update the model status
        model.status = new_status
        model.save()
        ModelHistory.objects.create(
            model_id=model.model_id,
            brand=model.brand,
            model_name=model.model_name,
            status=model.status,
            created_on=model.created_on,
            updated_on=model.updated_on,
            created_by=model.created_by.username if model.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True})
    except Model.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Model not found'}, status=404)   

class ViewModel(View):
    template_name = 'superadmin/detailview_model.html'

    def get(self, request, model_id):
        mlist = get_object_or_404(Model, pk=model_id)
        return render(request, self.template_name, {'mlist': mlist})         
    
# vehicletype ############################

@method_decorator(login_required(login_url='login'), name='dispatch')
class addvehicletype(TemplateView):
    template_name = "superadmin/add_vehicletype.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_vehicletype = VehicleType.objects.all().order_by('-vehicle_type_id').first()
        if last_vehicletype:
            last_company_format = int(last_vehicletype.company_format.replace('VT', ''))
            next_company_format = f'VT{last_company_format + 1:02}'
        else:
            next_company_format = 'VT01'
        context['next_company_format'] = next_company_format
        context['vehicletypes'] = VehicleType.objects.all()
        return context

    def post(self, request):
        vehicle_type_name = request.POST['vehicle_type_name']
        company_format = request.POST.get('company_format', '')

        vt = VehicleType(
            vehicle_type_name=vehicle_type_name,
            company_format=company_format,
            created_by=request.user,
            updated_by=request.user
        )
        vt.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class vehicletypeList(ListView):
    model = VehicleType
    template_name = "superadmin/view_vehicletype.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class Deletevehicletype(View):
    def get(self, request):
        vehicle_type_id = request.GET.get('vehicle_type_id', None)
        VehicleType.objects.get(vehicle_type_id=vehicle_type_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Editvehicletype(TemplateView):
    template_name = 'superadmin/edit_vehicletype.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['vehicle_type_id'] = self.kwargs['id']
            vtlist = VehicleType.objects.filter(vehicle_type_id=context['vehicle_type_id'])
        except:
            vtlist = VehicleType.objects.filter(vehicle_type_id=context['vehicle_type_id'])
            
        context['vtlist']= list(vtlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class Updatevehicletype(APIView):
    def post(self, request):
        vehicle_type_id = request.POST['vehicle_type_id']
        vehicle_type = VehicleType.objects.get(vehicle_type_id=vehicle_type_id)

        # Update the vehicle type with new data
        vehicle_type.company_format = request.POST['company_format']
        vehicle_type.vehicle_type_name = request.POST['vehicle_type_name']
        vehicle_type.updated_by = request.user
        vehicle_type.save()

        # Create another VehicleTypeHistory entry after updating the vehicle type
        VehicleTypeHistory.objects.create(
            vehicle_type_id=vehicle_type.vehicle_type_id,
            company_format=vehicle_type.company_format,
            vehicle_type_name=vehicle_type.vehicle_type_name,
            created_on=vehicle_type.created_on,
            updated_on=vehicle_type.updated_on,
            created_by=vehicle_type.created_by.username if vehicle_type.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class VehicleTypeHistoryView(TemplateView):
    template_name = 'superadmin/history_vehicletype.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_type_id = self.kwargs['vehicle_type_id']
        vehicle_type = get_object_or_404(VehicleType, vehicle_type_id=vehicle_type_id)
        history = VehicleTypeHistory.objects.filter(vehicle_type_id=vehicle_type_id)
        context['vehicle_type'] = vehicle_type
        context['history'] = history
        return context

@login_required(login_url='login')   
def check_vehicletype(request):
    vehicle_type_name = request.GET.get('vehicle_type_name', None)
    vehicletypes = VehicleType.objects.filter(vehicle_type_name=vehicle_type_name)
    data = {
        'exists': vehicletypes.count() > 0
    }
    return JsonResponse(data)


class ViewVehicletype(View):
    template_name = 'superadmin/detailview_vehicletype.html'

    def get(self, request, vehicle_type_id):
        vtlist = get_object_or_404(VehicleType, pk=vehicle_type_id)
        return render(request, self.template_name, {'vtlist': vtlist})  
    
# ridetype #########################################

@method_decorator(login_required(login_url='login'), name='dispatch')
class addridetype(TemplateView):
    template_name = "superadmin/add_ridetype.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_ridetype = Ridetype.objects.all().order_by('-ridetype_id').first()
        if last_ridetype:
            last_company_format = int(last_ridetype.company_format.replace('RT', ''))
            next_company_format = f'RT{last_company_format + 1:02}'
        else:
            next_company_format = 'RT01'
        context['next_company_format'] = next_company_format
        context['ridetypes'] = Ridetype.objects.all()
        return context

    def post(self, request):
        name = request.POST['name']
        company_format = request.POST.get('company_format', '')

        rt = Ridetype(
            name=name,
            company_format=company_format,
            created_by=request.user,
            updated_by=request.user
        )
        rt.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class ridetypeList(ListView):
    model = Ridetype
    template_name = "superadmin/view_ridetype.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class Deleteridetype(View):
    def get(self, request):
        ridetype_id = request.GET.get('ridetype_id', None)
        Ridetype.objects.get(ridetype_id=ridetype_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Editridetype(TemplateView):
    template_name = 'superadmin/edit_ridetype.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['ridetype_id'] = self.kwargs['id']
            rtlist = Ridetype.objects.filter(ridetype_id=context['ridetype_id'])
        except:
            rtlist = Ridetype.objects.filter(ridetype_id=context['ridetype_id'])
            
        context['rtlist']= list(rtlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class Updateridetype(APIView):
    def post(self, request):
        ridetype_id = request.POST['ridetype_id']
        ridetype = Ridetype.objects.get(ridetype_id=ridetype_id)

        # Update the ride type with new data
        ridetype.company_format = request.POST['company_format']
        ridetype.name = request.POST['name']
        ridetype.updated_by = request.user
        ridetype.save()

        # Create another RidetypeHistory entry after updating the ride type
        RidetypeHistory.objects.create(
            ridetype_id=ridetype.ridetype_id,
            company_format=ridetype.company_format,
            name=ridetype.name,
            created_on=ridetype.created_on,
            updated_on=ridetype.updated_on,
            created_by=ridetype.created_by.username if ridetype.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class RidetypeHistoryView(TemplateView):
    template_name = 'superadmin/history_ridetype.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ridetype_id = self.kwargs['ridetype_id']
        ridetype = get_object_or_404(Ridetype, ridetype_id=ridetype_id)
        history = RidetypeHistory.objects.filter(ridetype_id=ridetype_id).order_by('updated_on')
        context['ridetype'] = ridetype
        context['history'] = history
        return context

@login_required(login_url='login')   
def check_ridetype(request):
    name = request.GET.get('name', None)
    ridetypes = Ridetype.objects.filter(name=name)
    data = {
        'exists': ridetypes.count() > 0
    }
    return JsonResponse(data)

class ViewRidetype(View):
    template_name = 'superadmin/detailview_ridetype.html'

    def get(self, request, ridetype_id):
        rtlist = get_object_or_404(Ridetype, pk=ridetype_id)
        return render(request, self.template_name, {'rtlist': rtlist})  
    
# driver ###################################################################################

def fetch_vehicle_details(request):
    if request.method == "GET":
        vehicle_company_format = request.GET.get('vehicle_company_format')
        try:
            vehicle = Vehicle.objects.select_related(
                'model__brand__category'
            ).get(company_format=vehicle_company_format)
            response = {
                'success': True,
                'vehicle': {
                    'id': vehicle.vehicle_id,  # Ensure this is the numeric vehicle ID
                    'Vehicle_Number': vehicle.Vehicle_Number,
                    'category_name': vehicle.model.brand.category.category_name,
                    'brand_name': vehicle.model.brand.brand_name,
                    'model_name': vehicle.model.model_name,
                }
            }
        except Vehicle.DoesNotExist:
            response = {
                'success': False,
                'message': 'Vehicle not found'
            }
        return JsonResponse(response)

@login_required(login_url='login')
def check_dphonenumber(request):
    phone_number = request.GET.get('phone_number', None)
    ph = Driver.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)

class AddDriverView(TemplateView):
    template_name = "superadmin/add_driver.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_driver = Driver.objects.order_by('-driver_id').first()
        if last_driver and last_driver.company_format:
            last_company_format = int(last_driver.company_format.replace('DRIV', ''))
            next_company_format = f'DRIV{last_company_format + 1:02}'
        else:
            next_company_format = 'DRIV01'
        context['next_company_format'] = next_company_format

        # Fetch all active and verified vehicles
        all_vehicles = Vehicle.objects.filter(
            vehicle_status='active',
            verification_status='verified'
        )
        
        # Fetch all assigned vehicles
        assigned_vehicle_ids = Driver.objects.values_list('vehicle_id', flat=True)
        
        # Filter out the assigned vehicles
        unassigned_vehicles = [vehicle for vehicle in all_vehicles if vehicle.vehicle_id not in assigned_vehicle_ids]
        
        context['vehicles'] = unassigned_vehicles
        
        return context
    

    def post(self, request, *args, **kwargs):
        try:
            vehicle_id = request.POST['vehicle']
            company_format = request.POST['company_format']
            driver_name = request.POST['name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']
            pfrom_date = request.POST.get('pfrom_date', None) 
            pto_date = request.POST.get('pto_date', None) 
            dfrom_date = request.POST.get('dfrom_date', None)  
            dto_date = request.POST.get('dto_date', None)  
            profile_image = request.FILES.get('profile_image')
            address_proof = request.FILES.get('address_proof')
            police_clearance = request.FILES.get('police_clearance')
            driving_license = request.FILES.get('driving_license')
            status = request.POST['status']
            
            print(f"Vehicle ID: {vehicle_id}, Driver Name: {driver_name}")

            try:
                vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'Error', 'message': f'Vehicle with ID {vehicle_id} does not exist.'}, status=400)
            
            driver = Driver(
                vehicle=vehicle,
                company_format=company_format,
                name=driver_name,
                phone_number=phone_number,
                email=email,
                password=password,
                address=address,
                profile_image=profile_image if profile_image else None,
                address_proof=address_proof if address_proof else None,
                police_clearance=police_clearance if police_clearance else None,
                driving_license=driving_license if driving_license else None,
                pfrom_date=pfrom_date if pfrom_date else None,
                pto_date=pto_date if pto_date else None,
                dfrom_date=dfrom_date if dfrom_date else None,
                dto_date=dto_date if dto_date else None,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )
            driver.save()

            print("Driver saved successfully.")

            # Profile creation logic
            if vehicle.drive_status == 'selfdrive':
                # Ensure the Profile is created for selfdrive
                last_profile = Profile.objects.order_by('-profile_id').first()
                if last_profile and last_profile.company_format:
                    last_profile_format = int(last_profile.company_format.replace('USR', ''))
                    next_profile_format = f'USR{last_profile_format + 1:02}'
                else:
                    next_profile_format = 'USR01'

                user = User.objects.create_user(username=driver_name, email=email, password=password)
                profile = Profile.objects.create(
                    user=user,
                    phone_number=phone_number,
                    address=address,
                    type="driver",
                    status=status,
                    company_format=next_profile_format,
                    created_by=request.user,
                    updated_by=request.user
                )

                print("Profile created successfully for selfdrive.")
                
            elif vehicle.drive_status == 'otherdrive':
                # If the vehicle is driven by someone else, also create a Profile
                last_profile = Profile.objects.order_by('-profile_id').first()
                if last_profile and last_profile.company_format:
                    last_profile_format = int(last_profile.company_format.replace('USR', ''))
                    next_profile_format = f'USR{last_profile_format + 1:02}'
                else:
                    next_profile_format = 'USR01'

                user = User.objects.create_user(username=driver_name, email=email, password=password)
                profile = Profile.objects.create(
                    user=user,
                    phone_number=phone_number,
                    address=address,
                    type="driver",
                    status=status,
                    company_format=next_profile_format,
                    created_by=request.user,
                    updated_by=request.user
                )

                print("Profile created successfully for otherdrive.")
            
            return JsonResponse({'status': 'Success', 'message': 'Driver and Profile details added successfully'})
        
        except KeyError as e:
            return JsonResponse({'status': 'Error', 'message': f'Missing required parameter: {e}'}, status=400)
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'status': 'Error', 'message': str(e)}, status=400)



@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverListView(ListView):
    model = Driver
    template_name = "superadmin/view_driver.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverVerificationView(ListView):
    model = Driver
    template_name = "superadmin/view_driververification.html"    

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteDriverView(View):
    def get(self, request):
        driver_id = request.GET.get('driver_id', None)
        Driver.objects.get(driver_id=driver_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditDriverView(TemplateView):
    template_name = 'superadmin/edit_driver.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all active and verified vehicles
        all_vehicles = Vehicle.objects.filter(
            vehicle_status='active',
            verification_status='verified'
        )
        
        # Fetch all assigned vehicle IDs
        assigned_vehicle_ids = Driver.objects.values_list('vehicle_id', flat=True)
        
        # Filter out the assigned vehicles
        unassigned_vehicles = [vehicle for vehicle in all_vehicles if vehicle.vehicle_id not in assigned_vehicle_ids]
        
        # Add unassigned vehicles to the context
        context['vehiclelist'] = unassigned_vehicles
        
        try:
            context['driver_id'] = self.kwargs['id']
            driverlist = Driver.objects.filter(driver_id=context['driver_id'])
        except KeyError:
            driverlist = Driver.objects.none()
        
        # Add driver list to the context
        context['driverlist'] = list(driverlist)
        
        return context

from django.contrib.auth.models import User

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateDriverView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            # Fetch and validate inputs
            driver_id = request.POST.get('driver_id')
            vehicle_id = request.POST.get('vehicle', None)

            if not driver_id:
                return JsonResponse({'success': False, 'error': 'Missing driver_id'}, status=400)

            try:
                driver_id = int(driver_id)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid driver_id format'}, status=400)

            # Fetch the driver instance
            try:
                driver = Driver.objects.get(driver_id=driver_id)
            except Driver.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Driver not found'}, status=404)

            # Fetch the vehicle instance if vehicle_id is provided
            if vehicle_id:
                try:
                    vehicle_id = int(vehicle_id)
                    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
                    driver.vehicle = vehicle
                except (ValueError, Vehicle.DoesNotExist):
                    return JsonResponse({'success': False, 'error': 'Vehicle not found'}, status=404)

            # Update the related Profile first
            new_email = request.POST.get('email', driver.email)
            new_phone_number = request.POST.get('phone_number', driver.phone_number)
            new_address = request.POST.get('address', driver.address)
            new_status = request.POST.get('status', driver.status)         

            try:
                profile = Profile.objects.get(user__email=driver.email)
                profile.phone_number = new_phone_number
                profile.address = new_address
                profile.status = new_status
                profile.updated_by = request.user
                profile.save()
            except Profile.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Profile not found for the driver'}, status=404)

            # Update the related User model
            try:
                user = User.objects.get(email=driver.email)
                user.username = request.POST.get('name', driver.name)
                user.email = new_email  # Updating the email
                user.save()
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found for the driver'}, status=404)

            # Update the driver with new data, now including the email update
            driver.name = request.POST.get('name', driver.name)
            driver.phone_number = new_phone_number
            driver.email = new_email  # Set new email
            driver.address = new_address
            driver.status = new_status
            driver.company_format = request.POST.get('company_format', driver.company_format)
            driver.pfrom_date = request.POST.get('pfrom_date', driver.pfrom_date)
            driver.pto_date = request.POST.get('pto_date', driver.pto_date)
            driver.dfrom_date = request.POST.get('dfrom_date', driver.dfrom_date)
            driver.dto_date = request.POST.get('dto_date', driver.dto_date)

            if 'profile_image' in request.FILES:
                driver.profile_image = request.FILES['profile_image']
            if 'address_proof' in request.FILES:
                driver.address_proof = request.FILES['address_proof']
            if 'police_clearance' in request.FILES:
                driver.police_clearance = request.FILES['police_clearance']
            if 'driving_license' in request.FILES:
                driver.driving_license = request.FILES['driving_license']

            driver.updated_by = request.user
            driver.save() 
             # Handle vehicle and owner status updates
            if driver.vehicle:
                if driver.vehicle.drive_status == 'selfdrive':
                    driver.vehicle.vehicle_status = driver.status
                    driver.vehicle.save()

                    owner = driver.vehicle.owner
                    owner.status = driver.status
                    owner.save()
                elif driver.vehicle.drive_status == 'otherdrive':
                    if new_status == 'active' and driver.status == 'inactive':
                        driver.vehicle.vehicle_status = 'active'
                        driver.vehicle.save()
                    elif new_status == 'inactive' and driver.status == 'active':
                        driver.vehicle.vehicle_status = 'active'
                        driver.vehicle.save()

            DriverHistory.objects.create(
                driver_id=driver.driver_id,
                vehicle=driver.vehicle,
                name=driver.name,
                phone_number=driver.phone_number,
                email=driver.email,
                address=driver.address,
                status=driver.status,
                company_format=driver.company_format,
                pfrom_date=driver.pfrom_date,
                pto_date=driver.pto_date,
                dfrom_date=driver.dfrom_date,
                dto_date=driver.dto_date,
                profile_image=driver.profile_image.url if driver.profile_image else None,
                address_proof=driver.address_proof.url if driver.address_proof else None,
                police_clearance=driver.police_clearance.url if driver.police_clearance else None,
                driving_license=driver.driving_license.url if driver.driving_license else None,
                created_on=driver.created_on,
                updated_by=request.user.username,
                created_by=driver.created_by.username if driver.created_by else None
            )
            
            return JsonResponse({'success': True}, status=200)

        except ValueError as e:
            return JsonResponse({'success': False, 'error': f'Invalid input data: {e}'}, status=400)
        except Driver.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Driver not found'}, status=404)
        except Profile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)
        except Vehicle.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Vehicle not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'An unexpected error occurred: {e}'}, status=500)
            
class DriverHistoryView(TemplateView):
    template_name = 'superadmin/history_driver.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_id = self.kwargs['driver_id']
        driver = get_object_or_404(Driver, driver_id=driver_id)
        history = DriverHistory.objects.filter(driver_id=driver_id)
        context['driver'] = driver
        context['history'] = history
        return context

class ViewDriver(View):
    template_name = 'superadmin/detailview_driver.html'

    def get(self, request, driver_id):
        driverlist = get_object_or_404(Driver, pk=driver_id)
        return render(request, self.template_name, {'driverlist': driverlist}) 

def download_driver_documents(request, driver_id):
    # Fetch the vehicle object
    driver = Driver.objects.get(pk=driver_id)

    # List of all image fields in the Vehicle model
    image_fields = [
        driver.profile_image,
        driver.address_proof,
        driver.police_clearance,
        driver.driving_license,
    ]

    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={driver.company_format}_documents.zip'
    
    folder_name = driver.company_format  # Folder name inside the ZIP

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field:
                # Get the path of the image
                file_path = field.path
                # Get the file name
                file_name = os.path.basename(file_path)
                # Add the file to the ZIP under the specified folder
                zip_file.write(file_path, os.path.join(folder_name, file_name))
    
    return response

def verify_driver(request):
    driver_id = request.GET.get('driver_id')
    driver = Driver.objects.get(driver_id=driver_id)
    if driver.verification_status != 'verified':
        driver.verification_status = 'verified'
        driver.verified_on = timezone.now()
        driver.save()
        return JsonResponse({'verified': True})
    return JsonResponse({'verified': False})

@csrf_exempt
def toggle_driver_status(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        new_status = request.POST.get('new_status')
        block_reason = request.POST.get('block_reason', '')
        drive_status = request.POST.get('drive_status')
        owner_id = request.POST.get('owner_id')
        
        try:
            driver = Driver.objects.get(driver_id=driver_id)
            driver.status = new_status
            if new_status == 'inactive':
                driver.block_reason = block_reason
            
                if drive_status == 'selfdrive':
                    vehicle = driver.vehicle
                    vehicle.vehicle_status = new_status
                    vehicle.save()

                    owner = vehicle.owner
                    owner.status = new_status
                    owner.save()
                elif drive_status == 'otherdrive' and new_status == 'inactive':
                    # Separate the vehicle from the driver
                    driver.vehicle = None
                    driver.save()
            else:
                driver.block_reason = ''

            driver.save()
            DriverHistory.objects.create(
                driver_id=driver.driver_id,
                vehicle=driver.vehicle,
                name=driver.name,
                phone_number=driver.phone_number,
                email=driver.email,
                address=driver.address,
                status=driver.status,
                block_reason=driver.block_reason,
                company_format=driver.company_format,
                pfrom_date=driver.pfrom_date,
                pto_date=driver.pto_date,
                dfrom_date=driver.dfrom_date,
                dto_date=driver.dto_date,
                profile_image=driver.profile_image.url if driver.profile_image else None,
                address_proof=driver.address_proof.url if driver.address_proof else None,
                police_clearance=driver.police_clearance.url if driver.police_clearance else None,
                driving_license=driver.driving_license.url if driver.driving_license else None,
                created_on=driver.created_on,
                updated_by=request.user.username,
                created_by=driver.created_by.username if driver.created_by else None
            )

            return JsonResponse({'success': True}, status=200)
        except Driver.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Driver not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverReport(ListView):
    model = Driver
    template_name = "superadmin/driver_report.html"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all() 
        context['drivers'] = Driver.objects.all() 
        return context
    
# users###################################
@method_decorator(login_required(login_url='login'), name='dispatch')
class adduser(TemplateView):
    template_name = "superadmin/add_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_user = Profile.objects.all().order_by('-profile_id').first()
        if last_user:
            last_company_format = int(last_user.company_format.replace('USR', ''))
            next_company_format = f'USR{last_company_format + 1:02}'
        else:
            next_company_format = 'USR01'
        context['next_company_format'] = next_company_format
        return context

    def post(self, request):
        user_name = request.POST['user_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        user_type = request.POST['type']
        status = request.POST['status']
        company_format = request.POST.get('company_format', '')

        user = User.objects.create_user(username=user_name, email=email, password=password)
        profile = Profile.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            type=user_type,
            status=status,
            company_format=company_format,
            created_by=request.user,
        )

        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class UserList(ListView):
    model = Profile
    template_name = "superadmin/view_user.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteUser(View):
    def get(self, request):
        profile_id = request.GET.get('profile_id', None)
        if profile_id:
            try:
                profile = Profile.objects.get(profile_id=profile_id)
                user = profile.user
                profile.delete()  # Delete the profile
                user.delete()  # Delete the associated User
                data = {'deleted': True}
            except Profile.DoesNotExist:
                data = {'deleted': False, 'error': 'Profile does not exist'}
            except User.DoesNotExist:
                data = {'deleted': False, 'error': 'User does not exist'}
        else:
            data = {'deleted': False, 'error': 'Profile ID not provided'}
        
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditUser(TemplateView):
    template_name = 'superadmin/edit_user.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile_id'] = self.kwargs['id']
            userlist = Profile.objects.filter(profile_id=context['profile_id'])
        except:
            userlist = Profile.objects.filter(profile_id=context['profile_id'])
            
        context['userlist']= list(userlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUser(APIView):  
    def post(self, request):
        profile_id = request.POST.get('profile_id')
        profile = Profile.objects.get(profile_id=profile_id)
        
        # Update the profile with new data
        phone_number = request.POST.get('phone_number', profile.phone_number)
        address = request.POST.get('address', profile.address)
        email = request.POST.get('email', profile.user.email)
        password = request.POST.get('password')  # Retrieve the password from the form
        user_name = request.POST.get('user_name', profile.user.username)
        user_type = request.POST.get('type', profile.type)
        status = request.POST.get('status', profile.status)

        profile.phone_number = phone_number
        profile.address = address
        profile.type = user_type
        profile.status = status
        profile.updated_by = request.user

        # Update User fields
        profile.user.email = email
        profile.user.username = user_name
        if password:  # Only update the password if a new one was provided
            profile.user.set_password(password)
        profile.user.save()

        # Save updated profile
        profile.save()

        # Create a ProfileHistory entry after updating the profile
        ProfileHistory.objects.create(
            profile_id=profile_id,
            user=profile.user,
            phone_number=profile.phone_number,
            address=profile.address,
            type=profile.type,
            status=profile.status,
            company_format=profile.company_format,
            created_on=profile.created_on,
            updated_by=request.user.username,
            created_by=profile.created_by.username if profile.created_by else None
        )

        return JsonResponse({'success': True}, status=200)

    
class ProfileHistoryView(TemplateView):
    template_name = 'superadmin/history_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs['profile_id']
        profile = get_object_or_404(Profile, profile_id=profile_id)
        history = ProfileHistory.objects.filter(profile_id=profile_id)
        context['profile'] = profile
        context['history'] = history
        return context

# @login_required(login_url='login')
def check_phno(request):
    phone_number = request.GET.get('phone_number', None)
    ph = Profile.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)

# @login_required(login_url='login')
def check_useremail(request):
    email = request.GET.get('email', None)
    em = User.objects.filter(email=email)
    data = {
        'exists': em.count() > 0
    }
    return JsonResponse(data)        


# customer###################################

def check_phonenumber(request):
    phone_number = request.GET.get('phone_number', None)
    ph = Customer.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        new_status = request.POST.get('new_status')
        block_reason = request.POST.get('block_reason', '')

        try:
            customer = Customer.objects.get(pk=customer_id)
            customer.status = new_status
            if new_status == 'inactive':
                customer.block_reason = block_reason
            else:
                customer.block_reason = ''  # Clear block reason if reactivating
            customer.save()

            # Optionally, create a CustomerHistory entry here as well
            CustomerHistory.objects.create(
                customer_id=customer.customer_id,
                company_format=customer.company_format,
                customer_name=customer.customer_name,
                phone_number=customer.phone_number,
                address=customer.address,
                email=customer.email,
                status=customer.status,
                block_reason=customer.block_reason,
                created_on=customer.created_on,
                updated_on=customer.updated_on,
                created_by=customer.created_by.username if customer.created_by else None,
                updated_by=request.user.username
            )

            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class addcustomer(TemplateView):
    template_name = "superadmin/add_customer.html"

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
        password = request.POST['password']
        address = request.POST['address']
        status = request.POST['status']
        company_format = request.POST.get('company_format', '')

        cust = Customer(
            customer_name=customer_name,
            phone_number=phone_number,
            password=password,
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
    template_name = "superadmin/view_customer.html"
    def get_queryset(self):
        # First query: Get customers with ride count
        customers = Customer.objects.annotate(
            ride_count=Count('ridedetails')
        )

        # Second query: Calculate total fare for completed bookings
        completed_rides_totals = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('customer').annotate(
            total_fare=Sum('total_fare')
        ).values('customer', 'total_fare')

        # Convert to a dictionary for fast lookup
        fare_dict = {item['customer']: item['total_fare'] for item in completed_rides_totals}

        # Annotate customers with the total fare of completed bookings
        for customer in customers:
            customer.total_fare = fare_dict.get(customer.pk, 0.0)

        return customers

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteCustomer(View):
    def get(self, request):
        customer_id = request.GET.get('customer_id', None)
        Customer.objects.get(customer_id=customer_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditCustomer(TemplateView):
    template_name = 'superadmin/edit_customer.html'
    
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
        customer = Customer.objects.get(customer_id=customer_id)

        # Update the customer with new data
        customer.company_format = request.POST['company_format']
        customer.customer_name = request.POST['customer_name']
        customer.phone_number = request.POST['phone_number']
        customer.address = request.POST['address']
        customer.email = request.POST['email']
        customer.password = request.POST['password']
        customer.status = request.POST['status']
        customer.updated_by = request.user
        customer.save()

        # Create another CustomerHistory entry after updating the customer
        CustomerHistory.objects.create(
            customer_id=customer.customer_id,
            company_format=customer.company_format,
            customer_name=customer.customer_name,
            phone_number=customer.phone_number,
            address=customer.address,
            email=customer.email,
            password=customer.password,
            status=customer.status,
            created_on=customer.created_on,
            updated_on=customer.updated_on,
            created_by=customer.created_by.username if customer.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class CustomerHistoryView(TemplateView):
    template_name = 'superadmin/history_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(Customer, customer_id=customer_id)
        history = CustomerHistory.objects.filter(customer_id=customer_id).order_by('updated_on')
        context['customer'] = customer
        context['history'] = history
        return context

class ViewCustomer(View):
    template_name = 'superadmin/detailview_customer.html'

    def get(self, request, customer_id):
        customerlist = get_object_or_404(Customer, pk=customer_id)
        return render(request, self.template_name, {'customerlist': customerlist}) 

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
        # Add other statuses as needed

        context = {
            'customer': customer,
            'current_bookings': current_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'advanced_bookings': advanced_bookings,
            'assigned_bookings': assigned_bookings,
            'ongoing_booking': ongoing_booking,
            # Include other categories in the context
        }
        return render(request, 'superadmin/customer_bookings.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerProfileList(ListView):
    model = Customer
    template_name = "superadmin/cust_profile_list.html" 

    def get_queryset(self):
        # First query: Get customers with ride count
        customers = Customer.objects.annotate(
            ride_count=Count('ridedetails')
        )

        # Second query: Calculate total fare for completed bookings
        completed_rides_totals = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('customer').annotate(
            total_fare=Sum('total_fare')
        ).values('customer', 'total_fare')

        # Convert to a dictionary for fast lookup
        fare_dict = {item['customer']: item['total_fare'] for item in completed_rides_totals}

        # Annotate customers with the total fare of completed bookings
        for customer in customers:
            customer.total_fare = fare_dict.get(customer.pk, 0.0)

        return customers
    
# owner ###########################################################################################
@login_required(login_url='login')
def check_ownerphonenumber(request):
    phone_number = request.GET.get('phone_number', None)
    ph = VehicleOwner.objects.filter(phone_number=phone_number)
    data = {
        'exists': ph.count() > 0
    }
    return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddOwnerView(TemplateView):
    template_name = "superadmin/add_vehicleowner.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_owner = VehicleOwner.objects.all().order_by('-owner_id').first()
        if last_owner:
            last_company_format = int(last_owner.company_format.replace('VO', ''))
            next_company_format = f'VO{last_company_format + 1:02}'
        else:
            next_company_format = 'VO01'
        context['next_company_format'] = next_company_format
        return context

    def post(self, request):
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        address = request.POST['address']
        status = request.POST['status']
        company_format = request.POST.get('company_format', '')
        image = request.FILES['image']
        address_proof = request.FILES['address_proof']
        identity = request.FILES['identity']
        holdername = request.POST['holdername']
        ac_number = request.POST['ac_number']
        bankname = request.POST['bankname']
        ifsc_code = request.POST['ifsc_code']

        vo = VehicleOwner(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address,
            status=status,
            company_format=company_format,
            image=image,
            address_proof=address_proof,
            identity=identity,
            holdername=holdername,
            ac_number=ac_number,
            bankname=bankname,
            ifsc_code=ifsc_code,
            created_by=request.user,
            updated_by=request.user
        )
        vo.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerListView(ListView):
    model = VehicleOwner
    template_name = "superadmin/view_vehicleowner.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteOwnerView(View):
    def get(self, request):
        owner_id = request.GET.get('owner_id', None)
        VehicleOwner.objects.get(owner_id=owner_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditOwnerView(TemplateView):
    template_name = 'superadmin/edit_vehicleowner.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['owner_id'] = self.kwargs['id']
            ownerlist = VehicleOwner.objects.filter(owner_id=context['owner_id'])
        except:
            ownerlist = VehicleOwner.objects.filter(owner_id=context['owner_id'])
            
        context['ownerlist'] = list(ownerlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateOwnerView(APIView):  
    def post(self, request):
        owner_id = request.POST['owner_id']
        owner = get_object_or_404(VehicleOwner, owner_id=owner_id)
        original_owner_status = owner.status

        # Update the owner with new data
        owner.company_format = request.POST['company_format']
        owner.name = request.POST['name']
        owner.phone_number = request.POST['phone_number']
        owner.address = request.POST['address']
        owner.email = request.POST['email']
        if 'image' in request.FILES:
            owner.image = request.FILES['image']
        if 'address_proof' in request.FILES:
            owner.address_proof = request.FILES['address_proof']
        if 'identity' in request.FILES:
            owner.identity = request.FILES['identity']
        owner.status = request.POST['status']
        owner.holdername = request.POST['holdername']
        owner.ac_number = request.POST['ac_number']
        owner.bankname = request.POST['bankname']
        owner.ifsc_code = request.POST['ifsc_code']
        owner.updated_by = request.user
        owner.save()

        # Create a VehicleOwnerHistory entry after updating the owner
        VehicleOwnerHistory.objects.create(
            owner_id=owner.owner_id,
            company_format=owner.company_format,
            name=owner.name,
            phone_number=owner.phone_number,
            address=owner.address,
            email=owner.email,
            image=owner.image.url if owner.image else None,
            address_proof=owner.address_proof.url if owner.address_proof else None,
            identity=owner.identity.url if owner.identity else None,
            status=owner.status,
            holdername=owner.holdername,
            ac_number=owner.ac_number,
            bankname=owner.bankname,
            ifsc_code=owner.ifsc_code,
            created_on=owner.created_on,
            updated_on=owner.updated_on,
            created_by=owner.created_by.username if owner.created_by else None,
            updated_by=request.user.username
        )

        # Update corresponding vehicles if the status has changed
        if original_owner_status != owner.status:
            vehicles = owner.vehicle_set.all()  # Access related vehicles through reverse relationship
            for vehicle in vehicles:
                if vehicle.vehicle_status != owner.status:
                    vehicle.vehicle_status = owner.status
                    vehicle.save()

        return JsonResponse({'success': True}, status=200)

class VehicleOwnerHistoryView(TemplateView):
    template_name = 'superadmin/history_vehicleowner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_id = self.kwargs['owner_id']
        owner = get_object_or_404(VehicleOwner, owner_id=owner_id)
        history = VehicleOwnerHistory.objects.filter(owner_id=owner_id).order_by('updated_on')
        context['owner'] = owner
        context['history'] = history
        return context

class ViewOwner(View):
    template_name = 'superadmin/detailview_owner.html'

    def get(self, request, owner_id):
        ownerlist = get_object_or_404(VehicleOwner, pk=owner_id)
        return render(request, self.template_name, {'ownerlist': ownerlist}) 
    

def download_owner_documents(request, owner_id):
    # Fetch the vehicle object
    owner = VehicleOwner.objects.get(pk=owner_id)

    # List of all image fields in the Vehicle model
    image_fields = [
        owner.identity,
        owner.address_proof,
        owner.image,
    ]

    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={owner.company_format}_documents.zip'
    
    folder_name = owner.company_format  # Folder name inside the ZIP

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field:
                # Get the path of the image
                file_path = field.path
                # Get the file name
                file_name = os.path.basename(file_path)
                # Add the file to the ZIP under the specified folder
                zip_file.write(file_path, os.path.join(folder_name, file_name))
    
    return response

@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerVerification(ListView):
    model = VehicleOwner
    template_name = "superadmin/viewownerverification.html"   

def verify_owner(request):
    owner_id = request.GET.get('owner_id')
    owner = VehicleOwner.objects.get(owner_id=owner_id)
    if owner.verification_status != 'verified':
        owner.verification_status = 'verified'
        owner.verified_on = timezone.now()
        owner.save()
        return JsonResponse({'verified': True})
    return JsonResponse({'verified': False})   

@require_POST
def toggle_owner_status(request):
    owner_id = request.POST.get('owner_id')
    new_status = request.POST.get('new_status')
    block_reason = request.POST.get('block_reason', '')
  
    try:
        owner = VehicleOwner.objects.get(pk=owner_id)
        owner.status = new_status
        if new_status == 'inactive':
                owner.block_reason = block_reason
        else:
            owner.block_reason = ''
        owner.save()
        VehicleOwnerHistory.objects.create(
            owner_id=owner.owner_id,
            company_format=owner.company_format,
            name=owner.name,
            phone_number=owner.phone_number,
            address=owner.address,
            email=owner.email,
            image=owner.image.url if owner.image else None,
            address_proof=owner.address_proof.url if owner.address_proof else None,
            identity=owner.identity.url if owner.identity else None,
            status=owner.status,
            block_reason=block_reason,
            holdername=owner.holdername,
            ac_number=owner.ac_number,
            bankname=owner.bankname,
            ifsc_code=owner.ifsc_code,
            created_on=owner.created_on,
            updated_on=owner.updated_on,
            created_by=owner.created_by.username if owner.created_by else None,
            updated_by=request.user.username
        )
        return JsonResponse({'success': True})
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Owner not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})  

# vehicle ######################
@login_required(login_url='login')
def check_vehicleno(request):
    Vehicle_Number = request.GET.get('Vehicle_Number', None)
    vehicleno = Vehicle.objects.filter(Vehicle_Number=Vehicle_Number)
    data = {
        'exists': vehicleno.count() > 0
    }
    return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class AddVehicle(TemplateView):
    template_name = "superadmin/add_vehicle.html"
    
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
        
        # Setting next company format
        last_vehicle = Vehicle.objects.all().order_by('-vehicle_id').first()
        if last_vehicle:
            last_company_format = int(last_vehicle.company_format.replace('VEH', ''))
            next_company_format = f'VEH{last_company_format + 1:02}'
        else:
            next_company_format = 'VEH01'
        context['next_company_format'] = next_company_format
        
        return context
    
    def post(self, request):
        vehicle_number = request.POST['Vehicle_Number']
        model_id = request.POST['model']
        year = request.POST['year']
        insurance_expiry = request.POST['insurance_expiry']
        car_type = request.POST['car_type']
        color_id = request.POST['color']
        transmission_id = request.POST['transmission']
        owner_id = request.POST['owner']
        vehicle_type_id = request.POST['vehicle_type']
        commission_id = request.POST['commission_type']
        registration_certificate = request.FILES.get('registration_certificate')
        fc_certificate = request.FILES.get('fc_certificate')
        insurance_policy = request.FILES.get('insurance_policy')
        permit_details = request.FILES.get('permit_details')
        tax_details = request.FILES.get('tax_details')
        emission_test = request.FILES.get('emission_test')
        vehicle_status = request.POST['vehicle_status']
        drive_status = request.POST['drive_status']
        company_format = request.POST.get('company_format', '')

        vehicle = Vehicle(
            Vehicle_Number=vehicle_number,
            model=Model.objects.get(model_id=model_id),
            year=year,
            insurance_expiry=insurance_expiry,
            car_type=car_type,
            color=Color.objects.get(color_id=color_id),
            transmission=Transmission.objects.get(transmission_id=transmission_id),
            owner=VehicleOwner.objects.get(owner_id=owner_id),
            vehicle_type=VehicleType.objects.get(vehicle_type_id=vehicle_type_id),
            commission_type=CommissionType.objects.get(commission_id=commission_id),
            vehicle_status=vehicle_status,
            drive_status=drive_status,
            company_format=company_format,
            created_by=request.user,
            updated_by=request.user
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

@method_decorator(login_required(login_url='login'), name='dispatch')
class VehicleList(ListView):
    model = Vehicle
    template_name = "superadmin/view_vehicle.html"

    def get_queryset(self):
        return Vehicle.objects.filter(Q(vehicle_status='active'))

@method_decorator(login_required(login_url='login'), name='dispatch')
class VehicleBlockList(ListView):
    model = Vehicle
    template_name = "superadmin/view_vehicleblock.html"

    def get_queryset(self):
        return Vehicle.objects.filter(Q(vehicle_status='inactive'))

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteVehicle(View):
    def get(self, request):
        vehicle_id = request.GET.get('vehicle_id', None)
        Vehicle.objects.get(vehicle_id=vehicle_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditVehicle(TemplateView):
    template_name = 'superadmin/edit_vehicle.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')
        blist = Brand.objects.filter(status='active')
        modellist = Model.objects.filter(status='active')
        ownerlist = VehicleOwner.objects.filter(status='active',verification_status='verified')
        vtypelist = VehicleType.objects.all()
        ctypelist = CommissionType.objects.all()
        colorlist = Color.objects.all()
        tlist = Transmission.objects.all()
        try:
            context['vehicle_id'] = self.kwargs['id']
            vehiclelist = Vehicle.objects.filter(vehicle_id=context['vehicle_id'])
        except:
            vehiclelist = Vehicle.objects.filter(vehicle_id=context['vehicle_id'])
            
        context = {'blist':list(blist),'catlist':list(catlist),'modellist':list(modellist),'ownerlist':list(ownerlist),'vtypelist':list(vtypelist),'ctypelist':list(ctypelist),'vehiclelist':list(vehiclelist),'colorlist':list(colorlist),'tlist':list(tlist)}
        return context

@method_decorator(csrf_exempt, name='dispatch')
class UpdateVehicle(View):
    def post(self, request):
        vehicle_id = request.POST.get('vehicle_id')
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        vehicle.company_format = request.POST.get('company_format')
        vehicle.Vehicle_Number = request.POST.get('Vehicle_Number')
        vehicle.model = Model.objects.get(model_id=request.POST.get('model'))
        vehicle.year = request.POST.get('year')
        vehicle.insurance_expiry = request.POST.get('insurance_expiry')
        vehicle.car_type = request.POST.get('car_type')

        if 'registration_certificate' in request.FILES:
            vehicle.registration_certificate = request.FILES['registration_certificate']

        if 'fc_certificate' in request.FILES:
            vehicle.fc_certificate = request.FILES['fc_certificate']

        if 'insurance_policy' in request.FILES:
            vehicle.insurance_policy = request.FILES['insurance_policy']    

        if 'tax_details' in request.FILES:
            vehicle.tax_details = request.FILES['tax_details']  

        if 'permit_details' in request.FILES:
            vehicle.permit_details = request.FILES['permit_details']

        if 'emission_test' in request.FILES:
            vehicle.emission_test = request.FILES['emission_test']         
    

        vehicle.owner = VehicleOwner.objects.get(owner_id=request.POST.get('owner'))
        vehicle.vehicle_type = VehicleType.objects.get(vehicle_type_id=request.POST.get('vehicle_type'))
        vehicle.commission_type = CommissionType.objects.get(commission_id=request.POST.get('commission_type'))
        vehicle.color = Color.objects.get(color_id=request.POST.get('color'))
        vehicle.transmission = Transmission.objects.get(transmission_id=request.POST.get('transmission'))
        vehicle.vehicle_status = request.POST.get('vehicle_status')
        vehicle.drive_status = request.POST.get('drive_status')
        vehicle.updated_by = request.user
        vehicle.save()

        VehicleHistory.objects.create(
            vehicle_id=vehicle.vehicle_id,
            company_format=vehicle.company_format,
            Vehicle_Number=vehicle.Vehicle_Number,
            model=vehicle.model,
            year=vehicle.year,
            insurance_expiry=vehicle.insurance_expiry,
            car_type=vehicle.car_type,
            registration_certificate=vehicle.registration_certificate,
            fc_certificate=vehicle.fc_certificate,
            insurance_policy=vehicle.insurance_policy,
            tax_details=vehicle.tax_details,
            permit_details=vehicle.permit_details,
            emission_test=vehicle.emission_test,
            color=vehicle.color,
            transmission=vehicle.transmission,
            owner=vehicle.owner,
            vehicle_type=vehicle.vehicle_type,
            commission_type=vehicle.commission_type,
            vehicle_status=vehicle.vehicle_status,
            drive_status=vehicle.drive_status,
            created_on=vehicle.created_on,
            updated_on=vehicle.updated_on,
            created_by=vehicle.created_by.username if vehicle.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True, 'message': 'Vehicle updated successfully'}, status=200)
    
class VehicleHistoryView(TemplateView):
    template_name = 'superadmin/history_vehicle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)
        history = VehicleHistory.objects.filter(vehicle_id=vehicle_id).order_by('updated_on')
        context['vehicle'] = vehicle
        context['history'] = history
        return context

@csrf_exempt
def vehicleupdate_status(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        new_status = request.POST.get('new_status')
        block_reason = request.POST.get('block_reason', '')

        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            vehicle.vehicle_status = new_status
            if new_status == 'inactive':
                vehicle.block_reason = block_reason
            else:
                vehicle.block_reason = ''  # Clear block reason if reactivating
            vehicle.save()

            # Optionally, create a CustomerHistory entry here as well
            VehicleHistory.objects.create(
            vehicle_id=vehicle.vehicle_id,
            company_format=vehicle.company_format,
            Vehicle_Number=vehicle.Vehicle_Number,
            model=vehicle.model,
            year=vehicle.year,
            insurance_expiry=vehicle.insurance_expiry,
            car_type=vehicle.car_type,
            registration_certificate=vehicle.registration_certificate,
            fc_certificate=vehicle.fc_certificate,
            insurance_policy=vehicle.insurance_policy,
            tax_details=vehicle.tax_details,
            permit_details=vehicle.permit_details,
            emission_test=vehicle.emission_test,
            color=vehicle.color,
            transmission=vehicle.transmission,
            owner=vehicle.owner,
            vehicle_type=vehicle.vehicle_type,
            commission_type=vehicle.commission_type,
            vehicle_status=vehicle.vehicle_status,
            block_reason=vehicle.block_reason,
            created_on=vehicle.created_on,
            updated_on=vehicle.updated_on,
            created_by=vehicle.created_by.username if vehicle.created_by else None,
            updated_by=request.user.username
        )

            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Vehicle not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def download_vehicle_documents(request, vehicle_id):
    # Fetch the vehicle object
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    # List of all image fields in the Vehicle model
    image_fields = [
        vehicle.registration_certificate,
        vehicle.fc_certificate,
        vehicle.insurance_policy,
        vehicle.tax_details,
        vehicle.permit_details,
        vehicle.emission_test,
    ]

    # Create a ZIP file in memory
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={vehicle.company_format}_documents.zip'
    
    folder_name = vehicle.company_format  # Folder name inside the ZIP

    with zipfile.ZipFile(response, 'w') as zip_file:
        for field in image_fields:
            if field:
                # Get the path of the image
                file_path = field.path
                # Get the file name
                file_name = os.path.basename(file_path)
                # Add the file to the ZIP under the specified folder
                zip_file.write(file_path, os.path.join(folder_name, file_name))
    
    return response

class ViewVehicle(View):
    template_name = 'superadmin/detailview_vehicle.html'

    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        driver = Driver.objects.filter(vehicle=vehicle).first()  # Get the associated driver, if any
        return render(request, self.template_name, {'vehicle': vehicle, 'driver': driver})
    
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
        return JsonResponse({'verified': True})
    return JsonResponse({'verified': False})    
    
# ride details ##########################################

@csrf_exempt
def fetch_customer_details(request):
    phone_number = request.GET.get('phone_number', None)
    if phone_number:
        try:
            customer = Customer.objects.get(phone_number=phone_number)
            customer_details = {
                'id': customer.customer_id,  # Ensure the customer ID is included
                'name': customer.customer_name,
                'email': customer.email,
                'address': customer.address
            }
            return JsonResponse({'success': True, 'customer': customer_details})
        except Customer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


class AddRidee(TemplateView):
    template_name = "add_ride.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['customerlist'] = Customer.objects.all()
        context['ridetypelist'] = Ridetype.objects.all()
        context['catlist'] = Category.objects.all()
        context['blist'] = Brand.objects.all()
        context['modellist'] = Model.objects.all()
        
        last_ride = RideDetails.objects.all().order_by('-ride_id').first()
        if last_ride:
            last_company_format = int(last_ride.company_format.replace('RID', ''))
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
            
            print(f"Received Data: {company_format}, {ride_type_id}, {source}, {destination}, {pickup_date}, {pickup_time}, {model_id}, {total_fare}, {customer_id}, {customer_notes}, {ride_status}")

            # Ensure objects exist in database before saving
            customer = Customer.objects.get(customer_id=customer_id)
            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            model = Model.objects.get(model_id=model_id)

            # Determine ride status based on pickup date
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'
            
            ride_details = RideDetails(
                company_format=company_format,
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
            print(f"Customer with ID {customer_id} does not exist.")
            return JsonResponse({'status': 'Error', 'message': f'Customer with ID {customer_id} does not exist.'})
        except Exception as e:
            print(f"Error saving ride details: {e}")
            return JsonResponse({'status': 'Error', 'message': str(e)})
        
# add bookings inside superadmin##########################################

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

class AddRide(TemplateView):
    template_name = "superadmin/add_ride.html"
    
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
            # car_type = request.POST.get('car_type', '').strip()  # Fetch car_type (AC or Non-AC)
            slots = determine_time_slot(pickup_time)
            ride_status = request.POST['ride_status']
            phone_number = request.POST['phone_number']
            customer_name = request.POST['customer_name']
            email = request.POST['email']
            address = request.POST['address']

            print(f"Parsed data: {company_format}, {ride_type_id}, {source}, {destination}, {pickup_date}, {pickup_time}")

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
            print(f"Created new customer: {customer}")

            # Ensure objects exist in database before saving
            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            category_name = category.split('|')[0]
            car_type_name = category.split('|')[1]
            category_instance = Category.objects.get(category_name=category_name)

            # Retrieve pricing instance
            pricing_instance = Pricing.objects.get(
                category=category_instance,
                car_type=car_type_name,
                ridetype=ridetype,
                slots=slots,
            )
            print(f"Saving ride with details: {company_format}, {ridetype}, {category_instance}")

            # Determine ride status based on pickup date
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            # Use the next company format for the ride
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
                pricing = pricing_instance,  # Set the Pricing instance

            )
            ride_details.save()
            print("Ride details saved successfully.")
            
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
                
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class RideList(ListView):
    model = RideDetails
    template_name = "superadmin/view_ride.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.filter(verification_status='verified')
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='currentbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        
        return context

    def get_queryset(self):
        today = date.today()
        # Update ride status for rides with a past pickup date
        past_rides = RideDetails.objects.filter(pickup_date__lt=today, ride_status='currentbookings')
        past_rides.update(ride_status='pendingbookings')
        
        # Fetch rides with a pickup date of today and status as current bookings
        current_rides = RideDetails.objects.filter(ride_status='currentbookings', pickup_date=today)
        
        service_type = self.request.GET.get('service_type_id')
        if service_type:
            current_rides = current_rides.filter(ridetype_id=service_type)
        return current_rides
    
#################################### advance bookings ###########################################

@method_decorator(login_required(login_url='login'), name='dispatch')
class AdvanceBookingsList(ListView):
    model = RideDetails
    template_name = "superadmin/advance_bookings.html"  # Ensure you create this template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.filter(verification_status='verified')
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='advancebookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all() 
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
    template_name = "superadmin/pending_bookings.html"  # Ensure you create this template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='pendingbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        today = date.today()
        return RideDetails.objects.filter(ride_status='pendingbookings', pickup_date__lt=today)
    
# assigned ride list##################################################################################################
@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "superadmin/assigned_rides.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='assignbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        # Get only rides that are assigned
        return RideDetails.objects.filter(Q(ride_status='assignbookings')).select_related('driver')

# assign later list##################################################################################################
@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignLaterList(ListView):
    model = RideDetails
    template_name = "superadmin/assign_later.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='assignlaterbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        # Get only rides that are assigned
        return RideDetails.objects.filter(Q(ride_status='assignlaterbookings')).select_related('driver')
        
# ongoing rides########################################################################################################
class OngoingRideList(ListView):
    model = RideDetails
    template_name = "superadmin/ongoing_rides.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drivers'] = Driver.objects.all()
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='ongoingbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all()  
        context['ride_id'] = self.kwargs.get('ride_id', 1)  # Adjust this based on your URL setup
        return context

    def get_queryset(self):
        return RideDetails.objects.filter(ride_status='ongoingbookings') 
    
# completed rides########################################################################################################
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "superadmin/completed_rides.html"

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

# def completed_bookings_filter(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     if start_date and end_date:
#         bookings = RideDetails.objects.filter(booking_datetime__range=[start_date, end_date])
#         data = serialize('json', bookings, use_natural_primary_keys=True, use_natural_foreign_keys=True)
#         return JsonResponse(data, safe=False)
#     else:
#         return JsonResponse({'error': 'Invalid date range'}, status=400)
    
# invoice rides########################################################################################################

class InvoiceView(DetailView):
    model = RideDetails
    template_name = 'superadmin/invoice.html'
    context_object_name = 'ride'
    
    def get_object(self):
        ride_id = self.kwargs.get("ride_id")
        return get_object_or_404(RideDetails, ride_id=ride_id)


# assign driver###########################################################################################################
def assign_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver_id = data.get('driver_id')  # This will be company_format
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)  # Use ride_id instead of id
            driver = Driver.objects.get(company_format=driver_id)  # Lookup driver using company_format
            ride.driver = driver  # Assign the driver object
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

    return JsonResponse({'status': 'failed'}, status=400)

# advanceassign driver###########################################################################################################
def advanceassign_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver_id = data.get('driver_id')  # This will be company_format
        ride_id = data.get('ride_id')

        try:
            ride = RideDetails.objects.get(ride_id=ride_id)  # Use ride_id instead of id
            driver = Driver.objects.get(company_format=driver_id)  # Lookup driver using company_format
            ride.driver = driver  # Assign the driver object
            ride.ride_status = 'assignlaterbookings'
            ride.assigned_by=request.user
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
    template_name = 'superadmin/view_ride.html'
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
    template_name = 'superadmin/edit_ride.html'
  
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

# @method_decorator(login_required(login_url='login'), name='dispatch')
# class UpdateRide(APIView):
#     @csrf_exempt
#     def post(self, request):
#         # Retrieve and validate ride_id from request
#         ride_id = request.POST.get('ride_id')
#         if not ride_id:
#             return JsonResponse({'success': False, 'error': 'Missing ride_id'}, status=400)

#         try:
#             ride_id = int(ride_id)
#         except ValueError:
#             return JsonResponse({'success': False, 'error': 'Invalid ride_id'}, status=400)

#         # Retrieve the ride object
#         try:
#             ride = RideDetails.objects.get(ride_id=ride_id)
#         except RideDetails.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Ride not found'}, status=404)

#         # Update customer if provided
#         customer_id = request.POST.get('customer')
#         if customer_id:
#             try:
#                 # Customer handling
#                 phone_number = request.POST.get('phone_number')
#                 customer_name = request.POST.get('customer_name')
#                 email = request.POST.get('email')
#                 address = request.POST.get('address')

#                 if phone_number:
#                     customer, created = Customer.objects.get_or_create(
#                         phone_number=phone_number,
#                         defaults={
#                             'customer_name': customer_name,
#                             'email': email,
#                             'address': address,
#                             'created_by': request.user,
#                             'updated_by': request.user,
#                         }
#                     )
#                     if not created:
#                         customer.customer_name = customer_name
#                         customer.email = email
#                         customer.address = address
#                         customer.updated_by = request.user
#                         customer.save()
#                     ride.customer = customer
#             except (ValueError, Customer.DoesNotExist):
#                 return JsonResponse({'success': False, 'error': 'Invalid customer details'}, status=400)
                

#         # Update ridetype if provided
#         ridetype_id = request.POST.get('ridetype')
#         if ridetype_id:
#             try:
#                 ridetype_id = int(ridetype_id)
#                 ridetype = Ridetype.objects.get(ridetype_id=ridetype_id)
#                 ride.ridetype = ridetype
#             except (ValueError, Ridetype.DoesNotExist):
#                 return JsonResponse({'success': False, 'error': 'Invalid ridetype_id'}, status=400)

#         # Update model if provided
#         model_id = request.POST.get('model')
#         if model_id:
#             try:
#                 model_id = int(model_id)
#                 model = Model.objects.get(model_id=model_id)
#                 ride.model = model
#             except (ValueError, Model.DoesNotExist):
#                 return JsonResponse({'success': False, 'error': 'Invalid model_id'}, status=400)

#         # Update driver if provided
#         driver_id = request.POST.get('driver')
#         if driver_id:
#             try:
#                 driver_id = int(driver_id)
#                 driver = Driver.objects.get(driver_id=driver_id)
#                 ride.driver = driver
#             except (ValueError, Driver.DoesNotExist):
#                 return JsonResponse({'success': False, 'error': 'Invalid driver_id'}, status=400)
            
        

#         # Update other fields
#         ride.source = request.POST.get('source', ride.source)
#         ride.destination = request.POST.get('destination', ride.destination)
#         ride.pickup_date = request.POST.get('pickup_date', ride.pickup_date)
#         ride.pickup_time = request.POST.get('pickup_time', ride.pickup_time)
#         ride.total_fare = request.POST.get('total_fare', ride.total_fare)
#         ride.customer_notes = request.POST.get('customer_notes', ride.customer_notes)
#         ride.updated_by = request.user

#         try:
#             ride.save()
#         except IntegrityError as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
#         today = date.today().isoformat()
#         ride.ride_status = 'advancebookings' if ride.pickup_date > today else 'currentbookings'

#         # Create a RideDetailsHistory entry after updating the ride
#         try:
#             RideDetailsHistory.objects.create(
#                 ride_id=ride.ride_id,
#                 company_format=ride.company_format,
#                 ridetype=ride.ridetype,
#                 source=ride.source,
#                 destination=ride.destination,
#                 pickup_date=ride.pickup_date,
#                 pickup_time=ride.pickup_time,
#                 model=ride.model,
#                 driver=ride.driver,
#                 assigned_by=ride.assigned_by.username if ride.assigned_by else None,
#                 cancelled_by=ride.cancelled_by.username if ride.cancelled_by else None,
#                 total_fare=ride.total_fare,
#                 customer=ride.customer,
#                 customer_notes=ride.customer_notes,
#                 ride_status=ride.ride_status,
#                 booking_datetime=ride.booking_datetime,
#                 created_on=ride.created_on,
#                 updated_on=ride.updated_on,
#                 created_by=ride.created_by.username if ride.created_by else None,
#                 updated_by=request.user.username,
#                 comments=ride.comments
#             )
#         except (IntegrityError, DuplicateKeyError) as e:
#             return JsonResponse({'success': False, 'error': 'Duplicate key error: {}'.format(str(e))}, status=500)

#         return JsonResponse({'success': True}, status=200)
    
# class RideDetailsHistoryView(TemplateView):
#     template_name = 'superadmin/history_ride.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         ride_id = self.kwargs['ride_id']
#         ride = get_object_or_404(RideDetails, ride_id=ride_id)
#         history = RideDetailsHistory.objects.filter(ride_id=ride_id).order_by('updated_on')
#         context['ride'] = ride
#         context['history'] = history
#         return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateRide(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            # Retrieve POST data
            ride_id = request.POST['ride_id']
            company_format = request.POST['company_format']
            ride_type_id = request.POST['ridetype']
            source = request.POST.get('source',None)
            destination = request.POST.get('destination',None)
            pickup_date = request.POST['pickup_date']
            pickup_time = request.POST['pickup_time']
            category = request.POST['category']
            total_fare = request.POST['total_fare']
            customer_id = request.POST['customer']
            customer_notes = request.POST['customer_notes']
            # ride_status = request.POST['ride_status']
            phone_number = request.POST['phone_number']
            customer_name = request.POST['customer_name']
            email = request.POST['email']
            address = request.POST['address']
            slots = determine_time_slot(pickup_time)

            # Fetch the existing ride details
            ride_details = RideDetails.objects.get(ride_id=ride_id)

            # Handle customer: Get existing or create new one
            try:
                customer = Customer.objects.get(phone_number=phone_number)
                # Update customer information if necessary
                customer.customer_name = customer_name
                customer.email = email
                customer.address = address
                customer.updated_by = request.user
            except Customer.DoesNotExist:
                # Create new customer with a unique company_format
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

            # Ensure objects exist in database before saving
            ridetype = Ridetype.objects.get(ridetype_id=ride_type_id)
            category_name = category.split('|')[0]
            car_type_name = category.split('|')[1]
            category_instance = Category.objects.get(category_name=category_name)

            # Retrieve pricing instance
            pricing_instance = Pricing.objects.get(
                category=category_instance,
                car_type=car_type_name,
                ridetype=ridetype,
                slots=slots,
            )
            print(f"Saving ride with details: {company_format}, {ridetype}, {category_instance}")

            # Determine ride status based on pickup date
            today = date.today().isoformat()
            ride_status = 'advancebookings' if pickup_date > today else 'currentbookings'

            # Update ride details
            # ride_details.company_format = ride_details.company_format  # Retain existing company format
            ride_details.customer = customer
            ride_details.ridetype = ridetype
            ride_details.category = category
            ride_details.source = source
            ride_details.destination = destination
            ride_details.pickup_date = pickup_date
            ride_details.pickup_time = pickup_time
            ride_details.total_fare = total_fare
            ride_details.customer_notes = customer_notes
            ride_details.ride_status = ride_status
            ride_details.updated_by = request.user

            ride_details.save()

            return JsonResponse({'status': "Success", 'message': 'Ride details updated successfully'})
        except RideDetails.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': f'Ride with ID {ride_id} does not exist.'})
        except Exception as e:
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

@method_decorator(login_required(login_url='login'), name='dispatch')
class profile(TemplateView):
    template_name = 'superadmin/app-profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_id = self.request.session.get('user_id')
            userlist = User.objects.filter(id=user_id)
        except:
            userlist = User.objects.filter(id=user_id)
            
        context['userlist']= list(userlist)
        return context
    
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
    


##################    cancel booking    #################################################################### 
@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "superadmin/view_cancelbookings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Ridetype.objects.all()
        context['bookings'] = RideDetails.objects.filter(ride_status='completedbookings')
        context['categories'] = Category.objects.all() 
        context['vehicles'] = Vehicle.objects.all() 
        context['drivers'] = Driver.objects.all() 
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

####################################   pricing    ######################### ########################
@method_decorator(login_required(login_url='login'), name='dispatch')
class addprice(TemplateView):
    template_name = "superadmin/add_pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.all()
        rlist = Ridetype.objects.all()
        context = {'catlist': list(catlist),'rlist':list(rlist)}
        return context

    def post(self, request):
        category = request.POST['category']
        ridetype = request.POST['ridetype']
        slots = request.POST['slots']
        driver_beta = Decimal(request.POST.get('driver_beta', '0') or '0')
        toll_price = Decimal(request.POST.get('toll_price', '0') or '0')
        car_type = request.POST['car_type']
        trip_type = request.POST.get('trip_type')
        permit = Decimal(request.POST.get('permit', '0') or '0')
        price_per_km = Decimal(request.POST.get('price_per_km', '0') or '0')


        br = Pricing(
            category=Category.objects.get(category_id=category),
            ridetype=Ridetype.objects.get(ridetype_id=ridetype),
            slots=slots,
            driver_beta=driver_beta,
            toll_price=toll_price,
            car_type=car_type,
            trip_type=trip_type,
            permit=permit,
            price_per_km=price_per_km,
            created_by=request.user,
            updated_by=request.user
        )
        br.save()
        return JsonResponse({'status':"Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class PriceList(ListView):
    model = Pricing
    template_name = "superadmin/view_pricing.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletePrice(View):
    def get(self, request):
        pricing_id = request.GET.get('pricing_id', None)
        Pricing.objects.get(pricing_id=pricing_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPrice(TemplateView):
    template_name = 'superadmin/edit_pricing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.all()
        rlist = Ridetype.objects.all()
        try:
            context['pricing_id'] = self.kwargs['id']
            plist = Pricing.objects.filter(pricing_id=context['pricing_id'])
        except:
            plist = Pricing.objects.filter(pricing_id=context['pricing_id'])
            
        context = {'plist':list(plist),'catlist':list(catlist),'rlist':list(rlist)}
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdatePricing(APIView):
    def post(self, request):
        pricing_id = request.POST['pricing_id']
        pricing = Pricing.objects.get(pricing_id=pricing_id)

        # Update the pricing with new data
        pricing.ridetype_id = request.POST['ridetype']
        pricing.category_id = request.POST['category']
        pricing.slots = request.POST['slots']
        pricing.car_type = request.POST['car_type']
        pricing.driver_beta = Decimal(request.POST.get('driver_beta', '0') or '0')
        pricing.toll_price = Decimal(request.POST.get('toll_price', '0') or '0')
        pricing.trip_type = request.POST.get('trip_type')
        pricing.permit = Decimal(request.POST.get('permit', '0') or '0')
        pricing.price_per_km = Decimal(request.POST.get('price_per_km', '0') or '0')
        pricing.updated_by = request.user
        pricing.save()

        # Create another PricingHistory entry after updating the pricing
        PricingHistory.objects.create(
            pricing_id=pricing.pricing_id,
            ridetype=pricing.ridetype,
            category=pricing.category,
            slots=pricing.slots,
            driver_beta=pricing.driver_beta,
            toll_price=pricing.toll_price,
            car_type=pricing.car_type,
            trip_type=pricing.trip_type,
            permit=pricing.permit,
            price_per_km=pricing.price_per_km,  # Convert to string first
            created_on=pricing.created_on,
            updated_on=pricing.updated_on,
            created_by=pricing.created_by.username if pricing.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)
    
class PricingHistoryView(TemplateView):
    template_name = 'superadmin/history_pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pricing_id = self.kwargs['pricing_id']
        pricing = get_object_or_404(Pricing, pricing_id=pricing_id)
        history = PricingHistory.objects.filter(pricing_id=pricing_id).order_by('updated_on')
        context['pricing'] = pricing
        context['history'] = history
        return context

    
####################################   Commission    ######################### ########################
@method_decorator(login_required(login_url='login'), name='dispatch')
class addcommission(TemplateView):
    template_name = "superadmin/add_commissiontype.html"

    def post(self, request):
        commission_name = request.POST['commission_name']
        commission_percentage = request.POST['commission_percentage']

        br = CommissionType(
            commission_name=commission_name,
            commission_percentage=commission_percentage,
            created_by=request.user,
            updated_by=request.user
        )
        br.save()
        return JsonResponse({'status':"Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CommissionList(ListView):
    model = CommissionType
    template_name = "superadmin/view_commissiontype.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteCommission(View):
    def get(self, request):
        commission_id = request.GET.get('commission_id', None)
        CommissionType.objects.get(commission_id=commission_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class EditCommission(TemplateView):
    template_name = 'superadmin/edit_commissiontype.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clist = Category.objects.all()
        try:
            context['commission_id'] = self.kwargs['id']
            clist = CommissionType.objects.filter(commission_id=context['commission_id'])
        except:
            clist = CommissionType.objects.filter(commission_id=context['commission_id'])
            
        context = {'clist':list(clist)}
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateCommission(APIView):
    def post(self, request):
        commission_id = request.POST['commission_id']
        commission = CommissionType.objects.get(commission_id=commission_id)

        # Update the pricing with new data
        commission.commission_name = request.POST['commission_name']
        commission.commission_percentage = request.POST['commission_percentage']
        commission.updated_by = request.user
        commission.save()

        # Create another PricingHistory entry after updating the pricing
        CommissionHistory.objects.create(
            commission_id=commission.commission_id,
            commission_name=commission.commission_name,
            commission_percentage=commission.commission_percentage,
            created_on=commission.created_on,
            updated_on=commission.updated_on,
            created_by=commission.created_by.username if commission.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)
    
class CommissionHistoryView(TemplateView):
    template_name = 'superadmin/history_commission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission_id = self.kwargs['commission_id']
        commission = get_object_or_404(CommissionType, commission_id=commission_id)
        history = CommissionHistory.objects.filter(commission_id=commission_id).order_by('updated_on')
        context['commission'] = commission
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddAccountsView(TemplateView):
    template_name = "superadmin/add_accounts.html"

    def post(self, request):
        date = request.POST['date']
        day_name = request.POST['day_name']
        vehicle_atm = Decimal(request.POST.get('vehicle_atm', '0') or '0')
        tripsheet = Decimal(request.POST.get('tripsheet', '0') or '0')
        total_credit = Decimal(request.POST.get('total_credit', '0') or '0')
        cash_recieved = Decimal(request.POST.get('cash_recieved', '0') or '0')
        balance_bd = Decimal(request.POST.get('balance_bd', '0') or '0')
        total_balance = Decimal(request.POST.get('total_balance', '0') or '0')
        expense = Decimal(request.POST.get('expense', '0') or '0')
        cash_transfer = Decimal(request.POST.get('cash_transfer', '0') or '0')
        total_expense = Decimal(request.POST.get('total_expense', '0') or '0')
        balance = Decimal(request.POST.get('balance', '0') or '0')

        account = Accounts(
            date=date,
            day_name=day_name,
            vehicle_atm=vehicle_atm,
            tripsheet=tripsheet,
            total_credit=total_credit,
            cash_recieved=cash_recieved,
            balance_bd=balance_bd,
            total_balance=total_balance,
            expense=expense,
            cash_transfer=cash_transfer,
            total_expense=total_expense,
            balance=balance,
            created_by=request.user,
            updated_by=request.user
        )
        account.save()
        return JsonResponse({'status': "Success"})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountsListView(ListView):
    model = Accounts
    template_name = "superadmin/view_accounts.html"  

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAccounts(View):
    def get(self, request):
        account_id = request.GET.get('account_id', None)
        Accounts.objects.get(account_id=account_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)  

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditAccounts(TemplateView):
    template_name = 'superadmin/edit_accounts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['account_id'] = self.kwargs['id']
            alist = Accounts.objects.filter(account_id=context['account_id'])
        except:
            alist = Accounts.objects.filter(account_id=context['account_id'])
            
        context['alist']= list(alist)
        return context 

class UpdateAccounts(APIView):
    def post(self, request):
        date = request.POST['date']
        day_name = request.POST['day_name']
        vehicle_atm = request.POST['vehicle_atm']
        tripsheet = request.POST['tripsheet']
        total_credit = request.POST['total_credit']
        cash_recieved = request.POST['cash_recieved']
        balance_bd = request.POST['balance_bd']
        total_balance = request.POST['total_balance']
        expense = request.POST['expense']
        cash_transfer = request.POST['cash_transfer']
        total_expense = request.POST['total_expense']
        balance = request.POST['balance']
        account_id = request.POST['account_id']
    
        acc=Accounts.objects.get(account_id=account_id)
        acc.date=date
        acc.day_name=day_name
        acc.vehicle_atm=vehicle_atm
        acc.tripsheet=tripsheet
        acc.total_credit=total_credit
        acc.cash_recieved=cash_recieved
        acc.balance_bd=balance_bd
        acc.total_balance=total_balance
        acc.expense=expense
        acc.cash_transfer=cash_transfer
        acc.total_expense=total_expense
        acc.balance=balance
    
        acc.save()
        return JsonResponse({'success': True}, status=200)


# transmission #################################################
@login_required(login_url='login')
def check_transmission(request):
    transmission_name = request.GET.get('transmission_name', None)
    transmissions = Transmission.objects.filter(transmission_name=transmission_name)
    data = {
        'exists': transmissions.count() > 0
    }
    return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addtransmission(TemplateView):
    template_name = "superadmin/add_transmission.html"

    def post(self, request):
        transmission_name = request.POST['transmission_name']
        trans = Transmission(
            transmission_name=transmission_name,
            created_by=request.user,
            updated_by=request.user
        )
        trans.save()
        return JsonResponse({'status': "Success"})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class TransmissionListView(ListView):
    model = Transmission
    template_name = "superadmin/view_transmission.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteTransmission(View):
    def get(self, request):
        transmission_id = request.GET.get('transmission_id', None)
        Transmission.objects.get(transmission_id=transmission_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')   
class EditTransmission(TemplateView):
    template_name = 'superadmin/edit_transmission.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['transmission_id'] = self.kwargs['id']
            tlist = Transmission.objects.filter(transmission_id=context['transmission_id'])
        except:
            tlist = Transmission.objects.filter(transmission_id=context['transmission_id'])
            
        context['tlist']= list(tlist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateTransmission(APIView):
    def post(self, request):
        transmission_id = request.POST['transmission_id']
        transmission = get_object_or_404(Transmission, transmission_id=transmission_id)

        # Update the category with new data
        transmission.transmission_name = request.POST['transmission_name']
        transmission.updated_by = request.user
        transmission.save()

        # Create a CategoryHistory entry after updating the category
        TransmissionHistory.objects.create(
            transmission_id=transmission.transmission_id,
            transmission_name=transmission.transmission_name,
            created_on=transmission.created_on,
            updated_on=transmission.updated_on,
            created_by=transmission.created_by.username if transmission.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class TransmissionHistoryView(TemplateView):
    template_name = 'superadmin/history_transmission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transmission_id = self.kwargs['transmission_id']
        transmission = get_object_or_404(Transmission, transmission_id=transmission_id)
        history = TransmissionHistory.objects.filter(transmission_id=transmission_id).order_by('updated_on')
        context['transmission'] = transmission
        context['history'] = history
        return context 

class ViewTransmission(View):
    template_name = 'superadmin/detailview_transmission.html'

    def get(self, request, transmission_id):
        tlist = get_object_or_404(Transmission, pk=transmission_id)
        return render(request, self.template_name, {'tlist': tlist})          


# color #######################################################################

@login_required(login_url='login')   
def check_color(request):
    name = request.GET.get('name', None)
    colors = Color.objects.filter(name=name)
    data = {
        'exists': colors.count() > 0
    }
    return JsonResponse(data) 

@method_decorator(login_required(login_url='login'), name='dispatch')
class addcolor(TemplateView):
    template_name = "superadmin/add_color.html"

    def post(self, request):
        name = request.POST['name']

        cl = Color(
            name=name,
            created_by=request.user,
            updated_by=request.user
        )
        cl.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class colorList(ListView):
    model = Color
    template_name = "superadmin/view_color.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class Deletecolor(View):
    def get(self, request):
        color_id = request.GET.get('color_id', None)
        Color.objects.get(color_id=color_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class Editcolor(TemplateView):
    template_name = 'superadmin/edit_color.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['color_id'] = self.kwargs['id']
            clist = Color.objects.filter(color_id=context['color_id'])
        except:
            clist = Color.objects.filter(color_id=context['color_id'])
            
        context['clist']= list(clist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class Updatecolor(APIView):
    def post(self, request):
        color_id = request.POST['color_id']
        color = Color.objects.get(color_id=color_id)

        # Update the ride type with new data
        color.name = request.POST['name']
        color.updated_by = request.user
        color.save()

        # Create another RidetypeHistory entry after updating the ride type
        ColorHistory.objects.create(
            color_id=color.color_id,
            name=color.name,
            created_on=color.created_on,
            updated_on=color.updated_on,
            created_by=color.created_by.username if color.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class ColorHistoryView(TemplateView):
    template_name = 'superadmin/history_color.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color_id = self.kwargs['color_id']
        color = get_object_or_404(Color, color_id=color_id)
        history = ColorHistory.objects.filter(color_id=color_id).order_by('updated_on')
        context['color'] = color
        context['history'] = history
        return context


class ViewColor(View):
    template_name = 'superadmin/detailview_color.html'

    def get(self, request, color_id):
        clist = get_object_or_404(Color, pk=color_id)
        return render(request, self.template_name, {'clist': clist})  


    

# Commission details ##############################################

@method_decorator(login_required(login_url='login'), name='dispatch')
class CommVehicleListView(ListView):
    model = RideDetails
    template_name = "superadmin/comm_vehiclelist.html"
    
    def get_queryset(self):
        # Get the latest pickup_date for each driver where the ride status is 'completedbookings'
        latest_bookings = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('driver').annotate(
            latest_pickup_date=Max('pickup_date')
        )

        # Filter RideDetails to include only those with the latest pickup_date per driver
        queryset = RideDetails.objects.filter(
            driver__in=[booking['driver'] for booking in latest_bookings],
            pickup_date__in=[booking['latest_pickup_date'] for booking in latest_bookings],
            ride_status='completedbookings'
        ).select_related('driver', 'driver__vehicle', 'driver__vehicle__owner')

        # Add commission calculations to each RideDetails object in the queryset
        for ride in queryset:
            ride.driver_commission = self.calculate_driver_commission(ride)
            ride.company_commission = self.calculate_company_commission(ride)

        return queryset

    def calculate_driver_commission(self, ride):
        """
        Calculate the driver's commission based on the total fare and the vehicle's commission percentage.
        """
        if ride.driver and ride.driver.vehicle and ride.driver.vehicle.commission_type:
            vehicle_commission_percentage_str = str(ride.driver.vehicle.commission_type.commission_percentage)
            vehicle_commission_percentage = Decimal(vehicle_commission_percentage_str)

            vehicle_commission_amount = (ride.total_fare * vehicle_commission_percentage) / Decimal(100)

            driver_commission = ride.total_fare - vehicle_commission_amount
            return driver_commission
        return Decimal(0)

    def calculate_company_commission(self, ride):
        """
        Calculate the company's commission based on the total fare and the calculated driver commission.
        """
        driver_commission = self.calculate_driver_commission(ride)
        return ride.total_fare - driver_commission


class VehicleDetailView(ListView):
    model = RideDetails
    template_name = "superadmin/vehicle_commission_detail.html"
    
    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        queryset = RideDetails.objects.filter(
            driver__vehicle__vehicle_id=vehicle_id,
            ride_status='completedbookings'
        ).select_related('driver', 'driver__vehicle')

        # Add commission calculations to each RideDetails object in the queryset
        for ride in queryset:
            ride.driver_commission = self.calculate_driver_commission(ride)
            ride.company_commission = self.calculate_company_commission(ride)

        return queryset

    def calculate_driver_commission(self, ride):
        if ride.driver and ride.driver.vehicle and ride.driver.vehicle.commission_type:
            vehicle_commission_percentage_str = str(ride.driver.vehicle.commission_type.commission_percentage)
            vehicle_commission_percentage = Decimal(vehicle_commission_percentage_str)

            vehicle_commission_amount = (ride.total_fare * vehicle_commission_percentage) / Decimal(100)
            driver_commission = ride.total_fare - vehicle_commission_amount
            return driver_commission
        return Decimal(0)

    def calculate_company_commission(self, ride):
        driver_commission = self.calculate_driver_commission(ride)
        return ride.total_fare - driver_commission

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        context['company_format'] = vehicle.company_format  # Pass company format to the context
        return context


class VehicleListView(ListView):
    model = Vehicle
    template_name = "superadmin/vehicle_list.html"

    def get_queryset(self):
        # Use select_related to fetch related driver and owner details in one query
        return Vehicle.objects.select_related('owner').prefetch_related('driver_set').all()


class VehicleDailySummaryView(ListView):
    model = DailyVehicleComm
    template_name = "superadmin/vehicle_daily_summary.html"

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        # Get all unique dates with completed bookings for this vehicle
        completed_rides_dates = RideDetails.objects.filter(
            driver__vehicle=vehicle,
            ride_status='completedbookings'
        ).values_list('pickup_date', flat=True).distinct()

        for date in completed_rides_dates:
            # Filter rides by vehicle, status, and specific date
            rides = RideDetails.objects.filter(
                driver__vehicle=vehicle,
                ride_status='completedbookings',
                pickup_date=date
            )

            total_fare = Decimal(0)
            total_driver_commission = Decimal(0)
            total_company_commission = Decimal(0)

            # Calculate totals for each date
            for ride in rides:
                driver_commission = self.calculate_driver_commission(ride)
                company_commission = ride.total_fare - driver_commission

                total_fare += ride.total_fare
                total_driver_commission += driver_commission
                total_company_commission += company_commission

            # Debugging output
            print(f"vehicle: {vehicle}, date: {date}")
            print(f"total_fare: {total_fare}, total_driver_commission: {total_driver_commission}, total_company_commission: {total_company_commission}")

            # Update or create DailyVehicleComm records for each date
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

        # Return the queryset of all DailyVehicleComm records for this vehicle, ordered by date
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
    template_name = "superadmin/booking_details.html"

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        date = self.kwargs['date']
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        # Filter rides by vehicle and date
        rides = RideDetails.objects.filter(
            driver__vehicle=vehicle,
            ride_status='completedbookings',
            pickup_date=date
        ).order_by('pickup_time')

        # Calculate driver and company commissions for each ride
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
        