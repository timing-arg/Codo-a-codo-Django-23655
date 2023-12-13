from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import re

CUIT_REGEX = r'^\d{2}-\d{8}-\d{1}$'


# Create your models here.
# models.ForeignKey (uno a muchos)
# models.ManyToManyField (muchos a muchos)
# models.OneToOneField (uno a uno)

 #class Producto(models.Model):
 #   codigo_de_producto = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
 #   IdArticulo = models.IntegerField(verbose_name="IdArticulo")
 #   IdMaterial = models.IntegerField(verbose_name="IdMaterial")
 #   descripcion = models.CharField(max_length=250, null=True, verbose_name="Descripción del producto")
 #   Formato	= models.CharField(max_length=250, null=True, verbose_name="Formato")
 #   AnchoXLongitud	= models.CharField(max_length=250, null=True, verbose_name="Ancho x longitud")
 #   Ancho = models.IntegerField(verbose_name="Ancho")
 #   Longitud = models.IntegerField(verbose_name="Longitud")
 #   Buje = models.CharField(max_length=250, null=True, verbose_name="Buje")
 #   Codigo = models.CharField(max_length=250, null=True, verbose_name="Codigo")
 #   Minimo = models.IntegerField(verbose_name="Mínimo")
 #   StockMin = models.IntegerField(verbose_name="Stock mínimo")
 #   StockMax = models.IntegerField(verbose_name="Stock máximo")
 #   Existencia = models.IntegerField(verbose_name="Existencia")
 #   TiempoReposicion = models.CharField(max_length=250, null=True, verbose_name="Tiempo de reposición")
 #   moneda = models.CharField(max_length=3, choices=[("USD", "u$s"), ("ARS", "$")], default="USD", verbose_name="Moneda")
 #   iva = models.IntegerField(verbose_name="IVA")
 #   PrecioVenta	= models.CharField(max_length=3, choices=[("USD", "u$s"), ("ARS", "$")], default="USD", verbose_name="Moneda")
 #   #Imagen	Objeto OLE
 #   EsAccesorio	= models.CharField(max_length=250, null=True, verbose_name="Es accesorio")
 #   CodigoOrigen = models.CharField(max_length=250, null=True, verbose_name="Código origen")
 #   tipo_de_unidad = models.CharField(max_length=10, choices=[("p/millar", "millar"), ("p/unidad", "unidad"), ("precio", "precio")], default="p/millar", verbose_name="Tipo de unidad")
 #   Utilidad = models.IntegerField(verbose_name="Utilidad")
 #   PrecioCosto = models.IntegerField(verbose_name="Precio de costo")
 #   IdCliente = models.IntegerField(verbose_name="IdCliente")
 #   FechaUltActualiz = models.DateField(null=True, verbose_name="Fecha de última actualización")
    #Actualizar	    si/no
 #   StockActual = models.IntegerField(verbose_name="Stock actual")
 #   StockReservado = models.IntegerField(verbose_name="Stock reservado")
 #   StockDisponible	= models.IntegerField(verbose_name="Stock disponible")



class Persona(models.Model):
    nombre = models.CharField(max_length=30, null=True, verbose_name="Nombre")
    apellido = models.CharField(max_length=30, null=True, verbose_name="Apellido")
    email = models.EmailField(max_length=30, null=True, verbose_name="Email")
    tipo_documento = models.CharField(max_length=35, null=True, choices=[("DNI", "Documento Nacional de Identidad"), ("LC", "Libreta Cívica"), ("LE", "Libreta de Enrolamiento"), ("CI", "Cédula de Identidad")], default="DNI", verbose_name="Tipo de documento")
    documento = models.CharField(max_length=11, null=True, verbose_name="Documento número")
    firma = models.ImageField(upload_to='firmas/', null=True, blank=True, verbose_name="Firma")
    
    #def clean_cuit(self):
    #    if not (0 < self.cleaned_data['models.IntegerField(verbose_name="Cantidad")_documento'] <= 99999999999):
    #        raise ValidationError("El documento debe ser un models.IntegerField(verbose_name="Cantidad") positivo de 11 digitos válidos")
    #    return self.cleaned_data['models.IntegerField(verbose_name="Cantidad")_documento']

    def clean(self):
        if self.firma:
            width, height = get_image_dimensions(self.firma)
            if width > 500 or height > 500:
                raise ValidationError("La firma no puede tener más de 500x500 píxeles.")    

    #class Meta:
    #    abstract = True


