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
    path('adUserHistory/<int:user_id>/', ProfileHistoryView.as_view(), name='adUserHistory'),
    path('aduseremp', UserEmpList.as_view(), name='aduseremp'),


    # customer 
    path('adcustomerlist', views.CustomerList.as_view(), name='adcustomerlist'),
    path('adCustomerHistory/<int:customer_id>/', CustomerHistoryView.as_view(), name='adCustomer_history'),

    # vehicle owner##############################  
    path('adviewvehicleowner', views.OwnerListView.as_view(), name='adviewvehicleowner'),
    path('adVehicleownerHistory/<int:owner_id>/', VehicleOwnerHistoryView.as_view(), name='adVehicleowner_history'),

    # driverss####################### 
    path('adviewdriver', DriverListView.as_view(), name='adviewdriver'),
    path('adDriverHistory/<int:driver_id>/', DriverHistoryView.as_view(), name='addriver_history'),

    # vehicle ############################## 
    path('advehiclelist', views.VehicleList.as_view(), name='advehiclelist'),
    path('adVehicleHistory/<int:vehicle_id>/', VehicleHistoryView.as_view(), name='adVehicle_history'),

     # ride ############################## 
    path('adaddbookings', AddRide.as_view(), name='adaddbookings'),
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


    path('adcolorList', colorList.as_view(), name='adcolorList'),
    path('adColorHistory/<int:color_id>/', ColorHistoryView.as_view(), name='adColorHistory'),
    path('adTransmissionHistory/<int:transmission_id>/', TransmissionHistoryView.as_view(), name='adtransmission_history'),
    path('adTransmissionListView',TransmissionListView.as_view(),name='adTransmissionListView'),
    path('advehicleblocklist', VehicleBlockList.as_view(), name='advehicleblocklist'),
    path('adcustomer_profile/<int:customer_id>/', CustomerProfileHistoryView.as_view(), name='adcustomer_profile'),
    path('adcust_profile_list', CustomerProfileList.as_view(), name='adcust_profile_list'),

    path('advehicles/', VehicleListView.as_view(), name='advehicles'),
    path('advehicles/<str:vehicle_id>/daily-summary/', VehicleDailySummaryView.as_view(), name='advehicle_daily_summary'),
    path('advehicle/<int:vehicle_id>/details/<str:date>/', BookingDetailsView.as_view(), name='adbooking_details'),

    path('adaccounts_list', AccountsListView.as_view(), name='adaccounts_list'),

    #contact #########################
    path('adcontactlist', ContactList.as_view(), name='adcontactlist'),

#  enquiry ################################
    path('adenquirylist', EnquiryList.as_view(), name='adenquirylist'), 

    # package #######################

    path('adpackage_category_list', PackageCategoryList.as_view(), name='adpackage_category_list'),
    path('adpackage_name_list', PackageNameList.as_view(), name='adpackage_name_list'),
    path('adpackages_list', PackageList.as_view(), name='adpackages_list'),
    path('adpackage_order_list', PackageOrderList.as_view(), name='adpackage_order_list'),

    path('adPackageCategoryHistory/<int:package_category_id>/', PackageCategoryHistoryView.as_view(), name='adPackageCategoryHistory'),
    path('adPackageNameHistory/<int:package_name_id>/', PackageNameHistoryView.as_view(), name='adPackageNameHistory'),
    path('adPackagesHistory/<int:package_id>/', PackagesHistoryView.as_view(), name='adPackagesHistory'),
    path('adpackage_order_history/<int:order_id>/', PackageOrderHistoryView.as_view(), name='adpackage_order_history'),

    path('adupdate_ride_status/<int:ride_id>/',update_ride_status, name='adupdate_ride_status'),
    path('adview_assignlater', AssignLaterList.as_view(), name='adview_assignlater'),

    path('send_otp_adminuser/', SendOtp.as_view(), name='send_otp_adminuser'),
    path('verify_otp_adminuser/', VerifyOtp.as_view(), name='verify_otp_adminuser'),
    path('AdminPricingDetails', customerGetRidePricingDetails.as_view(), name='AdminPricingDetails'),
    path('adcancel_ride', cancel_ride, name='adcancel_ride'),
    path('adassign_driver', assign_driver, name='adassign_driver'),
    path('adadvanceassign_driver', advanceassign_driver, name='adadvanceassign_driver'),




]