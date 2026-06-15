from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
import secrets
from cdr22.forms import ConfiguracionSistemaForm, UsuarioCreateForm
from cdr22.models import Producto, Categoria, Cliente, Compra, Orden, Proveedor
from cdr22.roles import ROLE_NAMES, USER_MANAGER_ROLES
from cdr22.serializers import CompraCreateSerializer
from cdr22.services.configuracion import get_configuracion_sistema
from cdr22.services.compras import CompraEstadoError, anular_compra, cambiar_estado_compra, crear_compra
import json


def _compra_payload_from_post(post_data):
    items = []
    producto_ids = post_data.getlist('producto')
    cantidades = post_data.getlist('cantidad')
    costos = post_data.getlist('costo_unitario')

    for producto_id, cantidad, costo_unitario in zip(producto_ids, cantidades, costos):
        if not producto_id:
            continue

        items.append({
            'producto_id': producto_id,
            'cantidad': cantidad,
            'costo_unitario': costo_unitario,
        })

    return {
        'proveedor_id': post_data.get('proveedor') or None,
        'proveedor_nombre': post_data.get('proveedor_nombre', '').strip(),
        'numero_factura': post_data.get('numero_factura', '').strip(),
        'fecha_compra': post_data.get('fecha_compra'),
        'estado': post_data.get('estado', 'borrador'),
        'metodo_pago': post_data.get('metodo_pago', ''),
        'impuesto': post_data.get('impuesto') or '0',
        'observaciones': post_data.get('observaciones', '').strip(),
        'items': items,
    }

def _can_manage_users(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name__in=USER_MANAGER_ROLES).exists()
    )

def _ensure_roles():
    for role_name in ROLE_NAMES:
        Group.objects.get_or_create(name=role_name)

def _send_password_setup_email(request, user):
    reset_form = PasswordResetForm({'email': user.email})
    if reset_form.is_valid():
        reset_form.save(
            request=request,
            use_https=request.is_secure(),
            email_template_name='registration/password_setup_email.html',
            subject_template_name='registration/password_setup_subject.txt',
        )

def principal (request):
    return render(request, 'landing.html')

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
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 10)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
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

@login_required(login_url='login')
def pos(request):
    return render(request, 'dashboard/pos/index.html')

@login_required(login_url='login')
def ventas_index(request):
    ventas_list = Orden.objects.select_related('cliente', 'factura').prefetch_related('items').all()
    paginator = Paginator(ventas_list, 10)
    page_number = request.GET.get('page')
    ventas = paginator.get_page(page_number)

    return render(request, 'dashboard/ventas/index.html', {'ventas': ventas})

@login_required(login_url='login')
def ventas_detalle(request, venta_id):
    venta = get_object_or_404(
        Orden.objects.select_related('cliente', 'factura').prefetch_related('items'),
        id=venta_id
    )

    return render(request, 'dashboard/ventas/detalle.html', {'venta': venta})

@login_required(login_url='login')
def clientes_index(request):
    clientes_list = Cliente.objects.all()
    paginator = Paginator(clientes_list, 10)
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)
    
    return render(request, 'dashboard/clientes/index.html', {'clientes': clientes})

@login_required(login_url='login')
def clientes_crear(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email', '')
        telefono = request.POST.get('telefono', '')
        
        try:
            cliente = Cliente.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellidos=apellidos,
                email=email,
                telefono=telefono
            )
            return redirect('clientes_index')
        except Exception as e:
            return render(request, 'dashboard/clientes/crear.html', {
                'error': str(e)
            })
    
    return render(request, 'dashboard/clientes/crear.html')

@login_required(login_url='login')
def clientes_editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email', '')
        telefono = request.POST.get('telefono', '')
        
        try:
            cliente.cedula = cedula
            cliente.nombre = nombre
            cliente.apellidos = apellidos
            cliente.email = email
            cliente.telefono = telefono
            cliente.save()
            
            return redirect('clientes_index')
        except Exception as e:
            return render(request, 'dashboard/clientes/editar.html', {
                'cliente': cliente,
                'error': str(e)
            })
    
    return render(request, 'dashboard/clientes/editar.html', {
        'cliente': cliente
    })

