from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from cdr22.models import Producto, Categoria
import json

def principal (request):
    return render(request, 'dashboard/principal.html')

""" Auth Views """
def login_view(request):
    if request.method == 'POST':
        # Si viene JSON (desde fetch)
           if request.content_type == 'application/json':
               data = json.loads(request.body)
               print(data)  # Aquí ves los datos
               username = data.get('user')  # o 'username' según lo que envíes
               password = data.get('password')

               user = authenticate(request, username=username, password=password)
               if user is not None:
                   auth_login(request, user)
                   return JsonResponse({"message": "Login exitoso"})
               else:
                   return JsonResponse({"message": "Credenciales inválidas"}, status=422)

           # Si viene formulario tradicional
           else:
               form = AuthenticationForm(request, data=request.POST)
               if form.is_valid():
                   user = form.get_user()
                   auth_login(request, user)
                   return redirect('home')
               else:
                   return JsonResponse({"message": "Credenciales inválidas"}, status=422)
    return render(request, 'invitado/login.html')   

def olvidePassword(request):
    return render(request, 'invitado/olvide-password.html')


""" Dashboard Views """
@login_required(login_url='login') 
def home(request):
    return render(request, 'dashboard/home.html')

def testing(request):
    return render(request, 'testing.html')

""" Productos Views """
@login_required(login_url='login')
def productos_index(request):
    productos = Producto.objects.all()
    return render(request, 'dashboard/productos/index.html', {'productos': productos})

@login_required(login_url='login')
def productos_crear(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        marca = request.POST.get('marca')
        precio_costo = request.POST.get('precio_costo')
        precio_venta = request.POST.get('precio_venta')
        garantia_meses = request.POST.get('garantia_meses')
        estado = request.POST.get('estado')
        
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            
            Producto.objects.create(
                sku=sku,
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                marca=marca,
                precio_costo=precio_costo,
                precio_venta=precio_venta,
                garantia_meses=garantia_meses,
                estado=estado
            )
            
            return redirect('productos_index')
        except Categoria.DoesNotExist:
            return render(request, 'dashboard/productos/crear.html', {
                'categorias': Categoria.objects.all(),
                'error': 'Categoría no válida'
            })
    
    categorias = Categoria.objects.all()
    return render(request, 'dashboard/productos/crear.html', {'categorias': categorias})

@login_required(login_url='login')
def productos_editar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        sku = request.POST.get('sku')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        marca = request.POST.get('marca')
        precio_costo = request.POST.get('precio_costo')
        precio_venta = request.POST.get('precio_venta')
        garantia_meses = request.POST.get('garantia_meses')
        estado = request.POST.get('estado')
        
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            
            # Actualizar el producto
            producto.sku = sku
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.categoria = categoria
            producto.marca = marca
            producto.precio_costo = precio_costo
            producto.precio_venta = precio_venta
            producto.garantia_meses = garantia_meses
            producto.estado = estado
            producto.save()
            
            return redirect('productos_index')
        except Categoria.DoesNotExist:
            return render(request, 'dashboard/productos/editar.html', {
                'producto': producto,
                'categorias': Categoria.objects.all(),
                'error': 'Categoría no válida'
            })
    
    categorias = Categoria.objects.all()
    return render(request, 'dashboard/productos/editar.html', {
        'producto': producto,
        'categorias': categorias
    })

@login_required(login_url='login')
def productos_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        # Guardar información del producto para el mensaje
        producto_nombre = producto.nombre
        producto_sku = producto.sku
        
        # Eliminar el producto
        producto.delete()
        
        return redirect('productos_index')
    
    # Si es GET, mostrar página de confirmación
    return render(request, 'dashboard/productos/eliminar.html', {
        'producto': producto
    })
