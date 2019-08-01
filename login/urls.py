from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.index, name='login'),
    path('submit', views.submit, name='login'),
    ##path('ventas/<int:pk>/', views.DetailView.as_view(), name='detail'),
]