@login_required(login_url='login')
def clientes_eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes_index')
    
    return render(request, 'dashboard/clientes/eliminar.html', {
        'cliente': cliente
    })

@login_required(login_url='login')
def usuarios_index(request):
    if not _can_manage_users(request.user):
        messages.error(request, 'No tienes permisos para gestionar usuarios.')
        return redirect('home')

    usuarios_list = User.objects.prefetch_related('groups').order_by('username')
    paginator = Paginator(usuarios_list, 10)
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, 'dashboard/usuarios/index.html', {'usuarios': usuarios})

@login_required(login_url='login')
def usuarios_crear(request):
    if not _can_manage_users(request.user):
        messages.error(request, 'No tienes permisos para gestionar usuarios.')
        return redirect('home')

    _ensure_roles()

    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=form.cleaned_data['is_active'],
            )

            if form.cleaned_data['password_mode'] == 'manual':
                user.set_password(form.cleaned_data['password1'])
            else:
                user.set_password(secrets.token_urlsafe(24))

            user.save()
            user.groups.set([form.cleaned_data['role']])

            if form.cleaned_data['password_mode'] == 'email':
                _send_password_setup_email(request, user)
                messages.success(request, 'Usuario creado. Se generó el correo para configurar contraseña.')
            else:
                messages.success(request, 'Usuario creado correctamente.')

            return redirect('usuarios_index')
    else:
        form = UsuarioCreateForm(initial={'password_mode': 'email', 'is_active': True})

    return render(request, 'dashboard/usuarios/crear.html', {'form': form})

@login_required(login_url='login')
def configuracion_general(request):
    if not _can_manage_users(request.user):
        messages.error(request, 'No tienes permisos para gestionar la configuración.')
        return redirect('home')

    configuracion = get_configuracion_sistema()

    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada correctamente.')
            return redirect('configuracion_general')
    else:
        form = ConfiguracionSistemaForm(instance=configuracion)

    return render(request, 'dashboard/configuracion/general.html', {'form': form})

@login_required(login_url='login')
def compras_index(request):
    compras_list = Compra.objects.select_related('proveedor').prefetch_related('items').all()
    paginator = Paginator(compras_list, 10)
    page_number = request.GET.get('page')
    compras = paginator.get_page(page_number)

    return render(request, 'dashboard/compras/index.html', {'compras': compras})

@login_required(login_url='login')
def compras_detalle(request, compra_id):
    compra = get_object_or_404(
        Compra.objects.select_related('proveedor').prefetch_related('items__producto'),
        id=compra_id
    )

    return render(request, 'dashboard/compras/detalle.html', {'compra': compra})

@login_required(login_url='login')
def compras_crear(request):
    productos = Producto.objects.filter(estado='activo').order_by('nombre')
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        payload = _compra_payload_from_post(request.POST)
        serializer = CompraCreateSerializer(data=payload)

        if serializer.is_valid():
            crear_compra(serializer.validated_data)
            return redirect('compras_index')

        return render(request, 'dashboard/compras/crear.html', {
            'productos': productos,
            'proveedores': proveedores,
            'error': 'Hay errores en el formulario',
            'form_errors': serializer.errors,
        })

    return render(request, 'dashboard/compras/crear.html', {
        'productos': productos,
        'proveedores': proveedores,
    })

@login_required(login_url='login')
def compras_cambiar_estado(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)

    if request.method != 'POST':
        return redirect('compras_index')

    nuevo_estado = request.POST.get('estado')
    motivo_anulacion = request.POST.get('motivo_anulacion', '').strip()

    try:
        if nuevo_estado == 'anulada':
            anular_compra(compra, motivo=motivo_anulacion)
        else:
            cambiar_estado_compra(compra, nuevo_estado)
        messages.success(request, 'Estado de la compra actualizado correctamente.')
    except CompraEstadoError as e:
        primer_error = next(iter(e.errores.values()))[0]
        messages.error(request, primer_error)

    return redirect('compras_index')
