from django.shortcuts import render, redirect
from . form import RegisterForm
from django.contrib import messages


# Create your views here.
def login(request):
    
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