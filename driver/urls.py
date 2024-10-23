from django.urls import path
from driver.views import *

urlpatterns = [

    path('driverindex',driverindex,name='driverindex'),
    path('assigned_rides/', assigned_rides_view, name='assigned_rides'),
    path('start_ride/', start_ride, name='start_ride'),
    path('stop_ride/', stop_ride, name='stop_ride'),
    path('driver_profile/', driver_profile_view, name='driver_profile'),

    
]