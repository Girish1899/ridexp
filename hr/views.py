from django.shortcuts import get_object_or_404, render
from superadmin.models import RideDetails,Customer,Driver,Vehicle
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Attendance, Profile, User
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



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
    return render(request,'hr/index.html',context)
      

@csrf_exempt
def fetch_employee_details(request):
    username = request.GET.get('username', None)
    if username:
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            employee_details = {
                'id': profile.id,
                'company_format': profile.company_format,
                'type': profile.type, 
            }
            return JsonResponse({'success': True, 'profile': employee_details})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Employee not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@method_decorator(login_required(login_url='login'), name='dispatch')
class addattendance(TemplateView, APIView):
    template_name = "hr/add_attendance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = Profile.objects.all()
        context['profiles'] = profiles
        return context

    def post(self, request):
        print("POST request data:", request.POST)

        profile_id = request.POST.get('profile_id')
        date = request.POST.get('date')
        mark_attendance = request.POST.get('mark_attendance')

        print("Profile ID:", profile_id)
        print("Date:", date)
        print("Mark Attendance:", mark_attendance)

        if not profile_id:
            print("Error: Profile ID is required")
            return JsonResponse({'status': "Error", 'message': "Profile ID is required"})

        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            print("Error: Profile not found")
            return JsonResponse({'status': "Error", 'message': "Profile not found"})

        login_time = request.POST.get('login_time')
        logout_time = request.POST.get('logout_time')
        duration = request.POST.get('duration')

        print("Login Time:", login_time)
        print("Logout Time:", logout_time)
        print("Duration:", duration)

        attendance = Attendance(
            profile=profile,
            date=date,
            mark_attendance=mark_attendance,
            login_time=login_time if mark_attendance == 'Present' else None,
            logout_time=logout_time if mark_attendance == 'Present' else None,
            duration=duration if mark_attendance == 'Present' else None
        )

        attendance.save()
        print("Attendance saved:", attendance)

        return JsonResponse({'status': "Success", 'message': "Attendance added successfully"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class AttendanceListView(ListView):
    model = Attendance
    template_name = "hr/view_attendance.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendances'] = Attendance.objects.all()
        return context 

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAttendance(View):
    def  get(self, request):
        attendance_Id = request.GET.get('attendance_Id', None)
        Attendance.objects.get(attendance_Id=attendance_Id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)         

@login_required
def hr_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='hr')
    return render(request, 'hr/app-profile.html', {'profile': profile})