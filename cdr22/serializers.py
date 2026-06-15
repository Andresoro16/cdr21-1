from rest_framework import serializers
from decimal import Decimal
from .models import Cliente, Compra, Orden, OrdenItem, Producto, Proveedor


class OrdenItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenItem
        fields = ['detalle', 'precio', 'cantidad']
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value

class OrdenSerializer(serializers.ModelSerializer):
    items = OrdenItemSerializer(many=True, write_only=True)  # ← Nested validation
    cliente_cedula = serializers.CharField(write_only=True)
    
    class Meta:
        model = Orden
        fields = ['metodo_pago', 'cliente_cedula', 'estado', 'items']

    def validate_cliente_cedula(self, value):
        if not Cliente.objects.filter(cedula=value).exists():
            raise serializers.ValidationError("No existe un cliente con esta cédula")
        return value

    def validate_metodo_pago(self, value):
        allowed_methods = ['efectivo', 'tarjeta', 'transferencia']
        if value not in allowed_methods:
            raise serializers.ValidationError(f"Método debe ser uno de: {', '.join(allowed_methods)}")
        return value

    def create(self, validated_data):
        """Crear orden con items (transacción)"""
        cliente_cedula = validated_data.pop('cliente_cedula')
        items_data = validated_data.pop('items')
        cliente = Cliente.objects.get(cedula=cliente_cedula)
        total = 0
        for item in items_data:
            total += item['precio']
        validated_data['precio_total'] = total
        validated_data['cliente'] = cliente
        orden = Orden.objects.create(**validated_data)

        for item_data in items_data:
            OrdenItem.objects.create(orden=orden, **item_data)

        return orden

class OrdenReadSerializer(serializers.ModelSerializer):
    cliente_cedula = serializers.CharField(source='cliente.cedula', read_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'metodo_pago', 'precio_total', 'cliente_cedula', 'estado', 'created_at']


class CompraItemCreateSerializer(serializers.Serializer):
    producto_id = serializers.PrimaryKeyRelatedField(
        source='producto',
        queryset=Producto.objects.filter(estado='activo'),
        error_messages={
            'does_not_exist': 'El producto seleccionado no existe o no está activo.',
            'incorrect_type': 'El producto seleccionado no es válido.',
            'required': 'Seleccione un producto.',
        }
    )
    cantidad = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'La cantidad debe ser mayor a cero.',
            'required': 'Ingrese la cantidad.',
            'invalid': 'La cantidad debe ser un número entero.',
        }
    )
    costo_unitario = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal('0.01'),
        error_messages={
            'min_value': 'El costo unitario debe ser mayor a cero.',
            'required': 'Ingrese el costo unitario.',
            'invalid': 'El costo unitario debe ser un número válido.',
        }
    )

    def validate(self, attrs):
        attrs['subtotal'] = attrs['cantidad'] * attrs['costo_unitario']
        return attrs


class CompraCreateSerializer(serializers.Serializer):
    proveedor_id = serializers.PrimaryKeyRelatedField(
        source='proveedor',
        queryset=Proveedor.objects.all(),
        required=False,
        allow_null=True,
        error_messages={
            'does_not_exist': 'El proveedor seleccionado no existe.',
            'incorrect_type': 'El proveedor seleccionado no es válido.',
        }
    )
    proveedor_nombre = serializers.CharField(required=False, allow_blank=True, max_length=150)
    numero_factura = serializers.CharField(required=False, allow_blank=True, max_length=50)
    fecha_compra = serializers.DateField(
        error_messages={
            'required': 'Ingrese la fecha de compra.',
            'invalid': 'Ingrese una fecha válida.',
        }
    )
    estado = serializers.ChoiceField(
        choices=Compra.ESTADO_CHOICES,
        error_messages={
            'invalid_choice': 'Seleccione un estado válido.',
            'required': 'Seleccione el estado de la compra.',
        }
    )
    metodo_pago = serializers.ChoiceField(
        choices=Compra.METODO_PAGO_CHOICES,
        required=False,
        allow_blank=True,
        error_messages={
            'invalid_choice': 'Seleccione un método de pago válido.',
        }
    )
    impuesto = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0, required=False)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    items = CompraItemCreateSerializer(many=True)

    def validate(self, attrs):
        if not attrs.get('items'):
            raise serializers.ValidationError({
                'items': ['La compra debe tener al menos un producto.']
            })
        return attrs


class CompraReadSerializer(serializers.ModelSerializer):
    proveedor = serializers.CharField(source='proveedor.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    metodo_pago_display = serializers.CharField(source='get_metodo_pago_display', read_only=True)

    class Meta:
        model = Compra
        fields = [
            'id',
            'proveedor',
            'numero_factura',
            'fecha_compra',
            'subtotal',
            'impuesto',
            'total',
            'metodo_pago',
            'metodo_pago_display',
            'estado',
            'estado_display',
            'stock_aplicado',
            'observaciones',
            'motivo_anulacion',
            'anulada_en',
            'created_at',
        ]


class CompraEstadoSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(
        choices=Compra.ESTADO_CHOICES,
        error_messages={
            'invalid_choice': 'Seleccione un estado válido.',
            'required': 'Seleccione el nuevo estado.',
        }
    )
    motivo_anulacion = serializers.CharField(required=False, allow_blank=True)
