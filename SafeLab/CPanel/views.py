from django.shortcuts import render, HttpResponse, redirect
from .models import Aparatu, ChemSub, glaswerk, Other, safety
from .form import UploadFileForm
import datetime

# Create your views here.
def cpanel(request):
    return render(request, 'cpanel.html')

def safelab_aparatu(request):
    datas = Aparatu.objects.all()
    return render(request, 'safelab.html', {'datas': datas})

def chem(request):
    datas = ChemSub.objects.all()
    return render(request, 'chem.html', {'datas': datas})

def glasses(request):
    datas = glaswerk.objects.all()
    return render(request, 'glaswerk.html', {'datas': datas})

def safetys(request):
    datas = safety.objects.all()
    return render(request, 'safety.html', {'datas': datas})

def other(request):
    datas = Other.objects.all()
    return render(request, 'others.html', {'datas': datas})


def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return HttpResponse("El archivo no es un CSV")

            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines:
                fields = line.split(",")
                if len(fields) == 5:  # Asegúrate de que la línea tenga 3 campos
                    Aparatu.objects.create(
                        id=fields[0],
                        name=fields[1],
                        mark=fields[2],
                        range=fields[3],
                        cant=fields[4],
                        Obsevation=fields[5],
                        #date=datetime.datetime.strptime(fields[6], '%Y-%m-%d').date()
                    )
            return redirect('cpanel')  # Redirige a una URL de éxito
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})