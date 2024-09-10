from django.urls import path
from superadmin.views import *
from taxipro.views import global_fetch_customer_details

urlpatterns = [

    path('index',index,name='index'),

    # path('report', report, name='report'),
      
    # Brand #####################
    path('addbrand',addbrand.as_view(),name='addbrand'),
    # path('check-brand/', check_brand, name='check_brand'),
    path('BrandListView',BrandListView.as_view(),name='BrandListView'),
    path('DeleteBrand',DeleteBrand.as_view(),name='DeleteBrand'),  
    path('EditBrand/<int:id>/',EditBrand.as_view(),name="EditBrand"),
    path('BrandHistory/<int:brand_id>/', BrandHistoryView.as_view(), name='brand_history'),
    path('UpdateBrand',UpdateBrand.as_view(),name="UpdateBrand"),

    path('toggle_brand_status/', toggle_brand_status, name='toggle_brand_status'),
    path('brand/<int:brand_id>/view/', ViewBrand.as_view(), name='ViewBrand'),

    # category##################
    path('addcategory',addcategory.as_view(),name='addcategory'),
    path('check-category/', check_category, name='check_category'),
    path('CategoryListView',CategoryListView.as_view(),name='CategoryListView'),
    path('DeleteCategory',DeleteCategory.as_view(),name='DeleteCategory'),  
    path('EditCategory/<int:id>/',EditCategory.as_view(),name="EditCategory"),
    path('CategoryHistory/<int:category_id>/', CategoryHistoryView.as_view(), name='category_history'),
    path('UpdateCategory',UpdateCategory.as_view(),name="UpdateCategory"),

    path('toggle-category-status/', toggle_category_status, name='toggle_category_status'),
    path('category/<int:category_id>/view/', ViewCategory.as_view(), name='ViewCategory'),



    # Model ############################
    path('addmodel',addmodel.as_view(),name='addmodel'),
    path('ModelListView',ModelListView.as_view(),name='ModelListView'),
    path('DeleteModel',DeleteModel.as_view(),name='DeleteModel'),  
    path('EditModel/<int:id>/',EditModel.as_view(),name="EditModel"),
    path('ModelHistory/<int:model_id>/', ModelHistoryView.as_view(), name='model_history'),
    path('UpdateModel',UpdateModel.as_view(),name="UpdateModel"),

    path('toggle_model_status/', toggle_model_status, name='toggle_model_status'),
    path('model/<int:model_id>/view/', ViewModel.as_view(), name='ViewModel'),



    #vehicletype################  
    path('addvehicletype', addvehicletype.as_view(), name='addvehicletype'),
    path('check_vehicletype/', check_vehicletype, name='check_vehicletype'),
    path('vehicletypeList', vehicletypeList.as_view(), name='vehicletypeList'),
    path('Deletevehicletype', Deletevehicletype.as_view(), name='Deletevehicletype'),
    path('Editvehicletype/<int:id>/', Editvehicletype.as_view(), name='Editvehicletype'),
    path('VtypeHistory/<int:vehicle_type_id>/', VehicleTypeHistoryView.as_view(), name='Vtype_history'),
    path('Updatevehicletype', Updatevehicletype.as_view(), name='Updatevehicletype'),
    path('vehicletype/<int:vehicle_type_id>/view/', ViewVehicletype.as_view(), name='vehicletype'),


    #ridetype################  
    path('addridetype', addridetype.as_view(), name='addridetype'),
    path('check_ridetype/', check_ridetype, name='check_ridetype'),
    path('ridetypeList', ridetypeList.as_view(), name='ridetypeList'),
    path('Deleteridetype', Deleteridetype.as_view(), name='Deleteridetype'),
    path('Editridetype/<int:id>/', Editridetype.as_view(), name='Editridetype'),
    path('RtypeHistory/<int:ridetype_id>/', RidetypeHistoryView.as_view(), name='Rtype_history'),
    path('Updateridetype', Updateridetype.as_view(), name='Updateridetype'),

    path('ridetype/<int:ridetype_id>/view/', ViewRidetype.as_view(), name='ridetype'),


    # User 
    path('check_phno',check_phno,name='check_phno'),
    path('check_useremail',check_useremail,name='check_useremail'),
    path('adduser', adduser.as_view(), name='adduser'),
    path('userlist', UserList.as_view(), name='userlist'),
    path('DeleteUser', DeleteUser.as_view(), name='DeleteUser'),
    path('EditUser/<int:id>/', EditUser.as_view(), name='EditUser'),
    path('UserHistory/<int:profile_id>/', ProfileHistoryView.as_view(), name='User_history'),
    path('UpdateUser', UpdateUser.as_view(), name='UpdateUser'),
    #profile
    path('profile', profile.as_view(), name='profile'),
    path('update-user/', UpdateUserView.as_view(), name='update_user'),

    # customer 
    path('addcustomer', addcustomer.as_view(), name='addcustomer'),
    path('check_phonenumber', check_phonenumber, name='check_phonenumber'),
    path('customerlist', CustomerList.as_view(), name='customerlist'),
    path('DeleteCustomer', DeleteCustomer.as_view(), name='DeleteCustomer'),
    path('EditCustomer/<int:id>/', EditCustomer.as_view(), name='EditCustomer'),
    path('CustomerHistory/<int:customer_id>/', CustomerHistoryView.as_view(), name='Customer_history'),
    path('UpdateCustomer', UpdateCustomer.as_view(), name='UpdateCustomer'),    
    path('customer/<int:customer_id>/view/', ViewCustomer.as_view(), name='customer'),
    path('customer_profile/<int:customer_id>/', CustomerProfileHistoryView.as_view(), name='customer_profile'),
    path('cust_profile_list', CustomerProfileList.as_view(), name='cust_profile_list'),

    # vehicle owner##############################
    path('addvehicleowner', AddOwnerView.as_view(), name='addvehicleowner'),
    path('check_ownerphonenumber', check_ownerphonenumber, name='check_ownerphonenumber'),
    path('viewvehicleowner', OwnerListView.as_view(), name='viewvehicleowner'),
    path('DeleteVehicleowner', DeleteOwnerView.as_view(), name='DeleteVehicleowner'),
    path('EditVehicleowner/<int:id>/', EditOwnerView.as_view(), name='EditVehicleowner'),
    path('VehicleownerHistory/<int:owner_id>/', VehicleOwnerHistoryView.as_view(), name='Vehicleowner_history'),
    path('updatevehicleowner', UpdateOwnerView.as_view(), name='updatevehicleowner'),
    path('owner/<int:owner_id>/view/', ViewOwner.as_view(), name='owner'),

    path('download-owner-documents/<int:owner_id>/',download_owner_documents, name='download_owner_documents'),
    path('ownerverification', OwnerVerification.as_view(), name='ownerverification'),
    path('VerifyOwner/', verify_owner, name='VerifyOwner'),
    path('toggle-owner-status/', toggle_owner_status, name='toggle_owner_status'),
    
    

    # driverss#######################
    path('adddriver', AddDriverView.as_view(), name='adddriver'),
    path('check_dphonenumber', check_dphonenumber, name='check_dphonenumber'),
    path('viewdriver', DriverListView.as_view(), name='viewdriver'),
    path('viewdriververification', DriverVerificationView.as_view(), name='viewdriververification'),
    path('DeleteDriver', DeleteDriverView.as_view(), name='DeleteDriver'),
    path('EditDriver/<int:id>/', EditDriverView.as_view(), name='EditDriver'),
    path('DriverHistory/<int:driver_id>/', DriverHistoryView.as_view(), name='driver_history'),
    path('updatedriver', UpdateDriverView.as_view(), name='updatedriver'),
    path('toggle_driver_status/', toggle_driver_status, name='toggle_driver_status'),

    path('fetch_vehicle_details/', fetch_vehicle_details, name='fetch_vehicle_details'),
    path('driver/<int:driver_id>/view/', ViewDriver.as_view(), name='driver'),
    path('download-driver-documents/<int:driver_id>/',download_driver_documents, name='download_driver_documents'),
    path('VerifyDriver/', verify_driver, name='VerifyDriver'),

    path('driver_report', DriverReport.as_view(), name='driver_report'),





    # vehicle ##############################
    path('addvehicle', AddVehicle.as_view(), name='addvehicle'),
    path('check_vehicleno/',check_vehicleno,name='check_vehicleno'),
    path('vehiclelist', VehicleList.as_view(), name='vehiclelist'),
    path('vehicleblocklist', VehicleBlockList.as_view(), name='vehicleblocklist'),
    path('DeleteVehicle', DeleteVehicle.as_view(), name='DeleteVehicle'),
    path('EditVehicle/<int:id>/', EditVehicle.as_view(), name='EditVehicle'),
    path('VehicleHistory/<int:vehicle_id>/', VehicleHistoryView.as_view(), name='Vehicle_history'),
    path('UpdateVehicle', UpdateVehicle.as_view(), name='UpdateVehicle'),

    path('download-vehicle-documents/<int:vehicle_id>/',download_vehicle_documents, name='download_vehicle_documents'),
    path('vehicle/<int:vehicle_id>/view/', ViewVehicle.as_view(), name='vehicle'),
    path('VerifyVehicle/', verify_vehicle, name='VerifyVehicle'),
    path('vehicleupdate_status/',vehicleupdate_status,name='vehicleupdate_status'),



    # ride details ###########################

    path('fetch_customer_details/', fetch_customer_details, name='fetch_customer_details'),
    path('ridelist', RideList.as_view(), name='ridelist'),
    path('DeleteRide', DeleteRide.as_view(), name='DeleteRide'),
    path('EditRide/<int:id>/', EditRide.as_view(), name='EditRide'),
    path('UpdateRide', UpdateRide.as_view(), name='UpdateRide'),
    # path('completed_rides',completed_rides,name='completed_rides'),

# bookings####################################################################
    path('addbooking', AddRide.as_view(), name='addbooking'),
    path('ridelist/<int:ride_id>/', RideList.as_view(), name='ridelist'),
    path('assign_driver', assign_driver, name='assign_driver'),
    path('advanceassign_driver', advanceassign_driver, name='advanceassign_driver'),
    # path('RideHistory/<int:ride_id>/', RideDetailsHistoryView.as_view(), name='RideHistory'),
    path('advance_bookings', AdvanceBookingsList.as_view(), name='advance_bookings'),
    path('pending_bookings', PendingBookingsList.as_view(), name='pending_bookings'),
    path('view_assigned_rides', AssignedRideList.as_view(), name='view_assigned_rides'),
    path('view_assignlater', AssignLaterList.as_view(), name='view_assignlater'),
    path('ongoing_rides', OngoingRideList.as_view(), name='ongoing_rides'),
    path('completed_rides', CompletedRideList.as_view(), name='completed_rides'),
    path('cancelledbookings',CancelledListView.as_view(),name='cancelledbookings'),
    path('cancel_ride', cancel_ride, name='cancel_ride'),
    path('global_customerGetRidePricingDetails', customerGetRidePricingDetails.as_view(), name='global_customerGetRidePricingDetails'),


    path('current-bookings', AssignDriverView.as_view(), name='current_bookings'),
    path('invoice/<int:ride_id>/', InvoiceView.as_view(), name='invoice_view'),

################## price details ###########################
    path('addpricing', addprice.as_view(), name='addpricing'),
    path('pricinglist', PriceList.as_view(), name='pricinglist'),
    path('DeletePrice', DeletePrice.as_view(), name='DeletePrice'),
    path('EditPrice/<int:id>/', EditPrice.as_view(), name='EditPrice'),
    path('UpdatePricing', UpdatePricing.as_view(), name='UpdatePricing'),
    path('pricing_history/<int:pricing_id>/', PricingHistoryView.as_view(), name='pricing_history'),

# fetch customer
    path('global_fetch_customer_details/', global_fetch_customer_details, name='global_fetch_customer_details'),
    path('update-status/', update_status, name='update_status'),

    # commission #############################
    path('addcommission', addcommission.as_view(), name='addcommission'),
    path('commissionlist', CommissionList.as_view(), name='commissionlist'),
    path('DeleteCommission', DeleteCommission.as_view(), name='DeleteCommission'),
    path('editcommission/<int:id>/', EditCommission.as_view(), name='editcommission'),
    path('updatecommission', UpdateCommission.as_view(), name='updatecommission'),
    path('commission_history/<int:commission_id>/', CommissionHistoryView.as_view(), name='commission_history'),

# accounts #######################3
    path('add_accounts', AddAccountsView.as_view(), name='add_accounts'),
    path('accounts_list', AccountsListView.as_view(), name='accounts_list'),
    path('DeleteAccounts', DeleteAccounts.as_view(), name='DeleteAccounts'),
    path('EditAccounts/<int:id>/', EditAccounts.as_view(), name='EditAccounts'),
    path('UpdateAccounts', UpdateAccounts.as_view(), name='UpdateAccounts'),


    # Transmission##################
    path('addtransmission',addtransmission.as_view(),name='addtransmission'),
    path('check-transmission/', check_transmission, name='check_transmission'),
    path('TransmissionListView',TransmissionListView.as_view(),name='TransmissionListView'),
    path('DeleteTransmission',DeleteTransmission.as_view(),name='DeleteTransmission'),  
    path('EditTransmission/<int:id>/',EditTransmission.as_view(),name="EditTransmission"),
    path('TransmissionHistory/<int:transmission_id>/', TransmissionHistoryView.as_view(), name='transmission_history'),
    path('UpdateTransmission',UpdateTransmission.as_view(),name="UpdateTransmission"),
    path('transmission/<int:transmission_id>/view/', ViewTransmission.as_view(), name='transmission'),


    #color################  
    path('addcolor', addcolor.as_view(), name='addcolor'),
    path('check_color/', check_color, name='check_color'),
    path('colorList', colorList.as_view(), name='colorList'),
    path('Deletecolor', Deletecolor.as_view(), name='Deletecolor'),
    path('Editcolor/<int:id>/', Editcolor.as_view(), name='Editcolor'),
    path('ColorHistory/<int:color_id>/', ColorHistoryView.as_view(), name='ColorHistory'),
    path('Updatecolor', Updatecolor.as_view(), name='Updatecolor'),
    path('color/<int:color_id>/view/', ViewColor.as_view(), name='color'),


    #local package###################
    path('add_localpackage',addlocalpackage.as_view(),name='add_localpackage'),
    path('delete_localpackage',DeleteLocalPackage.as_view(),name='delete_localpackage'),
    path('view_localpackage',LocalPackageListView.as_view(),name='view_localpackage'),
    path('updatelocalpackage',UpdateLocalPackage.as_view(),name="updatelocalpackage"),
    path('editlocalpackage/<int:id>/',EditLocalPackage.as_view(),name="editlocalpackage"),

    #localprice
    path('add_localprice', AddLocalPrice.as_view(), name='add_localprice'),
    path('delete_localprice', DeleteLocalPrice.as_view(), name='delete_localprice'),
    path('view_localprice', LocalPriceList.as_view(), name='view_localprice'),
    path('updatelocalprice',UpdateLocalPrice.as_view(),name="updatelocalprice"),
    path('editlocalprice/<int:id>/',EditLocalPrice.as_view(),name="editlocalprice"),


    #airport
    path('add_airportpricing', AddAirportPricingView.as_view(), name='add_airportpricing'),
    path('delete_airportprice',DeleteAirportPrice.as_view(),name="delete_airportprice"),
    path('view_airportprice', AirportPriceList.as_view(), name='view_airportprice'),
    path('updateairportprice',UpdateAirportPackage.as_view(),name="updateairportprice"),
    path('editairportprice/<int:id>/',EditAirportPackage.as_view(),name="editairportprice"),

    #outstation
    path('add_outstationprice', AddOutstationView.as_view(), name='add_outstationprice'),
    path('delete_outstationprice',DeletestationPrice.as_view(),name="delete_outstationprice"),
    path('view_outstationprice', OutstationPriceList.as_view(), name='view_outstationprice'),
    path('updateoutstationprice',UpdateOutstationPrice.as_view(),name="updateoutstationprice"),
    path('editoutstationprice/<int:id>/',EditOutstationPrice.as_view(),name="editoutstationprice"),

    # Commission details ##################################

    path('CommVehicleListView',CommVehicleListView.as_view(),name="CommVehicleListView"),
    path('vehicle/<int:vehicle_id>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    
    path('vehicles/', VehicleListView.as_view(), name='vehicles'),
    path('vehicles/<str:vehicle_id>/daily-summary/', VehicleDailySummaryView.as_view(), name='vehicle_daily_summary'),
    path('vehicle/<int:vehicle_id>/details/<str:date>/', BookingDetailsView.as_view(), name='booking_details'),


]

