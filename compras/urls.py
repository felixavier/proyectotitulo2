from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('data', views.data_request, name='data'),
    path('dashboard', views.index, name='dashboard'),
]