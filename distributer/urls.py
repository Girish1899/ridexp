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