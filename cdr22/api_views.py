from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import models
from .models import Orden, Producto, Cliente
from .serializers import OrdenSerializer, OrdenReadSerializer
import json

# class Authentication: 
#     def login() : 
#         return ''
#     def register() :
#         return ''

@method_decorator(csrf_exempt, name='dispatch')
class OrdenAPIView(View):
    def post(self, request) :

        """ Validar JSON """
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                "mensaje" : "Mensaje invalido, debe ser JSON"
            })
        """ Validacion de serializer """
        serializer = OrdenSerializer(data=data)
        print(serializer)
        if not serializer.is_valid():
            return JsonResponse({
                "mensaje" : "Hubo un error",
                "errores" : serializer.errors
            }, status=422)
        
        """ Datos validados, guardar orden """
        validated_data = serializer.validated_data
        order =  serializer.save()
        print(order)
        return JsonResponse({
            "mensaje" : "Creado con exito",
            "orden: " : {
                "cedula" : order.cliente_cedula,
                "precio_total" : order.precio_total,
                "estado" : order.estado,
                "metodo_pago" : order.metodo_pago,
                "id" : order.id
            }
            
        }, status=201)
    def get(self, request) : 
        ordenes = Orden.objects.all()
        serializer = OrdenReadSerializer(ordenes, many=True)
        return JsonResponse({
            "mensaje" : "Ordenes obtenidas con exito",
            "ordenes" : serializer.data
        })

@method_decorator(csrf_exempt, name='dispatch')
class Reportes(View):
    def get(self, request):
        total_ordenes = 0
        numero_de_ordenes=0
        agrupacion_pagos={}

        ordenes = Orden.objects.all()

        for orden in ordenes:
            total_ordenes +=orden.precio_total
            numero_de_ordenes +=1
            if orden.metodo_pago in agrupacion_pagos:
                agrupacion_pagos[orden.metodo_pago] +=orden.precio_total
            else:
                agrupacion_pagos[orden.metodo_pago] = orden.precio_total
            

        return JsonResponse({
            "mensaje" : "Reporte generado",
            "reporte" : {
                "total_ordenes" : total_ordenes,
                "numero_de_ordenes" : numero_de_ordenes,
                "agrupacion_pagos" : agrupacion_pagos
            }
        })

@method_decorator(csrf_exempt, name='dispatch')
class ProductoSearchAPIView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({
                "mensaje": "Debe proporcionar un parámetro de búsqueda 'q'",
                "productos": []
            }, status=400)
        
        # Buscar por SKU, nombre o marca
        productos = Producto.objects.filter(
            estado='activo'
        ).filter(
            models.Q(sku__icontains=query) | 
            models.Q(nombre__icontains=query) | 
            models.Q(marca__icontains=query)
        )[:10]  # Limitar a 10 resultados
        
        resultado = []
        for producto in productos:
            resultado.append({
                'id': producto.id,
                'sku': producto.sku,
                'nombre': producto.nombre,
                'marca': producto.marca,
                'precio_venta': float(producto.precio_venta),
                'stock': producto.stock,
                'categoria': producto.categoria.nombre if producto.categoria else None,
            })
        
        return JsonResponse({
            "mensaje": "Productos encontrados",
            "productos": resultado
        })

@method_decorator(csrf_exempt, name='dispatch')
class ClienteSearchAPIView(View):
    def get(self, request):
        cedula = request.GET.get('cedula', '').strip()
        
        if not cedula:
            return JsonResponse({
                "mensaje": "Debe proporcionar un parámetro 'cedula'",
                "cliente": None
            }, status=400)
        
        try:
            cliente = Cliente.objects.get(cedula=cedula)
            return JsonResponse({
                "mensaje": "Cliente encontrado",
                "cliente": {
                    'id': cliente.id,
                    'cedula': cliente.cedula,
                    'nombre': cliente.nombre,
                    'apellidos': cliente.apellidos,
                    'email': cliente.email,
                    'telefono': cliente.telefono,
                }
            })
        except Cliente.DoesNotExist:
            return JsonResponse({
                "mensaje": "Cliente no encontrado",
                "cliente": None
            }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class ClienteCreateAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                "mensaje": "Mensaje inválido, debe ser JSON"
            }, status=400)
        
        # Validar campos requeridos
        cedula = data.get('cedula', '').strip()
        nombre = data.get('nombre', '').strip()
        apellidos = data.get('apellidos', '').strip()
        
        if not cedula or not nombre or not apellidos:
            return JsonResponse({
                "mensaje": "Los campos cedula, nombre y apellidos son requeridos",
                "errores": {
                    "cedula": "Requerido" if not cedula else "",
                    "nombre": "Requerido" if not nombre else "",
                    "apellidos": "Requerido" if not apellidos else "",
                }
            }, status=422)
        
        # Verificar si ya existe
        if Cliente.objects.filter(cedula=cedula).exists():
            return JsonResponse({
                "mensaje": "Ya existe un cliente con esta cédula",
            }, status=422)
        
        # Crear cliente
        cliente = Cliente.objects.create(
            cedula=cedula,
            nombre=nombre,
            apellidos=apellidos,
            email=data.get('email', ''),
            telefono=data.get('telefono', '')
        )
        
        return JsonResponse({
            "mensaje": "Cliente creado exitosamente",
            "cliente": {
                'id': cliente.id,
                'cedula': cliente.cedula,
                'nombre': cliente.nombre,
                'apellidos': cliente.apellidos,
                'email': cliente.email,
                'telefono': cliente.telefono,
            }
        }, status=201)