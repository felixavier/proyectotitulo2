from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('listar', views.listar, name='listar'),
    ##path('ventas/<int:pk>/', views.DetailView.as_view(), name='detail'),
]