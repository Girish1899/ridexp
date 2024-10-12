from django.urls import path
from author.views import *

urlpatterns = [

    path('authorindex',index,name='authorindex'),
    path('author-profile', author-profile-view, name='author-profile'),
    path('author-package-category', addpackagecategory.as-view(), name='author-package-category'),
    path('check-package-category/', check-package-category, name='check-package-category'),
    path('author-package-category-list', PackageCategoryList.as-view(), name='author-package-category-list'),
    path('author-DeletePackageCategory', DeletePackageCategory.as-view(), name='author-DeletePackageCategory'),
    path('author-EditPackageCategory/<int:id>/', EditPackageCategory.as-view(), name='author-EditPackageCategory'),
    path('author-PackageCategoryHistory/<int:package-category-id>/', PackageCategoryHistoryView.as-view(), name='author-PackageCategoryHistory'),
    path('author-UpdatePackageCategory', UpdatePackageCategory.as-view(), name='author-UpdatePackageCategory'),

    # packages
    path('create-author-packages', addwebpackages.as-view(), name='create-author-packages'),
    path('list-author-packages', webPackageList.as-view(), name='list-author-packages'),
    path('author-Packages-delete', DeletewebPackages.as-view(), name='author-Packages-delete'),
    path('author-Packages-edit/<int:id>/', EditwebPackages.as-view(), name='author-Packages-edit'),
    path('author-Packages-update', UpdatewebPackages.as-view(), name='author-Packages-update'),

    # Blogs
    path('create-author-blogs', AddBlogView.as-view(), name='create-author-blogs'),
    path('list-author-blogs', BlogListView.as-view(), name='list-author-blogs'),
    path('author-blogs-delete', webDeleteBlogs.as-view(), name='author-blogs-delete'),
    path('author-blogs-edit/<int:id>/', EditwebBlogs.as-view(), name='author-blogs-edit'),
    path('author-blogs-update', UpdatewebBlogs.as-view(), name='author-blogs-update'),
]