from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    ##path('ventas/<int:pk>/', views.DetailView.as_view(), name='detail'),
]