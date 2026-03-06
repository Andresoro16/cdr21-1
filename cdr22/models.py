from django.db import models

# Create your models here.

class Orden(models.Model):
    metodo_pago = models.CharField(max_length=100)
    precio_total = models.DecimalField(decimal_places=2, max_digits=10)
    cliente_cedula = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ordenes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Orden #{self.id} - {self.cliente_cedula}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')  # ← Relación FK
    detalle = models.CharField(max_length=150)
    precio = models.DecimalField(decimal_places=2, max_digits=10)  # ← Cambié de SmallIntegerField
    cantidad = models.PositiveIntegerField()  # ← PositiveIntegerField es mejor
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'orden_items'
    
    def __str__(self):
        return f"{self.detalle} - Orden #{self.orden.id}"
