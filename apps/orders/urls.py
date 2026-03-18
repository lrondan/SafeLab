from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
]