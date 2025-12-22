"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from core.views import home_view
from core import views

from django.conf import settings 
from django.conf.urls.static import static 




urlpatterns = [
    path('admin/', admin.site.urls),
# Main views referenced in the template
    path('homepage/', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
# Dynamic Policy Pages: URLs match the slugs in the footer
    path('refund-policy/', views.refund_policy_view , name='refund_policy'),
    path('terms-conditions/', views.terms_conditions_view, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)