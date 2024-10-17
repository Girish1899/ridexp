from django.urls import path
from telecaller.views import *


urlpatterns = [
    path('',index,name='indextel'),
    
# customer
    path('telecalleraddcustomer', addcustomer.as_view(), name='telecalleraddcustomer'),
    path('telecallercustomerlist', CustomerList.as_view(), name='telecallercustomerlist'),
    path('telecallerEditCustomer/<int:id>/', EditCustomer.as_view(), name='telecallerEditCustomer'),
    path('telecallerUpdateCustomer', UpdateCustomer.as_view(), name='telecallerUpdateCustomer'),  

    # ride details ###########################
    path('fetch_customer_details/', get_customer_details, name='fetch_customer_details'),
    path('tele_send_otp_admin/', SendOtp.as_view(), name='tele_send_otp_admin'),
    path('tele_verify_otp_admin/', VerifyOtp.as_view(), name='tele_verify_otp_admin'),
    path('telecalleraddride', AddRide.as_view(), name='telecalleraddride'),
    path('telecallerridelist', RideList.as_view(), name='telecallerridelist'),
    path('telecallerEditRide/<int:id>/', EditRide.as_view(), name='telecallerEditRide'),
    path('telecallerUpdateRide', UpdateRide.as_view(), name='telecallerUpdateRide'),


    path('telecaller_customerGetRidePricingDetails',customerGetRidePricingDetails.as_view(),name='telecaller_customerGetRidePricingDetails'),

    path('telecallercancelledbookings',CancelledListView.as_view(),name='telecallercancelledbookings'),
    path('update_cancel_status/<int:ride_id>/',update_ride_status, name='update_cancel_status'),
    path('telecallercancel_ride', cancel_ride, name='telecallercancel_ride'),
    path('telecalleradvance_bookings', AdvanceBookingsList.as_view(), name='telecalleradvance_bookings'),


    #profile
    path('profile', profile.as_view(), name='tele_profile'),
    path('update-user/', UpdateUserView.as_view(), name='tele_update_user'),
    path('callhistory', CalHistory.as_view(), name='callhistory'),

]