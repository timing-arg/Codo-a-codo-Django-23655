from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import re

CUIT_REGEX = r'^\d{2}-\d{8}-\d{1}$'


# Create your models here.
# models.ForeignKey (uno a muchos)
# models.ManyToManyField (muchos a muchos)
# models.OneToOneField (uno a uno)

class Familia(models.Model):
    idfamilia = models.AutoField(primary_key=True, verbose_name="Código de familia")
    nombre = models.CharField(max_length=250, null=False, blank=False, unique=True, verbose_name="Descripción de la familia")
    fecha_creacion = models.DateTimeField(auto_now_add=True)




class Articulo(models.Model):
    idarticulo = models.AutoField(primary_key=True, verbose_name="Código de articulo")
    articulo_descripcion = models.CharField(max_length=250, null=False, blank=False, unique=True, verbose_name="Descripción del artículo")
    vigente = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    familia = models.ForeignKey (Familia, on_delete=models.CASCADE)    
    



class Material(models.Model):
    idmaterial = models.AutoField(primary_key=True, verbose_name="Código de material")
    material = models.CharField(max_length=250, null=False, blank=False, unique=True, verbose_name="Descripción del material")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)




class Producto(models.Model):
    codigo_de_producto = models.CharField(primary_key=True, max_length=13, verbose_name="Código de producto")
    descripcion = models.CharField(max_length=250, null=False, blank=False, unique=True, verbose_name="Descripción del producto")
    formato	= models.CharField(max_length=250, null=True, blank=True, verbose_name="Formato")
    anchoXlongitud	= models.CharField(max_length=250, null=True, blank=False, verbose_name="Ancho x longitud")
    ancho = models.DecimalField(null=True, blank=False, max_digits=5, decimal_places=2, verbose_name="Ancho")
    longitud = models.DecimalField(null=True, blank=False, max_digits=5, decimal_places=2, verbose_name="Longitud")
    buje = models.CharField(max_length=250, null=True, blank=False, verbose_name="Buje")
    codigo = models.CharField(max_length=250, null=True, blank=False, verbose_name="Código")
    minimo = models.IntegerField(null=True, blank=False, verbose_name="Mínimo")
    stockmin = models.IntegerField(null=True, blank=False, verbose_name="Stock mínimo")
    stockmax = models.IntegerField(null=True, blank=False, verbose_name="Stock máximo")
    existencia = models.IntegerField(null=True, blank=False, verbose_name="Existencia")
    tiempo_de_reposicion = models.CharField(max_length=250, null=True, blank=False, verbose_name="Tiempo de reposición")
    moneda = models.CharField(max_length=3, null=False, blank=True, choices=[("USD", "u$s"), ("ARS", "$")], default="USD", verbose_name="Moneda")
    iva = models.IntegerField(null=False, blank=True, verbose_name="IVA")
    precio_de_venta	= models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=2,verbose_name="Precio de venta")
    es_accesorio = models.CharField(max_length=250, null=True, blank=False, verbose_name="Es accesorio")
    codigo_de_origen = models.CharField(max_length=250, null=True, blank=False, verbose_name="Código de origen")
    tipo_de_unidad = models.CharField(max_length=10, null=False, blank=True, choices=[("p/millar", "millar"), ("p/unidad", "unidad"), ("precio", "precio")], default="p/millar", verbose_name="Tipo de unidad")
    utilidad = models.IntegerField(null=True, blank=False, verbose_name="Utilidad")
    precio_de_costo = models.DecimalField(null=True, blank=False, max_digits=10, decimal_places=2,verbose_name="Precio de costo")
    idcliente = models.IntegerField(null=False, blank=False, verbose_name="IdCliente")
    fecha_ultima_actualizacion = models.DateField(null=True, verbose_name="Fecha de última actualización")
    stockactual = models.IntegerField(null=True, blank=False, verbose_name="Stock actual")
    stockreservado = models.IntegerField(null=True, blank=False, verbose_name="Stock reservado")
    stockdisponible	= models.IntegerField(null=True, blank=False, verbose_name="Stock disponible")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)




class Persona(models.Model):
    nombre = models.CharField(max_length=50, null=True, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, null=True, verbose_name="Apellido")
    email = models.EmailField(max_length=100, null=True, verbose_name="Email")
    tipo_documento = models.CharField(
        max_length=3,
        null=True,
        choices=[
            ("DNI", "Documento Nacional de Identidad"),
            ("LC", "Libreta Cívica"),
            ("LE", "Libreta de Enrolamiento"),
            ("CI", "Cédula de Identidad")
        ],
        default="DNI",
        verbose_name="Tipo de documento"
    )
    documento = models.CharField(max_length=11, null=True, verbose_name="Documento número")
    firma = models.ImageField(upload_to='firmas/', null=True, blank=True, verbose_name="Firma")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.firma:
            width, height = get_image_dimensions(self.firma)
            if width > 500 or height > 500:
                raise ValidationError("La firma no puede tener más de 500x500 píxeles.")    

    #class Meta:
    #    abstract = True




