"""
URL configuration for umico_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers
from umico_app.views import (
    CustomerViewSet, ScanViewSet, PrintViewSet, FrameViewSet, 
    AddressViewSet, GetCSRFToken, signup, index
)

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'scans', ScanViewSet)
router.register(r'prints', PrintViewSet)
router.register(r'frames', FrameViewSet)

#nested routers to add onto customer URL with PK id
customers_router = NestedDefaultRouter(router, r'customers', lookup='customer')
customers_router.register(r'scans', ScanViewSet, basename='customer-scans')
customers_router.register(r'frames', FrameViewSet, basename='customer-frames')
customers_router.register(r'prints', PrintViewSet, basename='customer-prints')

urlpatterns = [
    #Admin page
    path("admin/", admin.site.urls), # Admin page
    path('api-auth/', include('rest_framework.urls')), # API authentication
     # include the built-in auth urls for the built-in views
    path('accounts/', include('django.contrib.auth.urls')), # Built-in auth views
    path('accounts/signup/', signup, name='signup'), # Signup view
    path('csrf/', GetCSRFToken.as_view(), name='csrf-token'), # CSRF token endpoint
    path('', index, name='index'),  # Root URL
    path('', include(router.urls)), # Main API routes
    path('', include(customers_router.urls)), # Nested customer routes
   
]

