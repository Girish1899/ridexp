from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from superadmin.models import Customer, Driver, Ridetype, Vehicle
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
    

def global_fetch_vehicle_details(request):
    if request.method == "GET":
        vehicle_company_format = request.GET.get('vehicle_company_format')
        try:
            vehicle = Vehicle.objects.select_related(
                'model__brand__category', 'owner'
            ).get(company_format=vehicle_company_format)
            vehicle_data = {
                'id': vehicle.vehicle_id,
                'Vehicle_Number': vehicle.Vehicle_Number,
                'category_name': vehicle.model.brand.category.category_name,
                'brand_name': vehicle.model.brand.brand_name,
                'model_name': vehicle.model.model_name,
                'drive_status': vehicle.drive_status,
            }
            if vehicle.drive_status == 'selfdrive':
                vehicle_data.update({
                    'owner_name': vehicle.owner.name,
                    'owner_phone_number': vehicle.owner.phone_number,
                    'owner_email': vehicle.owner.email,
                    'owner_address': vehicle.owner.address,
                    'owner_profile_image': vehicle.owner.image.url if vehicle.owner.image else '',
                    'owner_address_proof': vehicle.owner.address_proof.url if vehicle.owner.address_proof else '',
                })
            response = {
                'success': True,
                'vehicle': vehicle_data
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