class Operador(Persona):
    numero_operador = models.PositiveIntegerField(verbose_name="Operador")
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='operador_persona',  # Agrega un related_name único
    )


# class Contacto(Persona):



class Domicilio(models.Model):
    DOMICILIO_LEGAL = 'Legal'
    DOMICILIO_ENTREGA = 'Entrega'

    TIPO_DOMICILIO_CHOICES = [
        (DOMICILIO_LEGAL, 'Domicilio Legal'),
        (DOMICILIO_ENTREGA, 'Domicilio de Entrega'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_DOMICILIO_CHOICES, verbose_name="Tipo de Domicilio")
    direccion = models.CharField(max_length=100, verbose_name="Dirección")
    calle = models.CharField(max_length=100, verbose_name="Calle")
    numero = models.PositiveIntegerField(verbose_name="Número")
    piso = models.IntegerField(verbose_name="Piso")
    puerta = models.CharField(max_length=100, verbose_name="Puerta")
    codigo_postal = models.CharField(max_length=100, verbose_name="Código postal")
    localidad = models.CharField(max_length=100, verbose_name="Localidad")
    provincia = models.CharField(max_length=20, verbose_name="Provincia")
    pais = models.CharField(max_length=100, verbose_name="Dirección")
    numero_domicilio_de_entrega = models.PositiveIntegerField(null=True, blank=True, verbose_name="Número de Entrega")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        if self.tipo == self.DOMICILIO_ENTREGA and self.numero_entrega is not None:
            return f"Domicilio de Entrega {self.numero_entrega}: {self.direccion}"
        else:
            return f"{self.get_tipo_display()}: {self.direccion}"




class Telefono(models.Model):
    TELEFONO = 'Telefono'
    WHATSAPP = 'WhatsApp'
    TELEGRAM = 'Telegram'

    TIPO_TELEFONO_CHOICES = [
        (TELEFONO, 'Teléfono'),
        (WHATSAPP, 'WhatsApp'),
        (TELEGRAM, 'Telegram'),
        # Agrega más opciones según sea necesario
    ]

    tipo = models.CharField(max_length=30, choices=TIPO_TELEFONO_CHOICES, verbose_name="Tipo de Teléfono")
    numero = models.CharField(max_length=15, verbose_name="Número de Teléfono")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.numero}"




class Perfil(models.Model):
    informacion_adicional = models.TextField(verbose_name="Información Adicional")
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Perfil de {self.persona}"




class Prospec(models.Model):
    razon_social = models.CharField(max_length=30, verbose_name="Razón Social", default=0)
    nombre_fantasia = models.CharField(max_length=30, verbose_name="Nombre de Fantasía", default=0)
    estado = models.CharField(max_length=10, verbose_name="Estado", default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cuit = models.CharField(max_length=13, verbose_name="CUIT", default=0)

    def clean(self):
        # Validar el formato del CUIT
        if not re.match(CUIT_REGEX, self.cuit):
            raise ValidationError("El CUIT no tiene un formato válido.")    

    class Meta:
        abstract = True

    def nombre_completo(self):
        return f"{self.razon_social} {self.nombre_fantasia}"




class Rubro(models.Model):
    rubro = models.CharField(max_length=255, verbose_name="Rubro", default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)




class Subrubro(models.Model):
    subrubro = models.CharField(max_length=255, verbose_name="Subrubro",default=0)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)




class Prospecto(Prospec):
    prospecto = models.IntegerField(verbose_name="Prospecto", default=0)
    contactado = models.CharField(null=True, max_length=100, verbose_name="Contactado")
    fecha_ultimo_contacto = models.DateField(null=True, verbose_name="Fecha de último contacto")
    cliente = models.IntegerField(null=True, verbose_name="Cliente")
    rubro = models.ForeignKey(Rubro, on_delete=models.PROTECT, default=1)
    subrubro = models.ForeignKey(Subrubro, on_delete=models.PROTECT, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)





class Proveedor(Prospec):
    proveedor = models.IntegerField(verbose_name="Proveedor", default=0)   
    fecha_creacion = models.DateTimeField(auto_now_add=True)





