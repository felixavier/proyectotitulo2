from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('listar', views.listar, name='listar'),
<<<<<<< HEAD
    path('evolucion', views.gr_total, name='evolucion_ventas'),
    path('fechas', views.gr_tiempo, name='fechas'),
    path('productos_vendidos', views.tb_productos, name='productos_vendidos'),
    path('data', views.data_fecha, name='data'),
=======
>>>>>>> origin/master
    ##path('ventas/<int:pk>/', views.DetailView.as_view(), name='detail'),
]