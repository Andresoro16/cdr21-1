from rest_framework import serializers
from .models import Cliente, Orden, OrdenItem


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
