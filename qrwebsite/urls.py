"""qrcode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls ,name='admin'),
    path('accounts/', include('allauth.urls')),
    
    path('', include('scan.urls', namespace='scan')),
    path('events/', include('events.urls', namespace='events')),
    path('users/', include('invitee.urls', namespace='invitee')),
    
    
    path('schema/', get_schema_view(
        title="API",
        description="API for the qr App",
        version="1.0.0"
    ), name="qr-schema"),
    path('api/', include_docs_urls(
        title="API",
        description="API for the qr App",
    ), name="qr-docs"),
    path('api/accounts/', include('dj_rest_auth.urls')),
    path('api/event/', include('events.api.urls', namespace='events-api')),
    path('api/invitee/', include('invitee.api.urls', namespace='invitee-api')),
    # path('api/fest', include('fest.api.urls', namespace='fest-api')),
    path('api/scan/', include('scan.api.urls', namespace='scan-api')),
    
    
]
