from django.urls import path
from distributer.views import *

urlpatterns = [

    path('',index,name='indexd'),
    # driverss#######################
    # Brand #####################
    path('dispatch-addbrand',addbrand.as_view(),name='dispatch-addbrand'),
    # path('check-brand/', check_brand, name='check_brand'),
    path('dispatch-BrandListView',BrandListView.as_view(),name='dispatch-BrandListView'),
    path('dispatch-DeleteBrand',DeleteBrand.as_view(),name='dispatch-DeleteBrand'),  
    path('dispatch-EditBrand/<int:id>/',EditBrand.as_view(),name="dispatch-EditBrand"),
    path('dispatch-BrandHistory/<int:brand_id>/', BrandHistoryView.as_view(), name='dispatch-brand_history'),
    path('dispatch-UpdateBrand',UpdateBrand.as_view(),name="dispatch-UpdateBrand"),

    path('dispatch-toggle_brand_status/', toggle_brand_status, name='dispatch-toggle_brand_status'),
    path('dispatch-brand/<int:brand_id>/view/', ViewBrand.as_view(), name='dispatch-ViewBrand'),

    # category##################
    path('dispatch-addcategory',addcategory.as_view(),name='dispatch-addcategory'),
    path('dispatch-check-category/', check_category, name='dispatch-check_category'),
    path('dispatch-CategoryListView',CategoryListView.as_view(),name='dispatch-CategoryListView'),
    path('dispatch-DeleteCategory',DeleteCategory.as_view(),name='dispatch-DeleteCategory'),  
    path('dispatch-EditCategory/<int:id>/',EditCategory.as_view(),name="dispatch-EditCategory"),
    path('dispatch-CategoryHistory/<int:category_id>/', CategoryHistoryView.as_view(), name='dispatch-category_history'),
    path('dispatch-UpdateCategory',UpdateCategory.as_view(),name="dispatch-UpdateCategory"),

    path('dispatch-toggle-category-status/', toggle_category_status, name='dispatch-toggle_category_status'),
    path('dispatch-category/<int:category_id>/view/', ViewCategory.as_view(), name='dispatch-ViewCategory'),



    # Model ############################
    path('dispatch-addmodel',addmodel.as_view(),name='dispatch-addmodel'),
    path('dispatch-ModelListView',ModelListView.as_view(),name='dispatch-ModelListView'),
    path('dispatch-DeleteModel',DeleteModel.as_view(),name='dispatch-DeleteModel'),  
    path('dispatch-EditModel/<int:id>/',EditModel.as_view(),name="dispatch-EditModel"),
    path('dispatch-ModelHistory/<int:model_id>/', ModelHistoryView.as_view(), name='dispatch-model_history'),
    path('dispatch-UpdateModel',UpdateModel.as_view(),name="dispatch-UpdateModel"),

    path('dispatch-toggle_model_status/', toggle_model_status, name='dispatch-toggle_model_status'),
    path('dispatch-model/<int:model_id>/view/', ViewModel.as_view(), name='dispatch-ViewModel'),



    #vehicletype################  
    path('dispatch-addvehicletype', addvehicletype.as_view(), name='dispatch-addvehicletype'),
    path('dispatch-check_vehicletype/', check_vehicletype, name='dispatch-check_vehicletype'),
    path('dispatch-vehicletypeList', vehicletypeList.as_view(), name='dispatch-vehicletypeList'),
    path('dispatch-Deletevehicletype', Deletevehicletype.as_view(), name='dispatch-Deletevehicletype'),
    path('dispatch-Editvehicletype/<int:id>/', Editvehicletype.as_view(), name='dispatch-Editvehicletype'),
    path('dispatch-VtypeHistory/<int:vehicle_type_id>/', VehicleTypeHistoryView.as_view(), name='dispatch-Vtype_history'),
    path('dispatch-Updatevehicletype', Updatevehicletype.as_view(), name='dispatch-Updatevehicletype'),
    path('dispatch-vehicletype/<int:vehicle_type_id>/view/', ViewVehicletype.as_view(), name='dispatch-vehicletype'),


    #ridetype################  
    path('dispatch-addridetype', addridetype.as_view(), name='dispatch-addridetype'),
    path('dispatch-check_ridetype/', check_ridetype, name='dispatch-check_ridetype'),
    path('dispatch-ridetypeList', ridetypeList.as_view(), name='dispatch-ridetypeList'),
    path('dispatch-Deleteridetype', Deleteridetype.as_view(), name='dispatch-Deleteridetype'),
    path('dispatch-Editridetype/<int:id>/', Editridetype.as_view(), name='dispatch-Editridetype'),
    path('dispatch-RtypeHistory/<int:ridetype_id>/', RidetypeHistoryView.as_view(), name='dispatch-Rtype_history'),
    path('dispatch-Updateridetype', Updateridetype.as_view(), name='dispatch-Updateridetype'),

    path('dispatch-ridetype/<int:ridetype_id>/view/', ViewRidetype.as_view(), name='dispatch-ridetype'),

    # Transmission##################
    path('dispatch-addtransmission',addtransmission.as_view(),name='dispatch-addtransmission'),
    path('dispatch-check-transmission/', check_transmission, name='dispatch-check_transmission'),
    path('dispatch-TransmissionListView',TransmissionListView.as_view(),name='dispatch-TransmissionListView'),
    path('dispatch-DeleteTransmission',DeleteTransmission.as_view(),name='dispatch-DeleteTransmission'),  
    path('dispatch-EditTransmission/<int:id>/',EditTransmission.as_view(),name="dispatch-EditTransmission"),
    path('dispatch-TransmissionHistory/<int:transmission_id>/', TransmissionHistoryView.as_view(), name='dispatch-transmission_history'),
    path('dispatch-UpdateTransmission',UpdateTransmission.as_view(),name="dispatch-UpdateTransmission"),
    path('dispatch-transmission/<int:transmission_id>/view/', ViewTransmission.as_view(), name='dispatch-transmission'),


    #color################  
    path('dispatch-addcolor', addcolor.as_view(), name='dispatch-addcolor'),
    path('dispatch-check_color/', check_color, name='dispatch-check_color'),
    path('dispatch-colorList', colorList.as_view(), name='dispatch-colorList'),
    path('dispatch-Deletecolor', Deletecolor.as_view(), name='dispatch-Deletecolor'),
    path('dispatch-Editcolor/<int:id>/', Editcolor.as_view(), name='dispatch-Editcolor'),
    path('dispatch-ColorHistory/<int:color_id>/', ColorHistoryView.as_view(), name='dispatch-ColorHistory'),
    path('dispatch-Updatecolor', Updatecolor.as_view(), name='dispatch-Updatecolor'),
    path('dispatch-color/<int:color_id>/view/', ViewColor.as_view(), name='dispatch-color'),

    # customer 
    path('dispatch-addcustomer', addcustomer.as_view(), name='dispatch-addcustomer'),
    path('dispatch-check_phonenumber', check_phonenumber, name='dispatch-check_phonenumber'),
    path('dispatch-customerlist', CustomerList.as_view(), name='dispatch-customerlist'),
    path('dispatch-DeleteCustomer', DeleteCustomer.as_view(), name='dispatch-DeleteCustomer'),
    path('dispatch-EditCustomer/<int:id>/', EditCustomer.as_view(), name='dispatch-EditCustomer'),
    path('dispatch-CustomerHistory/<int:customer_id>/', CustomerHistoryView.as_view(), name='dispatch-Customer_history'),
    path('dispatch-UpdateCustomer', UpdateCustomer.as_view(), name='dispatch-UpdateCustomer'),    
    path('dispatch-customer/<int:customer_id>/view/', ViewCustomer.as_view(), name='dispatch-customer'),
    path('dispatch-customer_profile/<int:customer_id>/', CustomerProfileHistoryView.as_view(), name='dispatch-customer_profile'),
    path('dispatch-cust_profile_list', CustomerProfileList.as_view(), name='dispatch-cust_profile_list'),


    # vehicle owner##############################
    path('dispatch-addvehicleowner', AddOwnerView.as_view(), name='dispatch-addvehicleowner'),
    path('dispatch-check_ownerphonenumber', check_ownerphonenumber, name='dispatch-check_ownerphonenumber'),
    path('dispatch-viewvehicleowner', OwnerListView.as_view(), name='dispatch-viewvehicleowner'),
    path('dispatch-DeleteVehicleowner', DeleteOwnerView.as_view(), name='dispatch-DeleteVehicleowner'),
    path('dispatch-EditVehicleowner/<int:id>/', EditOwnerView.as_view(), name='dispatch-EditVehicleowner'),
    path('dispatch-VehicleownerHistory/<int:owner_id>/', VehicleOwnerHistoryView.as_view(), name='dispatch-Vehicleowner_history'),
    path('dispatch-updatevehicleowner', UpdateOwnerView.as_view(), name='dispatch-updatevehicleowner'),
    path('dispatch-owner/<int:owner_id>/view/', ViewOwner.as_view(), name='dispatch-owner'),

    path('dispatch-download-owner-documents/<int:owner_id>/',download_owner_documents, name='dispatch-download_owner_documents'),
    path('dispatch-ownerverification', OwnerVerification.as_view(), name='dispatch-ownerverification'),
    path('dispatch-VerifyOwner/', verify_owner, name='dispatch-VerifyOwner'),
    path('dispatch-toggle-owner-status/', toggle_owner_status, name='dispatch-toggle_owner_status'),
    
    
# driver
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


    #  enquiry ################################
    path('dispatch-enquirylist', EnquiryList.as_view(), name='dispatch-enquirylist'),   

    # author

    # package category
    path('dispatch-author-package-category', addpackagecategory.as_view(), name='dispatch-author-package-category'),
    path('dispatch-check-package-category/', check_package_category, name='dispatch-check-package-category'),
    path('dispatch-author-package-category-list', PackageCategoryList.as_view(), name='dispatch-author-package-category-list'),
    path('dispatch-author-DeletePackageCategory', DeletePackageCategory.as_view(), name='dispatch-author-DeletePackageCategory'),
    path('dispatch-author-EditPackageCategory/<int:id>/', EditPackageCategory.as_view(), name='dispatch-author-EditPackageCategory'),
    path('dispatch-author-PackageCategoryHistory/<int:package_category_id>/', PackageCategoryHistoryView.as_view(), name='dispatch-author-PackageCategoryHistory'),
    path('dispatch-author-UpdatePackageCategory', UpdatePackageCategory.as_view(), name='dispatch-author-UpdatePackageCategory'),

    # packages
    path('dispatch-create-author-packages', addwebpackages.as_view(), name='dispatch-create-author-packages'),
    path('dispatch-list-author-packages', webPackageList.as_view(), name='dispatch-list-author-packages'),
    path('dispatch-author-Packages-delete', DeletewebPackages.as_view(), name='dispatch-author-Packages-delete'),
    path('dispatch-author-Packages-edit/<int:id>/', EditwebPackages.as_view(), name='dispatch-author-Packages-edit'),
    path('dispatch-author-Packages-update', UpdatewebPackages.as_view(), name='dispatch-author-Packages-update'),

    # Blogs
    path('dispatch-create-author-blogs', AddBlogView.as_view(), name='dispatch-create-author-blogs'),
    path('dispatch-list-author-blogs', BlogListView.as_view(), name='dispatch-list-author-blogs'),
    path('dispatch-author-blogs-delete', webDeleteBlogs.as_view(), name='dispatch-author-blogs-delete'),
    path('dispatch-author-blogs-edit/<int:id>/', EditwebBlogs.as_view(), name='dispatch-author-blogs-edit'),
    path('dispatch-author-blogs-update', UpdatewebBlogs.as_view(), name='dispatch-author-blogs-update'),
    

]