from django.urls import path
from django.http import HttpResponse
from . import api_views

urlpatterns = [
    path('ordenes/', api_views.OrdenAPIView.as_view(), name='api.ordenes'),
    path('reporte/', api_views.Reportes.as_view(), name='api.reportes'),
    path('productos/search/', api_views.ProductoSearchAPIView.as_view(), name='api.productos.search'),
    path('clientes/search/', api_views.ClienteSearchAPIView.as_view(), name='api.clientes.search'),
    path('clientes/create/', api_views.ClienteCreateAPIView.as_view(), name='api.clientes.create'),
    path('ordenes/create/', api_views.OrdenCreateAPIView.as_view(), name='api.ordenes.create'),
]