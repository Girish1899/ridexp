from django.urls import path
from distributer.views import *

urlpatterns = [

    path('',index,name='indexd'),
    # driverss#######################
    path('distributerviewdriver', DriverListView.as_view(), name='distributerviewdriver'),
    path('fetch_vehicle_details/', fetch_vehicle_details, name='fetch_vehicle_details'),
    path('check_dphonenumber', check_dphonenumber, name='check_dphonenumber'),
    path('distributerEditDriver/<int:id>/', EditDriverView.as_view(), name='distributerEditDriver'),
    path('distributerupdatedriver', UpdateDriverView.as_view(), name='distributerupdatedriver'),

    # ride details ###########################
    path('distributeraddride', AddRide.as_view(), name='distributeraddride'),
    path('distributerridelist', RideList.as_view(), name='distributerridelist'),
    path('distributerEditRide/<int:id>/', EditRide.as_view(), name='distributerEditRide'),
    path('distributerUpdateRide', UpdateRide.as_view(), name='distributerUpdateRide'),
    # path('fetch_customer_details/',fetch_customer_details, name='fetch_customer_details'),
    path('distributerDeleteRide', DeleteRide.as_view(), name='distributerDeleteRide'),

    # bookings####################################################################
    path('distributerridelist/<int:ride_id>/', RideList.as_view(), name='distributerridelist'),
    path('distributerassign_driver', assign_driver, name='distributerassign_driver'),
    path('distributeradvanceassign_driver', advanceassign_driver, name='distributeradvanceassign_driver'),
    path('distributer_view_assignlater', AssignLaterList.as_view(), name='distributer_view_assignlater'),
    # path('distributer_update_ride_status', distributer_update_ride_status, name='distributer_update_ride_status'),


    path('distributerRideHistory/<int:ride_id>/', RideDetailsHistoryView.as_view(), name='distributerRideHistory'),
    path('distributerview_assigned_rides', AssignedRideList.as_view(), name='distributerview_assigned_rides'),
    path('distributerongoing_rides', OngoingRideList.as_view(), name='distributerongoing_rides'),
    path('distributercompleted_rides', CompletedRideList.as_view(), name='distributercompleted_rides'),
    path('distributercancelledbookings',CancelledListView.as_view(),name='distributercancelledbookings'),
    path('distributercancel_ride', cancel_ride, name='distributercancel_ride'),

    path('distributercurrent-bookings', AssignDriverView.as_view(), name='distributercurrent_bookings'),

    path('distributeradvance_bookings', AdvanceBookingsList.as_view(), name='distributeradvance_bookings'),
    path('distributerpending_bookings', PendingBookingsList.as_view(), name='distributerpending_bookings'),
    path('distributercurrent-bookings', AssignDriverView.as_view(), name='distributercurrent_bookings'),
    path('distributerinvoice/<int:ride_id>/', InvoiceView.as_view(), name='distributerinvoice_view'),


    #profile
    # path('profile', profile.as_view(), name='distributer_profile'),
    path('distributer_profile', distributer_profile_view, name='distributer_profile'),

    path('update-user/', UpdateUserView.as_view(), name='distributer_update_user'),

    path('send_otp_distributer/', SendOtp.as_view(), name='send_otp_distributer'),
    path('verify_otp_distributer/', VerifyOtp.as_view(), name='verify_otp_distributer'),
    path('distributerPricingDetails', customerGetRidePricingDetails.as_view(), name='distributerPricingDetails'),

    path('distributer_invoice/<int:ride_id>/', InvoiceView.as_view(), name='distributer_invoice_view'),


    

]