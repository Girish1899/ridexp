from django.urls import path
from hr.views import *

urlpatterns = [

    path('hrindex',index,name='hrindex'),
    path('fetch_employee_details/', fetch_employee_details, name='fetch_employee_details'),

    path('addattendance',addattendance.as_view(),name='addattendance'),
    path('attendancelist',AttendanceListView.as_view(),name='attendancelist'),
    path('DeleteAttendance',DeleteAttendance.as_view(),name='DeleteAttendance'),
    path('hr_profile', hr_profile_view, name='hr_profile'),


]