class Presupuesto(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    condicion_de_pago = models.CharField(max_length=250, verbose_name="Condición de pago")
    validez = models.CharField(max_length=150, null=True, verbose_name="Validez")
    plazo_de_entrega = models.CharField(max_length=250, null=True, verbose_name="Plazo de entrega")
    tipo_de_cambio = models.CharField(max_length=250, verbose_name="Tipo de cambio")
    observacion = models.CharField(max_length=250, verbose_name="Observación")
    operador = models.IntegerField(verbose_name="Operador")
    estado_del_presupuesto = models.CharField(max_length=30, verbose_name="Estado del presupuesto")
    contacto = models.CharField(max_length=150, verbose_name="Nombre del contacto")
    fecha_dias_habiles = models.DateField(verbose_name="Fecha días hábiles")
    total_neto = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Total neto")
    cliente = models.ForeignKey(Prospecto, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)





class PresupuestoDetalle(models.Model):
    codigo_de_producto = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    descripcion = models.CharField(max_length=250, null=True, verbose_name="Descripción del producto")
    monto = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Monto")
    moneda = models.CharField(
        max_length=3,
        choices=[
            ("USD", "u$s"),
            ("ARS", "$")
            ], 
            default="USD", 
            verbose_name="Moneda"
    )
    tipo_de_unidad = models.CharField(
        max_length=10,
        choices=[
            ("p/millar", "millar"),
            ("p/unidad", "unidad"),
            ("precio", "precio")
            ],
            default="p/millar",
            verbose_name="Tipo de unidad"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Subtotal")
    proveedor_ppto = models.IntegerField(verbose_name="Proveedor ppto.")
    fecha_ppto_proveedor = models.DateField(verbose_name="Fecha ppto.")
    tipo_de_cambio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tipo de cbio ppto.")
    presupuesto = models.ForeignKey (Presupuesto, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)





class NotaPedido(models.Model):
    fecha = models.DateField(verbose_name="Fecha del pedido")
    fecha_de_entrega = models.DateField(verbose_name="Fecha de entrega")
    hora_de_entrega = models.TimeField(verbose_name="Hora de entrega") 
    anulada = models.BooleanField(default=False, verbose_name="¿Está anulado?")
    tipo_de_domicilio = models.CharField(max_length=50, null=True, verbose_name="Tipo de domicilio")
    direccion_de_entrega_numero = models.PositiveIntegerField(null=True, blank=True, verbose_name="Dirección de entrega")
    contacto = models.CharField(max_length=50, null=True, verbose_name="Contacto")
    oc = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    operador = models.IntegerField(verbose_name="Operador")
    hora_del_pedido = models.TimeField(verbose_name="Hora del pedido")
    tipo_de_cambio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tipo de cambio")
    condicion_de_pago = models.CharField(max_length=250, verbose_name="Condición de pago")
    remito = models.BooleanField(default=False, verbose_name="¿Tiene remito?")    
    factura = models.BooleanField(default=False, verbose_name="¿Tiene factura?")
    factura_numero = models.CharField(max_length=30, verbose_name="Factura número")
    factura_fecha = models.DateField(verbose_name="Fecha de factura")
    factura_usuario = models.CharField(max_length=30, verbose_name="Factura usuario")
    recibo_numero = models.PositiveIntegerField(null=True, blank=True, verbose_name="Número de recibo")
    recibo_fecha = models.DateField(verbose_name="Fecha de recibo")
    recibo_importe = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Importe del recibo")
    recibo_usuario = models.CharField(max_length=30,verbose_name="Recibo usuario")
    facturado = models.BooleanField(default=False, verbose_name="¿Facturado?")
    estado = models.CharField(max_length=30,verbose_name="Estado")
    estado_fecha = models.DateField(verbose_name="Fecha de estado")
    estado_usuario = models.CharField(max_length=30, verbose_name="Estado usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ManyToManyField(Prospecto)




class NotaPedidoDetalle(models.Model):
    item = models.PositiveIntegerField(verbose_name="Ítem")
    cliente = models.CharField(max_length=10, null=True, verbose_name="Código de producto")
    producto = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    descripcion_personalizada = models.CharField(max_length=250, null=True, verbose_name="Descripción personalizada")
    cantidad_en_millares = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Cantidad en millares")
    cantidad_x_rollo = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Cantidad por rollo")
    cantidad_de_rollos = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Cantidad de rollos")
    ancho_x_alto = models.DecimalField(max_digits=30, decimal_places=2,verbose_name="Ancho por alto")
    bandas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Bandas")
    material = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    buje = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    moneda = models.CharField(
        max_length=3,
        choices=[
            ("USD", "u$s"),
            ("ARS", "$")
            ], 
            default="USD", 
            verbose_name="Moneda"
    )
    tipo_de_unidad = models.CharField(
        max_length=10,
        choices=[
            ("p/millar", "millar"),
            ("p/unidad", "unidad"),
            ("precio", "precio")
            ],
            default="p/millar",
            verbose_name="Tipo de unidad"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Precio")
    iva_porciento = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="IVA %")
    importe = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Importe")
    iva_importe = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="IVA importe")
    total = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Total")
    observacion = models.CharField(max_length=250, null=True, verbose_name="Observación")
    estado = models.CharField(max_length=13, null=True, verbose_name="Estado")
    estado_fecha = models.CharField(max_length=13, null=True, verbose_name="Estado fecha")
    estado_usuario = models.CharField(max_length=13, null=True, verbose_name="Estado usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)





class Registracion(models.Model):
    fecha = models.DateField(verbose_name="Fecha de registracion")
    prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE)



    
