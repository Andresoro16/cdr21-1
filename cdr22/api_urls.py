from django.urls import path
from django.http import HttpResponse
from . import api_views

urlpatterns = [
    path('ordenes/', api_views.OrdenAPIView.as_view(), name='api.ordenes'),
    path('reporte/', api_views.Reportes.as_view(), name='api.reportes'),
    path('productos/search/', api_views.ProductoSearchAPIView.as_view(), name='api.productos.search'),
]