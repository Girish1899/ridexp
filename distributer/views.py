from datetime import date, datetime, time
from decimal import Decimal
import json
import os
import random
from django.db import IntegrityError
from django.shortcuts import render
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View,DetailView
from rest_framework.response import Response
from rest_framework import status
from superadmin.models import Blogs, Brand, BrandHistory,Category, CategoryHistory, Color, ColorHistory, CommissionHistory, CommissionType, CustomerHistory, DailyVehicleComm, DriverHistory, Enquiry,Model, ModelHistory, PackageCategories, PackageCategoriesHistory, Pricing, Profile, RideDetails, RideDetailsHistory, RidetypeHistory, Transmission, TransmissionHistory,User,Customer,Driver,Ridetype,Vehicle, VehicleHistory, VehicleOwner, VehicleOwnerHistory, VehicleType, VehicleTypeHistory, WebsitePackages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum, Count
import zipfile
from django.http import HttpResponse
from django.core.cache import cache
import requests
from django.db.models import  Max
from docxtpl import DocxTemplate
from docx2pdf import convert
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from PIL import Image
from io import BytesIO
from django.core.exceptions import ObjectDoesNotExist
import os
from django.core.files.base import ContentFile
from django.contrib import messages

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
    return render(request,'distributer/index.html',context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addbrand(TemplateView):
    template_name = "distributer/add_brand.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active')
        brands = Brand.objects.all().values('category_id', 'brand_name')
        context['catlist'] = catlist
        context['brands'] = brands
        return context

    def post(self, request):
        user_type = self.request.session.get('user_type')
        if user_type != "distributer":
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
    template_name = "distributer/view_brand.html"

    def get(self, request, *args, **kwargs):
        user_typ = self.request.session.get('user_type')
        if user_typ !="distributer":
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
    template_name = 'distributer/edit_brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        catlist = Category.objects.filter(category_status='active') 
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

        brand.brand_name = request.POST['brand_name']
        brand.category = Category.objects.get(category_id=request.POST.get('category'))
        brand.status = request.POST['status']
        brand.updated_by = request.user
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
    template_name = 'distributer/history_brand.html'

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
    template_name = 'distributer/detailview_brand.html'

    def get(self, request, brand_id):
        brandlist = get_object_or_404(Brand, pk=brand_id)
        return render(request, self.template_name, {'brandlist': brandlist})  
    
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
    template_name = "distributer/add_category.html"

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
            img = Image.open(image)
            
            img = img.resize((880, 450), Image.LANCZOS)

            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg']:
                format = 'JPEG'
            elif file_extension == '.png':
                format = 'PNG'
            elif file_extension == '.gif':
                format = 'GIF'
            else:
                format = 'JPEG'  

            img_io = BytesIO()
            img.save(img_io, format=format)
            img_content = ContentFile(img_io.getvalue(), image.name)

            cat.image.save(image.name, img_content, save=False)

        cat.save()
        return JsonResponse({'status': "Success"})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = "distributer/view_category.html"

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
    template_name = 'distributer/edit_category.html'
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

        category.category_name = request.POST['category_name']
        category.seats = request.POST['seats']
        category.category_status = request.POST['category_status']
        category.updated_by = request.user 

        print('post datas', category.category_name)

        if 'image' in request.FILES:
            image = request.FILES['image']
            img = Image.open(image)
            
            img = img.resize((880, 450), Image.LANCZOS)

            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg']:
                format = 'JPEG'
            elif file_extension == '.png':
                format = 'PNG'
            elif file_extension == '.gif':
                format = 'GIF'
            else:
                format = 'JPEG'  

            img_io = BytesIO()
            img.save(img_io, format=format)
            img_content = ContentFile(img_io.getvalue(), image.name)

            category.image.save(image.name, img_content, save=False)

        category.save()
        print('after saving datas', category.category_name)

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
    template_name = 'distributer/history_category.html'

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

class ViewCategory(View):
    template_name = 'distributer/detailview_category.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return render(request, self.template_name, {'category': category})

        

@method_decorator(login_required(login_url='login'), name='dispatch')
class addmodel(TemplateView):
    template_name = "distributer/add_model.html"

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
    template_name = "distributer/view_model.html"

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
    template_name = 'distributer/edit_model.html'
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

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateModel(APIView):
    def post(self, request):
        model_id = request.POST['model_id']
        model_name = request.POST['model_name']
        brand_id = request.POST['brand']
        status = request.POST['status']

        if Model.objects.filter(brand_id=brand_id, model_name=model_name).exclude(model_id=model_id).exists():
            return JsonResponse({'success': False, 'message': "Model already exists for the selected brand."}, status=400)

        model = get_object_or_404(Model, model_id=model_id)
        original_model_status = model.status

        model.model_name = model_name
        model.brand_id = brand_id
        model.status = status
        model.updated_by = request.user
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

        if original_model_status != model.status:
            vehicles = model.vehicles.all()  
            for vehicle in vehicles:
                if vehicle.vehicle_status != model.status:
                    vehicle.vehicle_status = model.status
                    vehicle.save()

        return JsonResponse({'success': True}, status=200)

class ModelHistoryView(TemplateView):
    template_name = 'distributer/history_model.html'

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
    template_name = 'distributer/detailview_model.html'

    def get(self, request, model_id):
        mlist = get_object_or_404(Model, pk=model_id)
        return render(request, self.template_name, {'mlist': mlist})         
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class addvehicletype(TemplateView):
    template_name = "distributer/add_vehicletype.html"

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
    template_name = "distributer/view_vehicletype.html"

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
    template_name = 'distributer/edit_vehicletype.html'
    
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

        vehicle_type.company_format = request.POST['company_format']
        vehicle_type.vehicle_type_name = request.POST['vehicle_type_name']
        vehicle_type.updated_by = request.user
        vehicle_type.save()

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
    template_name = 'distributer/history_vehicletype.html'

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
    template_name = 'distributer/detailview_vehicletype.html'

    def get(self, request, vehicle_type_id):
        vtlist = get_object_or_404(VehicleType, pk=vehicle_type_id)
        return render(request, self.template_name, {'vtlist': vtlist})  
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class addridetype(TemplateView):
    template_name = "distributer/add_ridetype.html"

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
    template_name = "distributer/view_ridetype.html"

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
    template_name = 'distributer/edit_ridetype.html'
    
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

        ridetype.company_format = request.POST['company_format']
        ridetype.name = request.POST['name']
        ridetype.updated_by = request.user
        ridetype.save()

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
    template_name = 'distributer/history_ridetype.html'

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
    template_name = 'distributer/detailview_ridetype.html'

    def get(self, request, ridetype_id):
        rtlist = get_object_or_404(Ridetype, pk=ridetype_id)
        return render(request, self.template_name, {'rtlist': rtlist})  
    
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
    template_name = "distributer/add_transmission.html"

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
    template_name = "distributer/view_transmission.html"

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
    template_name = 'distributer/edit_transmission.html'
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

        transmission.transmission_name = request.POST['transmission_name']
        transmission.updated_by = request.user
        transmission.save()

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
    template_name = 'distributer/history_transmission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transmission_id = self.kwargs['transmission_id']
        transmission = get_object_or_404(Transmission, transmission_id=transmission_id)
        history = TransmissionHistory.objects.filter(transmission_id=transmission_id).order_by('updated_on')
        context['transmission'] = transmission
        context['history'] = history
        return context 

class ViewTransmission(View):
    template_name = 'distributer/detailview_transmission.html'

    def get(self, request, transmission_id):
        tlist = get_object_or_404(Transmission, pk=transmission_id)
        return render(request, self.template_name, {'tlist': tlist})          



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
    template_name = "distributer/add_color.html"

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
    template_name = "distributer/view_color.html"

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
    template_name = 'distributer/edit_color.html'
    
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

        color.name = request.POST['name']
        color.updated_by = request.user
        color.save()

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
    template_name = 'distributer/history_color.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color_id = self.kwargs['color_id']
        color = get_object_or_404(Color, color_id=color_id)
        history = ColorHistory.objects.filter(color_id=color_id).order_by('updated_on')
        context['color'] = color
        context['history'] = history
        return context


class ViewColor(View):
    template_name = 'distributer/detailview_color.html'

    def get(self, request, color_id):
        clist = get_object_or_404(Color, pk=color_id)
        return render(request, self.template_name, {'clist': clist})  

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
                customer.block_reason = ''  
            customer.save()

            CustomerHistory.objects.create(
                customer_id=customer.customer_id,
                company_format=customer.company_format,
                customer_name=customer.customer_name,
                phone_number=customer.phone_number,
                address=customer.address,
                email=customer.email,
                password=customer.password,
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
    template_name = "distributer/add_customer.html"

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
    template_name = "distributer/view_customer.html"
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
    template_name = 'distributer/edit_customer.html'
    
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

        customer.company_format = request.POST['company_format']
        customer.customer_name = request.POST['customer_name']
        customer.phone_number = request.POST['phone_number']
        customer.address = request.POST['address']
        customer.email = request.POST['email']
        customer.password = request.POST['password']
        customer.status = request.POST['status']
        customer.updated_by = request.user
        customer.save()

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
    template_name = 'distributer/history_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.kwargs['customer_id']
        customer = get_object_or_404(Customer, customer_id=customer_id)
        history = CustomerHistory.objects.filter(customer_id=customer_id).order_by('updated_on')
        context['customer'] = customer
        context['history'] = history
        return context

class ViewCustomer(View):
    template_name = 'distributer/detailview_customer.html'

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

        context = {
            'customer': customer,
            'current_bookings': current_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'advanced_bookings': advanced_bookings,
            'assigned_bookings': assigned_bookings,
            'ongoing_booking': ongoing_booking,
        }
        return render(request, 'distributer/customer_bookings.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomerProfileList(ListView):
    model = Customer
    template_name = "distributer/cust_profile_list.html" 

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
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class addcommission(TemplateView):
    template_name = "distributer/add_commissiontype.html"

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
    template_name = "distributer/view_commissiontype.html"

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
    template_name = 'distributer/edit_commissiontype.html'
    
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

        commission.commission_name = request.POST['commission_name']
        commission.commission_percentage = request.POST['commission_percentage']
        commission.updated_by = request.user
        commission.save()

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
    template_name = 'distributer/history_commission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission_id = self.kwargs['commission_id']
        commission = get_object_or_404(CommissionType, commission_id=commission_id)
        history = CommissionHistory.objects.filter(commission_id=commission_id).order_by('updated_on')
        context['commission'] = commission
        context['history'] = history
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CommVehicleListView(ListView):
    model = RideDetails
    template_name = "distributer/comm_vehiclelist.html"
    
    def get_queryset(self):
        latest_bookings = RideDetails.objects.filter(
            ride_status='completedbookings'
        ).values('driver').annotate(
            latest_pickup_date=Max('pickup_date')
        )

        queryset = RideDetails.objects.filter(
            driver__in=[booking['driver'] for booking in latest_bookings],
            pickup_date__in=[booking['latest_pickup_date'] for booking in latest_bookings],
            ride_status='completedbookings'
        ).select_related('driver', 'driver__vehicle', 'driver__vehicle__owner')

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
    template_name = "distributer/vehicle_commission_detail.html"
    
    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        queryset = RideDetails.objects.filter(
            driver__vehicle__vehicle_id=vehicle_id,
            ride_status='completedbookings'
        ).select_related('driver', 'driver__vehicle')

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
        context['company_format'] = vehicle.company_format  
        return context


class VehicleListView(ListView):
    model = Vehicle
    template_name = "distributer/vehicle_list.html"

    def get_queryset(self):
        return Vehicle.objects.select_related('owner').prefetch_related('driver_set').all()


class VehicleDailySummaryView(ListView):
    model = DailyVehicleComm
    template_name = "distributer/vehicle_daily_summary.html"

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
    template_name = "distributer/booking_details.html"

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
    template_name = "distributer/add_vehicleowner.html"

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
    template_name = "distributer/view_vehicleowner.html"

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
    template_name = 'distributer/edit_vehicleowner.html'
    
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

        if original_owner_status != owner.status:
            vehicles = owner.vehicle_set.all()  
            for vehicle in vehicles:
                if vehicle.vehicle_status != owner.status:
                    vehicle.vehicle_status = owner.status
                    vehicle.save()

        return JsonResponse({'success': True}, status=200)

class VehicleOwnerHistoryView(TemplateView):
    template_name = 'distributer/history_vehicleowner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_id = self.kwargs['owner_id']
        owner = get_object_or_404(VehicleOwner, owner_id=owner_id)
        history = VehicleOwnerHistory.objects.filter(owner_id=owner_id).order_by('updated_on')
        context['owner'] = owner
        context['history'] = history
        return context

class ViewOwner(View):
    template_name = 'distributer/detailview_owner.html'

    def get(self, request, owner_id):
        ownerlist = get_object_or_404(VehicleOwner, pk=owner_id)
        return render(request, self.template_name, {'ownerlist': ownerlist}) 
    

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

@method_decorator(login_required(login_url='login'), name='dispatch')
class OwnerVerification(ListView):
    model = VehicleOwner
    template_name = "distributer/viewownerverification.html"   

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
    template_name = "distributer/add_vehicle.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['catlist'] = Category.objects.filter(category_status='active')
        context['blist'] = Brand.objects.filter(status='active')
        context['ownerlist'] = VehicleOwner.objects.filter(status='active',verification_status='verified')
        context['modellist'] = Model.objects.filter(status='active')
        context['vtypelist'] = VehicleType.objects.all()
        context['ctypelist'] = CommissionType.objects.all()
        context['colorlist'] = Color.objects.all()
        context['tlist'] = Transmission.objects.all()
        
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
    template_name = "distributer/view_vehicle.html"

    def get_queryset(self):
        return Vehicle.objects.filter(Q(vehicle_status='active'))

@method_decorator(login_required(login_url='login'), name='dispatch')
class VehicleBlockList(ListView):
    model = Vehicle
    template_name = "distributer/view_vehicleblock.html"

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
    template_name = 'distributer/edit_vehicle.html'
  
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
    template_name = 'distributer/history_vehicle.html'

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
                vehicle.block_reason = ''  
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

class ViewVehicle(View):
    template_name = 'distributer/detailview_vehicle.html'

    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        driver = Driver.objects.filter(vehicle=vehicle).first() 
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
                    'id': vehicle.vehicle_id,  
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
    template_name = "distributer/add_driver.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_driver = Driver.objects.order_by('-driver_id').first()
        if last_driver and last_driver.company_format:
            last_company_format = int(last_driver.company_format.replace('DRIV', ''))
            next_company_format = f'DRIV{last_company_format + 1:02}'
        else:
            next_company_format = 'DRIV01'
        context['next_company_format'] = next_company_format

        all_vehicles = Vehicle.objects.filter(
            vehicle_status='active',
            verification_status='verified'
        )
        

        assigned_vehicle_ids = Driver.objects.values_list('vehicle_id', flat=True)
        
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

            if vehicle.drive_status == 'selfdrive':
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
    template_name = "distributer/view_driver.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DriverVerificationView(ListView):
    model = Driver
    template_name = "distributer/view_driververification.html"    

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
    template_name = 'distributer/edit_driver.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_vehicles = Vehicle.objects.filter(
            vehicle_status='active',
            verification_status='verified'
        )
        
        assigned_vehicle_ids = Driver.objects.values_list('vehicle_id', flat=True)
        
        unassigned_vehicles = [vehicle for vehicle in all_vehicles if vehicle.vehicle_id not in assigned_vehicle_ids]
        
        context['vehiclelist'] = unassigned_vehicles
        
        try:
            context['driver_id'] = self.kwargs['id']
            driverlist = Driver.objects.filter(driver_id=context['driver_id'])
        except KeyError:
            driverlist = Driver.objects.none()
        
        context['driverlist'] = list(driverlist)
        
        return context

from django.contrib.auth.models import User

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateDriverView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            driver_id = request.POST.get('driver_id')
            vehicle_id = request.POST.get('vehicle', None)

            if not driver_id:
                return JsonResponse({'success': False, 'error': 'Missing driver_id'}, status=400)

            try:
                driver_id = int(driver_id)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid driver_id format'}, status=400)

            try:
                driver = Driver.objects.get(driver_id=driver_id)
            except Driver.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Driver not found'}, status=404)

            if vehicle_id:
                try:
                    vehicle_id = int(vehicle_id)
                    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
                    driver.vehicle = vehicle
                except (ValueError, Vehicle.DoesNotExist):
                    return JsonResponse({'success': False, 'error': 'Vehicle not found'}, status=404)

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

            try:
                user = User.objects.get(email=driver.email)
                user.username = request.POST.get('name', driver.name)
                user.email = new_email 
                user.save()
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found for the driver'}, status=404)

            driver.name = request.POST.get('name', driver.name)
            driver.phone_number = new_phone_number
            driver.email = new_email  
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
    template_name = 'distributer/history_driver.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_id = self.kwargs['driver_id']
        driver = get_object_or_404(Driver, driver_id=driver_id)
        history = DriverHistory.objects.filter(driver_id=driver_id)
        context['driver'] = driver
        context['history'] = history
        return context

class ViewDriver(View):
    template_name = 'distributer/detailview_driver.html'

    def get(self, request, driver_id):
        driverlist = get_object_or_404(Driver, pk=driver_id)
        return render(request, self.template_name, {'driverlist': driverlist}) 

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
    template_name = "distributer/driver_report.html"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all() 
        context['drivers'] = Driver.objects.all() 
        return context


def fetch_vehicle_details(request):
    if request.method == "GET":
        vehicle_company_format = request.GET.get('vehicle_company_format')
        print("--------",request.GET)
        try:
            vehicle = Vehicle.objects.select_related(
                'model__brand__category'
            ).get(company_format=vehicle_company_format)
            response = {
                'success': True,
                'vehicle': {
                    'id': vehicle.vehicle_id,
                    'Vehicle_Number': vehicle.Vehicle_Number,
                    'category_name': vehicle.model.brand.category.category_name,
                    'brand_name': vehicle.model.brand.brand_name,
                    'model_name': vehicle.model.model_name
                }
            }
        except Vehicle.DoesNotExist:
            response = {
                'success': False,
                'message': 'Vehicle not found'
            }
        return JsonResponse(response)
 

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
    template_name = "distributer/add_ride.html"

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
    template_name = "distributer/view_ride.html"

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
    template_name = "distributer/advance_bookings.html" 

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
    template_name = "distributer/pending_bookings.html"  

    def get_queryset(self):
        today = date.today()
        return RideDetails.objects.filter(ride_status='pendingbookings', pickup_date__lt=today)
    
class OngoingRideList(ListView):
    model = RideDetails
    template_name = "distributer/ongoing_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='ongoingbookings') & Q(assigned_by=self.request.user)).select_related('driver') 

    
class CompletedRideList(ListView):
    model = RideDetails
    template_name = "distributer/completed_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='completedbookings') & Q(assigned_by=self.request.user)).select_related('driver')
    


class InvoiceView(DetailView):
    model = RideDetails
    template_name = 'distributer/invoice.html'
    context_object_name = 'ride'
    
    def get_object(self):
        ride_id = self.kwargs.get("ride_id")
        return get_object_or_404(RideDetails, ride_id=ride_id)    

class AssignDriverView(ListView):
    model = Driver
    template_name = 'distributer/view_ride.html'
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
    template_name = 'distributer/edit_ride.html'
  
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
    template_name = 'distributer/history_ride.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride_id = self.kwargs['ride_id']
        ride = get_object_or_404(RideDetails, ride_id=ride_id)
        history = RideDetailsHistory.objects.filter(ride_id=ride_id).order_by('updated_on')
        context['ride'] = ride
        context['history'] = history
        return context


@login_required
def distributer_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='distributer')
    return render(request, 'distributer/app-profile.html', {'profile': profile})
    
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignedRideList(ListView):
    model = RideDetails
    template_name = "distributer/assigned_rides.html"

    def get_queryset(self):
        return RideDetails.objects.filter(Q(ride_status='assignbookings') & Q(assigned_by=self.request.user)).select_related('driver')


@method_decorator(login_required(login_url='login'), name='dispatch')
class AssignLaterList(ListView):
    model = RideDetails
    template_name = "distributer/assign_later.html"

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
        return RideDetails.objects.filter(Q(ride_status='assignlaterbookings') & Q(assigned_by=self.request.user)).select_related('driver')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class CancelledListView(ListView):
    model = RideDetails
    template_name = "distributer/view_cancelbookings.html"

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


class InvoiceView(View):
    
    def get(self, request, *args, **kwargs):

        try:
            ride_id = self.kwargs.get("ride_id")
            
            try:
                ride = RideDetails.objects.get(ride_id=ride_id)
            except RideDetails.DoesNotExist:
                return JsonResponse({'success': False, 'message': "Ride not found."})

            template_path = os.path.join("media", "Invoice_template.docx")
            template = DocxTemplate(template_path)

            current_date = datetime.now().strftime('%d-%m-%Y')

            sList = {
                'serv_type': 'Drop',
                'serv_desp': f"{ride.source} - {ride.destination}",
                'serv_amount': str(ride.total_fare),
            }

            context = {
                'invno': '0002',  
                'sdate': current_date,  
                'sptype': 'September 2024',
                'spstatus': 'Completed',
                'serv_customer_name': ride.customer.customer_name,
                'servrtype': ride.ridetype.name,
                'servcarno': ride.driver.vehicle.Vehicle_Number,
                'serv_dist_trav': '12KM',
                'serv_sub_total': ride.total_fare,
                'serv_sgst': '18',
                'serv_cgst': '12',
                'serv': sList,
                'ttial': ride.total_fare,
            }

            output_docx = os.path.join("media", f"RideXpress_Invoice_{ride_id}.docx")
            template.render(context)
            template.save(output_docx)

            print("Document saved successfully!")

            output_pdf = os.path.join("media", f"RideXpress_Invoice_{ride_id}.pdf")
            convert(output_docx, output_pdf)

            print("Conversion complete! PDF saved.")

            return JsonResponse({'success': True, 'message': f"Invoice for ride {ride_id} generated successfully!"})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        


class EnquiryList(ListView):
    model = Enquiry
    template_name = "distributer/view_enquiry.html"     
        

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
    template_name = "distributer/add_package_category.html"

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
    template_name = "distributer/view_package_category.html"

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
    template_name = 'distributer/edit_package_category.html'
    
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
    template_name = 'distributer/history_package_category.html'

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
    template_name = "distributer/add_webpackages.html"

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
    template_name = "distributer/view_webpackages.html"

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
    template_name = 'distributer/edit_webpackages.html'

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
    template_name = "distributer/add_blog.html"

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
    template_name = "distributer/view_blog.html"

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
    template_name = 'distributer/edit_blog.html'

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
