from django.urls import path
from telecaller.views import *


urlpatterns = [
    path('',index,name='indextel'),
    
    path('telecalleraddcustomer', addcustomer.as_view(), name='telecalleraddcustomer'),
    path('telecallercustomerlist', CustomerList.as_view(), name='telecallercustomerlist'),
    path('telecallerEditCustomer/<int:id>/', EditCustomer.as_view(), name='telecallerEditCustomer'),
    path('telecallerUpdateCustomer', UpdateCustomer.as_view(), name='telecallerUpdateCustomer'),  
    path('tele_check_phonenumber', check_phonenumber, name='tele_check_phonenumber'),

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


    path('tele_profile', profile.as_view(), name='tele_profile'),
    path('telecaller-profile', telecaller_profile_view, name='telecaller-profile'),
    path('update-user/', UpdateUserView.as_view(), name='tele_update_user'),
    path('callhistory/<int:ride_id>/', call_history_view, name='callhistory'),

    path('televiewdriver', DriverListView.as_view(), name='televiewdriver'),

    path('tele-enquirylist', EnquiryList.as_view(), name='tele-enquirylist'),   


    path('tele-author-package-category', addpackagecategory.as_view(), name='tele-author-package-category'),
    path('tele-check-package-category/', check_package_category, name='tele-check-package-category'),
    path('tele-author-package-category-list', PackageCategoryList.as_view(), name='tele-author-package-category-list'),
    path('tele-author-DeletePackageCategory', DeletePackageCategory.as_view(), name='tele-author-DeletePackageCategory'),
    path('tele-author-EditPackageCategory/<int:id>/', EditPackageCategory.as_view(), name='tele-author-EditPackageCategory'),
    path('tele-author-PackageCategoryHistory/<int:package_category_id>/', PackageCategoryHistoryView.as_view(), name='tele-author-PackageCategoryHistory'),
    path('tele-author-UpdatePackageCategory', UpdatePackageCategory.as_view(), name='tele-author-UpdatePackageCategory'),

    path('tele-create-author-packages', addwebpackages.as_view(), name='tele-create-author-packages'),
    path('tele-list-author-packages', webPackageList.as_view(), name='tele-list-author-packages'),
    path('tele-author-Packages-delete', DeletewebPackages.as_view(), name='tele-author-Packages-delete'),
    path('tele-author-Packages-edit/<int:id>/', EditwebPackages.as_view(), name='tele-author-Packages-edit'),
    path('tele-author-Packages-update', UpdatewebPackages.as_view(), name='tele-author-Packages-update'),

    path('tele-create-author-blogs', AddBlogView.as_view(), name='tele-create-author-blogs'),
    path('tele-list-author-blogs', BlogListView.as_view(), name='tele-list-author-blogs'),
    path('tele-author-blogs-delete', webDeleteBlogs.as_view(), name='tele-author-blogs-delete'),
    path('tele-author-blogs-edit/<int:id>/', EditwebBlogs.as_view(), name='tele-author-blogs-edit'),
    path('tele-author-blogs-update', UpdatewebBlogs.as_view(), name='tele-author-blogs-update'),

]