from django.shortcuts import render, redirect
from . form import RegisterForm
from django.contrib import messages
from .models import Register_User


# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = Register_User.objects.filter(email=email, password=password)
        if user:
            return redirect('cpanel')
        else:
            messages.error(request, 'email or password is incorrect')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        messages.success(request, 'Account created successfully')
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, 'logout.html')