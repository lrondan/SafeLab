"""
URL configuration for SafeLab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from LLR.views import login, register, logout
from CPanel.views import safelab_aparatu, other, cpanel, upload_csv, chem, glasses, safetys

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('cpanel/', cpanel, name='cpanel'),
    path('devices/', safelab_aparatu, name='devices'),
    path('chem/', chem, name='chem'),
    path('glaswerk/', glasses, name='glaswerk'),
    path('safety/', safetys, name='safety'),
    path('other/', other, name='other'),
    path('upload/', upload_csv, name='upload_csv'),
]
