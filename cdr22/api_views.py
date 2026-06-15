from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import models, transaction
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
                "cedula" : order.cliente.cedula if order.cliente else None,
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

@method_decorator(csrf_exempt, name='dispatch')
class OrdenCreateAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({
                "mensaje": "Mensaje inválido, debe ser JSON"
            }, status=400)
        
        try:
            # Obtener datos del cliente
            cliente_data = data.get('cliente', {})
            cedula = cliente_data.get('cedula', '').strip()
            
            if not cedula:
                return JsonResponse({
                    "mensaje": "La cédula del cliente es requerida"
                }, status=400)
            
            # Buscar o crear cliente
            cliente, created = Cliente.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre': cliente_data.get('nombre', ''),
                    'apellidos': cliente_data.get('apellidos', ''),
                    'email': cliente_data.get('email', ''),
                    'telefono': cliente_data.get('telefono', '')
                }
            )
            
            if not created:
                # Actualizar datos si el cliente ya existe
                cliente.nombre = cliente_data.get('nombre', cliente.nombre)
                cliente.apellidos = cliente_data.get('apellidos', cliente.apellidos)
                cliente.email = cliente_data.get('email', cliente.email)
                cliente.telefono = cliente_data.get('telefono', cliente.telefono)
                cliente.save()
            
            # Obtener datos de la orden
            items = data.get('items', [])
            metodo_pago = data.get('metodo_pago', 'no especificado')
            subtotal = float(data.get('subtotal', 0))
            impuesto = float(data.get('impuesto', 0))
            total = float(data.get('total', 0))
            
            if not items:
                return JsonResponse({
                    "mensaje": "La orden debe contener al menos un artículo"
                }, status=400)
            
            productos_validados = []

            for item in items:
                # Buscar por 'id' (como lo envía el carrito del POS)
                producto_id = item.get('id') or item.get('producto_id')
                
                if not producto_id:
                    return JsonResponse({
                        "mensaje": "Cada item debe tener un id o producto_id"
                    }, status=400)
                
                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    return JsonResponse({
                        "mensaje": f"Producto con id {producto_id} no existe"
                    }, status=404)

                cantidad = int(item.get('cantidad', 1))

                if producto.stock < cantidad:
                    return JsonResponse({
                        "mensaje": "Stock insuficiente",
                        "errores": {
                            "producto_id": producto.id,
                            "producto": producto.nombre,
                            "stock_disponible": producto.stock,
                            "cantidad_solicitada": cantidad,
                            "detalle": f"No hay suficiente stock para {producto.nombre}. Disponible: {producto.stock}, solicitado: {cantidad}."
                        }
                    }, status=422)

                productos_validados.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unitario": float(item.get('precio_unitario', 0)),
                })

            from .models import Factura, OrdenItem

            with transaction.atomic():
                # Crear factura
                factura_numero = f"FAC-{Factura.objects.count() + 1:06d}"

                factura = Factura.objects.create(
                    numero=factura_numero,
                    cliente=cliente,
                    subtotal=subtotal,
                    impuesto=impuesto,
                    total=total,
                    metodo_pago=metodo_pago,
                    estado='emitida'
                )

                # Crear orden
                orden = Orden.objects.create(
                    cliente=cliente,
                    factura=factura,
                    metodo_pago=metodo_pago,
                    subtotal=subtotal,
                    impuesto=impuesto,
                    precio_total=total,
                    estado='completada'
                )

                # Crear items de la orden
                for item_validado in productos_validados:
                    producto = item_validado["producto"]
                    cantidad = item_validado["cantidad"]
                
                    OrdenItem.objects.create(
                        orden=orden,
                        detalle=producto.nombre,
                        precio=item_validado["precio_unitario"],
                        cantidad=cantidad
                    )

                    # Actualizar stock del producto
                    producto.stock -= cantidad
                    producto.save()
            
            return JsonResponse({
                "mensaje": "Orden creada exitosamente",
                "orden": {
                    'id': orden.id,
                    'factura_numero': factura.numero,
                    'cliente': {
                        'cedula': cliente.cedula,
                        'nombre': cliente.nombre,
                        'apellidos': cliente.apellidos,
                    },
                    'subtotal': str(orden.subtotal),
                    'impuesto': str(orden.impuesto),
                    'total': str(orden.precio_total),
                    'estado': orden.estado,
                    'fecha': orden.created_at.isoformat()
                }
            }, status=201)
        
        except Producto.DoesNotExist:
            return JsonResponse({
                "mensaje": "Uno o más productos no existen"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "mensaje": f"Error al crear la orden: {str(e)}"
            }, status=500)
