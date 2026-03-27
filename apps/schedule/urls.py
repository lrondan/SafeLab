from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('', views.schedule, name='main'),
    path('<int:session_id>/export-excel/', views.export_practicals_to_excel, name='export')
]