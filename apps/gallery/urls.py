from django.urls import path
from .views import gallery, safety

urlpatterns = [
    path('', gallery, name='gallery'),
    path('safety/', safety, name='safety'),
]