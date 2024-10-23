"""taxipro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf.urls.static import static
from rescue import views
from taxipro import settings
from django.views.generic import TemplateView
from taxipro.views import *
from superadmin import views

urlpatterns = [
    path('', include('website.urls')),


    path('forgot_password', views.forgot_password.as_view(), name='forgot_password'),
    path('forgot-password.html', views.forgot_password.as_view(), name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('robots.txt', views.robots.as_view(), name='robots'),
    path('sitemap.xml', views.sitemap.as_view(), name='sitemap'),

    path('admin/', admin.site.urls),
    path('superadmin/', include('superadmin.urls')),
    path('adminuser/', include('adminuser.urls')),
    path('rescue/', include('rescue.urls')),
    path('customer/', include('customer.urls')),
    path('quality/', include('quality.urls')),
    path('telecaller/', include('telecaller.urls')),
    path('distributer/', include('distributer.urls')),
    path('addride', views.AddRidee.as_view(), name='addride'),
    path('driver/', include('driver.urls')),
    path('hr/', include('hr.urls')),
    path('author/', include('author.urls')),
    
    path('get_customer_details/',get_customer_details,name='get_customer_details'),

    path('check_dphonenumber', check_dphonenumber, name='check_dphonenumber'),
    path('global_fetch_vehicle_details/', global_fetch_vehicle_details, name='global_fetch_vehicle_details'),
  
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