class Operador(Persona):
    models.IntegerField(verbose_name="Cantidad")_operador = models.IntegerField(verbose_name="Operador")


# class Contacto(Persona):



class Domicilio(models.Model):
    tipo = models.CharField(max_length=30, verbose_name="Tipo de Domicilio")
    direccion = models.CharField(max_length=100, verbose_name="Dirección")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo}: {self.direccion}"


class Telefono(models.Model):
    tipo = models.CharField(max_length=30, verbose_name="Tipo de Teléfono")
    models.IntegerField(verbose_name="Cantidad")_telefono = models.CharField(max_length=15, verbose_name="Número de Teléfono")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo}: {self.models.IntegerField(verbose_name="Cantidad")_telefono}"


class Perfil(models.Model):
    informacion_adicional = models.TextField(verbose_name="Información Adicional")
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"Perfil de {self.persona}"


class Prospec(models.Model):
    razon_social = models.CharField(max_length=30, verbose_name="Razón Social", default=0)
    nombre_fantasia = models.CharField(max_length=30, verbose_name="Nombre de Fantasía", default=0)
    estado = models.CharField(max_length=10, verbose_name="Estado", default=0)
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


class SubRubro(models.Model):
    subrubro = models.CharField(max_length=255, verbose_name="Subrubro",default=0)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)


class Prospecto(Prospec):
    models.IntegerField(verbose_name="Cantidad")_prospecto = models.IntegerField(verbose_name="Prospecto", default=0)
    contactado = models.CharField(null=True, max_length=100, verbose_name="Contactado")
    fecha_ultimo_contacto = models.DateField(null=True, verbose_name="Fecha de último contacto")
    cliente = models.IntegerField(null=True, verbose_name="Cliente")
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, default=1)
    subrubro = models.ForeignKey(SubRubro, on_delete=models.CASCADE, default=1) 


class Proveedor(Prospec):
    models.IntegerField(verbose_name="Cantidad")_proveedor = models.IntegerField(verbose_name="Proveedor", default=0)   


class Presupuesto(models.Model):
    models.IntegerField(verbose_name="Cantidad")_presupuesto = models.IntegerField(verbose_name="Presupuesto")
    fecha = models.DateField(verbose_name="Fecha")
    condicion_de_pago = models.CharField(max_length=250, verbose_name="Condición de pago")
    validez = models.CharField(max_length=150, null=True, verbose_name="Validez")
    plazo_de_entrega = models.CharField(max_length=250, null=True, verbose_name="Plazo de entrega")
    tipo_de_cambio = models.CharField(max_length=250, verbose_name="Tipo de cambio")
    observacion = models.CharField(max_length=250, verbose_name="Observación")
    models.IntegerField(verbose_name="Cantidad")_operador = models.IntegerField(verbose_name="Operador")
    estado_del_presupuesto = models.CharField(max_length=30, verbose_name="Estado del presupuesto")
    contacto = models.CharField(max_length=150, verbose_name="Nombre del contacto")
    fecha_dias_habiles = models.DateField(verbose_name="Fecha días hábiles")
    total_neto = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Total neto")
    cliente = models.ManyToManyField(Prospecto)


class PresupuestoDetalle(models.Model):
    codigo_de_producto = models.CharField(max_length=13, null=True, verbose_name="Código de producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    descripcion = models.CharField(max_length=250, null=True, verbose_name="Descripción del producto")
    monto = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Monto")
    moneda = models.CharField(max_length=3, choices=[("USD", "u$s"), ("ARS", "$")], default="USD", verbose_name="Moneda")
    tipo_de_unidad = models.CharField(max_length=10, choices=[("p/millar", "millar"), ("p/unidad", "unidad"), ("precio", "precio")], default="p/millar", verbose_name="Tipo de unidad")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Subtotal")
    proveedor_ppto = models.IntegerField(verbose_name="Provvedor ppto.")
    fecha_ppto_proveedor = models.DateField(verbose_name="Fecha ppto.")
    tipo_de_cambio = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Tipo de cbio ppto.")
    presupuesto_models.IntegerField(verbose_name="Cantidad") = models.ForeignKey (Presupuesto, on_delete=models.CASCADE)



class Registracion(models.Model):
    fecha = models.DateField(verbose_name="Fecha de registracion")
    models.IntegerField(verbose_name="Cantidad")_prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE)



    
