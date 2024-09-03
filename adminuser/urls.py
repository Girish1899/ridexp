from django.urls import path
from adminuser.views import *
from . import views

urlpatterns = [
    # path('index',adminuser_index,name='adminindex'),
    path('adindex/', views.adminuser_index, name='adindex'),
    
    # category##################
    path('adCategoryListView',views.CategoryListView.as_view(),name='adCategoryListView'),
    path('adCategoryHistory/<int:category_id>/', CategoryHistoryView.as_view(), name='adcategory_history'),

    # Brand #####################
    path('adBrandListView',views.BrandListView.as_view(),name='adBrandListView'),
    path('adBrandHistory/<int:brand_id>/', BrandHistoryView.as_view(), name='adbrand_history'),

    # Model ############################
    path('adModelListView',views.ModelListView.as_view(),name='adModelListView'),
    path('adModelHistory/<int:model_id>/', ModelHistoryView.as_view(), name='admodel_history'),

    #vehicletype################
    path('advehicletypeList', views.vehicletypeList.as_view(), name='advehicletypeList'),
    path('adVtypeHistory/<int:vehicle_type_id>/', VehicleTypeHistoryView.as_view(), name='adVtype_history'),
  
    #ridetype################  
    path('adridetypeList', views.ridetypeList.as_view(), name='adridetypeList'),
    path('adRtypeHistory/<int:ridetype_id>/', RidetypeHistoryView.as_view(), name='adRtype_history'),

    # User 
    path('aduserlist', views.UserList.as_view(), name='aduserlist'),
    path('adUserHistory/<int:user_id>/', ProfileHistoryView.as_view(), name='adUser_history'),

    # customer 
    path('adcustomerlist', views.CustomerList.as_view(), name='adcustomerlist'),
    path('adCustomerHistory/<int:customer_id>/', CustomerHistoryView.as_view(), name='adCustomer_history'),

    # vehicle owner##############################  
    path('adviewvehicleowner', views.OwnerListView.as_view(), name='adviewvehicleowner'),
    path('adVehicleownerHistory/<int:owner_id>/', VehicleOwnerHistoryView.as_view(), name='adVehicleowner_history'),

    # driverss####################### 
    path('adviewdriver', views.DriverListView.as_view(), name='adviewdriver'),
    path('adDriverHistory/<int:driver_id>/', DriverHistoryView.as_view(), name='addriver_history'),

    # vehicle ############################## 
    path('advehiclelist', views.VehicleList.as_view(), name='advehiclelist'),
    path('adVehicleHistory/<int:vehicle_id>/', VehicleHistoryView.as_view(), name='adVehicle_history'),

     # ride ############################## 
    path('ADaddbooking', AddRide.as_view(), name='ADaddbooking'),
    path('adridelist/<int:ride_id>/', RideList.as_view(), name='adridelist'),
    path('adridelist',RideList.as_view(), name='adridelist'),
    path('adcompleted-bookings-filter/', completed_bookings_filter, name='adcompleted_bookings_filter'),
    path('adadvance_bookings/', AdvanceBookingsList.as_view(), name='adadvance_bookings'),
    path('adpending_bookings/', PendingBookingsList.as_view(), name='adpending_bookings'),
    path('adview_assigned_rides', AssignedRideList.as_view(), name='adview_assigned_rides'),
    path('adongoing_rides', OngoingRideList.as_view(), name='adongoing_rides'),
    path('adcompleted_rides', CompletedRideList.as_view(), name='adcompleted_rides'),
    path('adcancelledbookings',CancelledListView.as_view(),name='adcancelledbookings'),
    # path('adcancel_ride', cancel_ride, name='adcancel_ride'),

    # path('adcurrent-bookings', AssignDriverView.as_view(), name='adcurrent_bookings'),
    path('adinvoice/<int:ride_id>/', InvoiceView.as_view(), name='adinvoice_view'),

    #profile
    path('adminuser_profile', adminuser_profile_view, name='adminuser_profile'),

    # path('profile', profile.as_view(), name='admin_profile'),
    path('update-user/', UpdateUserView.as_view(), name='admin_update_user'),

    path('adcommissionlist', CommissionList.as_view(), name='adcommissionlist'),
    path('adcommission_history/<int:commission_id>/', CommissionHistoryView.as_view(), name='adcommission_history'),

################## price details ###########################
    path('adpricinglist', PriceList.as_view(), name='adpricinglist'),
    path('adpricing_history/<int:pricing_id>/', PricingHistoryView.as_view(), name='adpricing_history'),




]