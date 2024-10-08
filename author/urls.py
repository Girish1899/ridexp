from django.urls import path
from author.views import *

urlpatterns = [

    path('authorindex',index,name='authorindex'),
    path('author_profile', author_profile_view, name='author_profile'),
    path('author_package_category', addpackagecategory.as_view(), name='author_package_category'),
    path('check_package_category/', check_package_category, name='check_package_category'),
    path('author_package_category_list', PackageCategoryList.as_view(), name='author_package_category_list'),
    path('author_DeletePackageCategory', DeletePackageCategory.as_view(), name='author_DeletePackageCategory'),
    path('author_EditPackageCategory/<int:id>/', EditPackageCategory.as_view(), name='author_EditPackageCategory'),
    path('author_PackageCategoryHistory/<int:package_category_id>/', PackageCategoryHistoryView.as_view(), name='author_PackageCategoryHistory'),
    path('author_UpdatePackageCategory', UpdatePackageCategory.as_view(), name='author_UpdatePackageCategory'),

    # packages
    path('create_author_packages', addwebpackages.as_view(), name='create_author_packages'),
    path('list_author_packages', webPackageList.as_view(), name='list_author_packages'),
    path('author_Packages_delete', DeletewebPackages.as_view(), name='author_Packages_delete'),
    path('author_Packages_edit/<int:id>/', EditwebPackages.as_view(), name='author_Packages_edit'),
    path('author_Packages_update', UpdatewebPackages.as_view(), name='author_Packages_update'),

    # Blogs
    path('create_author_blogs', AddBlogView.as_view(), name='create_author_blogs'),
    path('list_author_blogs', BlogListView.as_view(), name='list_author_blogs'),
    path('author_blogs_delete', webDeleteBlogs.as_view(), name='author_blogs_delete'),
    path('author_blogs_edit/<int:id>/', EditwebBlogs.as_view(), name='author_blogs_edit'),
    path('author_blogs_update', UpdatewebBlogs.as_view(), name='author_blogs_update'),
]