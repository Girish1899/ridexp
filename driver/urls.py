from django.urls import path
from driver.views import *

urlpatterns = [

    path('driverindex',driverindex,name='driverindex'),
    # path('driverridelist',DriverrideView.as_view(),name="driverridelist"),
    # path('driver_app_dashboard', driver_dashboard, name='driver_app_dashboard'),
    # path('ride_list/<str:driver_id>/', driver_ride_list_view, name='driver_ride_list'),
    # path('driver/start_ride/', start_ride, name='start_ride'),
    # path('driver/stop_ride/', stop_ride, name='stop_ride'),
    path('assigned_rides/', assigned_rides_view, name='assigned_rides'),
    path('start_ride/', start_ride, name='start_ride'),
    path('stop_ride/', stop_ride, name='stop_ride'),
    path('driver_profile/', driver_profile_view, name='driver_profile'),

    
]