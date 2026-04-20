"""
URL configuration for SafeLab project.

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
from django.urls import include
from apps.core import views

urlpatterns = [
    path('cpanel/', admin.site.urls, name='cpanel'),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('reports/', include('apps.reports.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('schedule/',include('apps.schedule.urls')),
    path('home/', include('apps.inventory.urls')),
]

handler400 = 'apps.core.views.custom_400_view'
handler403 = 'apps.core.views.custom_403_view'
handler404 = 'apps.core.views.custom_404_view'
handler500 = 'apps.core.views.custom_500_view'
