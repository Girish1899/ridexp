from django.urls import path
from author.views import *

urlpatterns = [

    path('authorindex',index,name='authorindex'),
    path('author-profile', author_profile_view, name='author-profile'),
    path('author-package-category', addpackagecategory.as_view(), name='author-package-category'),
    path('check-package-category/', check_package_category, name='check-package-category'),
    path('author-package-category-list', PackageCategoryList.as_view(), name='author-package-category-list'),
    path('author-DeletePackageCategory', DeletePackageCategory.as_view(), name='author-DeletePackageCategory'),
    path('author-EditPackageCategory/<int:id>/', EditPackageCategory.as_view(), name='author-EditPackageCategory'),
    path('author-PackageCategoryHistory/<int:package_category_id>/', PackageCategoryHistoryView.as_view(), name='author-PackageCategoryHistory'),
    path('author-UpdatePackageCategory', UpdatePackageCategory.as_view(), name='author-UpdatePackageCategory'),

    path('check-blogtitle/', check_blogtitle, name='check-blogtitle'),
    path('create-author-packages', addwebpackages.as_view(), name='create-author-packages'),
    path('list-author-packages', webPackageList.as_view(), name='list-author-packages'),
    path('author-Packages-delete', DeletewebPackages.as_view(), name='author-Packages-delete'),
    path('author-Packages-edit/<int:id>/', EditwebPackages.as_view(), name='author-Packages-edit'),
    path('author-Packages-update', UpdatewebPackages.as_view(), name='author-Packages-update'),

    path('create-author-blogs', AddBlogView.as_view(), name='create-author-blogs'),
    path('list-author-blogs', BlogListView.as_view(), name='list-author-blogs'),
    path('author-blogs-delete', webDeleteBlogs.as_view(), name='author-blogs-delete'),
    path('author-blogs-edit/<int:id>/', EditwebBlogs.as_view(), name='author-blogs-edit'),
    path('author-blogs-update', UpdatewebBlogs.as_view(), name='author-blogs-update'),
]