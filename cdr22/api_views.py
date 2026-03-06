from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .models import Orden
import json

# class Authentication: 
#     def login() : 
#         return ''
#     def register() :
#         return ''

@method_decorator(csrf_exempt, name='dispatch')
class OrdenAPIView(View):
    def post(self, request) :
        data = json.loads(request.body)
        items = data.get('items', [])  # ← Usar .get() es más seguro
        if not items :
            return JsonResponse({
                'error' : 'Los items son obligatorios'
            }, status=400);
    
        return JsonResponse({
            "mensaje" : "Creado con exito"
        }, status=201)
    def get(self, request) : 
        return JsonResponse({
            "mensaje" : "Ordenes obtenidas con exito"
        })

@method_decorator(csrf_exempt, name='dispatch')
class Reportes(View):
    def get(self, request):
        return JsonResponse({
            "mensaje" : "Reporte generado"
        })

