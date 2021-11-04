from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('carga_archivo', views.carga, name='carga-archivo'),
    path('consulta_datos', views.consultaDatos, name='consulta-datos'),
    path('grafica_fechas', views.graficaFechas, name='grafica-fechas'),
    path('grafica_valores', views.graficaValores, name='grafica-valores'),
]
