from django.shortcuts import render, redirect
from . form import RegisterForm
from . models import Register_User

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.name = request.user
            form.password = request.password
            form.confirm_password = request.confirm_password
            form.email = request.email
            form.save()
            return redirect('login', pk = form.pk)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def logout(request):
    return render(request, 'logout.html')