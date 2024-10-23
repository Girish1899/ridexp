from django.urls import path

from rescue.views import *

urlpatterns = [

    path('',rescueindex,name='rescueindex'),
   
    path('rescueaddbooking', AddRide.as_view(), name='rescueaddbooking'),
    path('rescueridelist/<int:ride_id>/', RideList.as_view(), name='rescueridelist'),
    path('rescueridelist', RideList.as_view(), name='rescueridelist'),
    path('rescueassign_driver', assign_driver, name='rescueassign_driver'),
    path('rescueRideHistory/<int:ride_id>/', RideDetailsHistoryView.as_view(), name='rescueRideHistory'),
    path('rescueadvance_bookings', AdvanceBookingsList.as_view(), name='rescueadvance_bookings'),
    path('rescuepending_bookings', PendingBookingsList.as_view(), name='rescuepending_bookings'),
    path('rescueview_assigned_rides', AssignedRideList.as_view(), name='rescueview_assigned_rides'),
    path('rescueongoing_rides', OngoingRideList.as_view(), name='rescueongoing_rides'),
    path('rescuecompleted_rides', CompletedRideList.as_view(), name='rescuecompleted_rides'),
    path('rescuecancelledbookings',CancelledListView.as_view(),name='rescuecancelledbookings'),
    path('rescuecancel_ride', cancel_ride, name='rescuecancel_ride'),

    path('rescuecurrent-bookings', AssignDriverView.as_view(), name='rescuecurrent_bookings'),
    path('rescueinvoice/<int:ride_id>/', InvoiceView.as_view(), name='rescueinvoice_view'),

    path('rescuedriverlist', DriverListView.as_view(), name='rescuedriverlist'),
    path('RescueEditDriver/<int:id>/', EditDriverView.as_view(), name='RescueEditDriver'),
    path('rescueupdatedriver', UpdateDriverView.as_view(), name='rescueupdatedriver'),

    path('rescuecustomerlist', CustomerList.as_view(), name='rescuecustomerlist'),
    path('RescueEditCustomer/<int:id>/', EditCustomer.as_view(), name='RescueEditCustomer'),
    path('RescueUpdateCustomer', UpdateCustomer.as_view(), name='RescueUpdateCustomer'),  

    path('update-user/', UpdateUserView.as_view(), name='rescue_update_user'),
    path('rescue_profile', rescue_profile_view, name='rescue_profile'),

]