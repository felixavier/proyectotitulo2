from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('data', views.data, name='data'),
]