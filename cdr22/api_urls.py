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
    path('ordenes/<int:orden_id>/factura/pdf/', api_views.FacturaPDFAPIView.as_view(), name='api.ordenes.factura.pdf'),
    path('compras/', api_views.ComprasAPIView.as_view(), name='api.compras'),
    path('compras/<int:compra_id>/estado/', api_views.CompraEstadoAPIView.as_view(), name='api.compras.estado'),
]
