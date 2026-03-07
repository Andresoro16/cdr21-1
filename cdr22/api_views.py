from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .models import Orden
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

