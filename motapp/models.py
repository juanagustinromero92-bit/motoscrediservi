# Create your models here.
from django.db import models

# ==========================================
# 1. CATÁLOGO PROFESIONAL DE MOTOS
# ==========================================

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='marcas/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True) # Ej: Scooter, Enduro, Pista, Touring
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Moto(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # Para URLs limpias (ej: /motos/yamaha-mt07)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='motos')
    modelo = models.IntegerField(default=2027) # <-- Asegúrate de tener este campo
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='motos')
    
    # Especificaciones técnicas
    cilindraje = models.IntegerField(help_text="En cc")
    potencia = models.CharField(max_length=50, blank=True, help_text="Ej: 74 HP @ 9000 RPM")
    frenos = models.CharField(max_length=50, blank=True, help_text="Ej: ABS Doble disco")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="En kg")
    anio = models.IntegerField(verbose_name="Año", blank=True, null=True, default=2027)
    
    # Comercial
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    destacado = models.BooleanField(default=False, help_text="Para mostrar en la página principal")
    imagen_principal = models.ImageField(upload_to='motos/')
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre} ({self.anio})"


class ImagenMoto(models.Model):
    """Galería de imágenes secundarias para la vista detallada de la moto"""
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='motos/galeria/')


# ==========================================
# 2. INFORMACIÓN DE LA EMPRESA
# ==========================================

class InfoEmpresa(models.Model):
    nombre = models.CharField(max_length=100, default="Mi Concesionario")
    mision = models.TextField()
    vision = models.TextField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    horario_atencion = models.CharField(max_length=100)
    link_whatsapp = models.URLField(blank=True, help_text="Enlace directo a WhatsApp de ventas")

    class Meta:
        verbose_name = "Información de la Empresa"
        verbose_name_plural = "Información de la Empresa"

    def __str__(self):
        return self.nombre


# ==========================================
# 3. MÓDULO DE PAGOS Y PEDIDOS
# ==========================================

class Pedido(models.Model):
    ESTADOS_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('CANCELADO', 'Cancelado'),
    ]

    moto = models.ForeignKey(Moto, on_delete=models.PROTECT)
    cliente_nombre = models.CharField(max_length=100)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    cliente_documento = models.CharField(max_length=20, verbose_name="Cédula/DNI")
    
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)
    estado_pago = models.CharField(max_length=15, choices=ESTADOS_PAGO, default='PENDIENTE')
    
    # Campos para pasarela de pago (Ej: Wompi, MercadoPago, Stripe, PayU)
    id_transaccion_pasarela = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente_nombre} ({self.estado_pago})"
