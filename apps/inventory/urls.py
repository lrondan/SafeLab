from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campus/<int:campus_id>/', views.campus_detail, name='campus_detail'),
    path('lab/<int:lab_id>/', views.lab_detail, name='lab_detail'),
    path('lab/<int:lab_id>/equipment/new/', views.equipment_create, name='equipment_create'),
    path('lab/<int:lab_id>/reagent/new/', views.reagent_create, name='reagent_create'),
    path('reagent/<int:reagent_id>/edit/', views.reagent_update, name='reagent_update'),
    path('reagent/<int:reagent_id>/delete/', views.reagent_delete, name='reagent_delete'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('lab/<int:lab_id>/component/new/', views.component_create, name='component_create'),
    path('component/<int:component_id>/edit/', views.component_update, name='component_update'),
    path('component/<int:component_id>/delete/', views.component_delete, name='component_delete'),
    path('lab/<int:lab_id>/glassware/new/', views.glassware_create, name='glassware_create'),
    path('glassware/<int:glassware_id>/edit/', views.glassware_update, name='glassware_update'),
    path('glassware/<int:glassware_id>/delete/', views.glassware_delete, name='glassware_delete'),
    path('lab/<int:lab_id>/export-excel/', views.export_lab_to_excel, name='export_lab_to_excel'),
]