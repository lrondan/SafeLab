from urllib import request
from django.contrib.auth import logout
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    profile = None
    if hasattr(request, 'user') and request.user.is_authenticated:
        profile = request.user.profile

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Session closed successfully.")
        return HttpResponseRedirect('/')


    