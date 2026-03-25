from django.db import models

# ============================================
# PRODUCTOS
# ============================================

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categorias'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('descontinuado', 'Descontinuado'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    sku = models.CharField(max_length=50, unique=True, help_text="Código único del repuesto")
    
    # Categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    
    # Precios
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, help_text="Costo para el taller")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio al cliente")
    
    # Stock
    stock = models.PositiveIntegerField(default=0, help_text="Cantidad disponible")
    stock_minimo = models.PositiveIntegerField(default=5)
    
    # Detalles
    marca = models.CharField(max_length=100, help_text="Fabricante del repuesto")
    garantia_meses = models.PositiveIntegerField(default=12, help_text="Meses de garantía")
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'productos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nombre} - {self.sku}"
    
    def margen_ganancia(self):
        """Calcula el margen de ganancia en porcentaje"""
        if self.precio_costo > 0:
            return ((self.precio_venta - self.precio_costo) / self.precio_costo) * 100
        return 0

# ============================================
# ÓRDENES
# ============================================

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
