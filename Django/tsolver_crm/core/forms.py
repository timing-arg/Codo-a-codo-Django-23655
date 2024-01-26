from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from .models import Familia, Articulo, Material, Producto
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

import re

CUIT_REGEX = r'^\d{2}-\d{8}-\d{1}$'


class BlueBackgroundTextInput(forms.TextInput):
    class Media:
        CSS = {'all': ('core/css/blue_background_text_input.css',)}


class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto", widget=BlueBackgroundTextInput, required=True)
    apellido =forms.CharField(label="Apellido de contacto", widget=forms.TextInput(attrs={'class': 'fondo_rojo'}), required=True)
    edad = forms.IntegerField(label="Edad")
    dni = forms.IntegerField(label="DNI")
    mail = forms.EmailField(label="Mail", required=True)
    mensaje =  forms.CharField(widget=forms.Textarea)

    def clean_edad(self):
        if self.cleaned_data["edad"] < 18:
            raise ValidationError("El usuario no puede tener menos de 18 años")
        
        return self.cleaned_data["edad"]

    def clean(self):
        # Este if simula una busqueda en la base de datos
        if self.cleaned_data["nombre"] == "Carlos" and self.cleaned_data["apellido"] == "Lopez":
            raise ValidationError("El usuario Carlos Lopez ya existe")
        
        # Si el usuario no existe lo damos de alta

        return self.cleaned_data
    

class AltaPersonaForm(forms.Form):
    nombre = forms.CharField(label="Nombre del prospecto", required=True)
    apellido =forms.CharField(label="Apellido del prospecto", required=True)
    dni = forms.IntegerField(label="DNI", required=True)
    email = forms.EmailField(label="email", required=True)
    legajo = forms.CharField(label="Legajo", required=True)


class AltaProspectoForm(forms.Form):
    razon_social = forms.CharField(label="Razón Social", required=True)
    nombre_fantasia = forms.CharField(label="Nombre de Fantasía", required=False)
    estado = forms.CharField(label="Estado", required=True)
    cuit = forms.CharField(label="CUIT", required=True)
    numero_prospecto = forms.IntegerField(label="Prospecto")
    contactado = forms.CharField(label="Contactado")
    fecha_ultimo_contacto = forms.DateField(label="Fecha de último contacto")
    cliente = forms.CharField(label="Cliente")
    rubro = forms.CharField(label="Rubro",required=True)
    subrubro = forms.CharField(label="SubRubro",required=True)



    def clean(self):
        cleaned_data = super().clean()
        cuit = cleaned_data.get('cuit')

        # Validar el formato del CUIT
        if not re.match(CUIT_REGEX, cuit):
            raise ValidationError("El CUIT no tiene un formato válido.")

    def nombre_completo(self):
        razon_social = self.cleaned_data.get('razon_social', '')
        nombre_fantasia = self.cleaned_data.get('nombre_fantasia', '')
        return f"{razon_social} {nombre_fantasia}"

class Prospecto(forms.Form):
    numero_prospecto = forms.IntegerField(label="Prospecto")
    contactado = forms.CharField(label="Contactado")
    fecha_ultimo_contacto = forms.DateField(label="Fecha de último contacto")
    cliente = forms.CharField(label="Cliente")
    rubro = forms.CharField(label="Rubro")
    subrubro = forms.CharField(label="SubRubro")

class CrearProductoForm(forms.ModelForm):
    codigo_de_producto=forms.CharField(label='Código de producto', required=True, min_length=13, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código de 13 dígitos'}))
    descripcion=forms.CharField(label='Descripción', required=True, min_length=1, max_length=255,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción del producto'}))
    formato=forms.CharField(label='Formato', required=False, min_length=1, max_length=40,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Formato'}))
    anchoXlongitud=forms.CharField(label='Ancho x longitud', required=False, min_length=1, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'p.ej.:50x80'}))
    ancho=forms.DecimalField(label='Ancho', required=False, min_value=0.01, max_value=999.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'p.ej.:50'}))
    longitud=forms.DecimalField(label='Longitud', required=False, min_value=0.01, max_value=999.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'p.ej.:80'}))
    buje=forms.CharField(label='Buje', required=False, min_length=1, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'p.ej.:Buje de 40 mm'}))
    codigo=forms.CharField(label='Código', required=False, min_length=1, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código'}))
    minimo=forms.IntegerField(label='Mínimo', required=False, min_value=1, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mínimo'}))
    stockmin=forms.IntegerField(label='Stock mínimo', required=False, min_value=1, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stock mínimo'}))
    stockmax=forms.IntegerField(label='Stock máximo', required=False, min_value=1, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stock máximo'}))
    existencia=forms.IntegerField(label='Existencia', required=False, min_value=1, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Existencia'}))
    tiempo_de_reposicion=forms.CharField(label='Tiempo de reposición', required=False, min_length=1, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tiempo de reposición'}))
    moneda=forms.CharField(label='Moneda', required=True, min_length=1, max_length=3,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Moneda'}))
    iva=forms.IntegerField(label='IVA porciento', required=True, min_value=0.01, max_value=99.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'IVA porciento'}))
    precio_de_venta=forms.DecimalField(label='Precio de venta', required=False, min_value=0.01, max_value=10000000.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Precio de venta'}))
    es_accesorio=forms.CharField(label='Es accesorio?', required=False, min_length=1, max_length=50,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Si o No'}))
    codigo_de_origen=forms.CharField(label='Código de origen', required=True, min_length=1, max_length=13,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código de origen'}))
    tipo_de_unidad=forms.CharField(label='Tipo de unidad', required=True, min_length=1, max_length=10,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tipo de unidad'}))
    utilidad=forms.DecimalField(label='Utilidad', required=False, min_value=0.01, max_value=10000000.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Utilidad'}))
    precio_de_costo=forms.DecimalField(label='Precio de costo', required=False, min_value=0.01, max_value=10000000.00,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Precio de costo'}))
    idcliente=forms.IntegerField(label='Cliente número', required=False, min_value=0, max_value=999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cliente número'}))
    fecha_ultima_actualizacion=forms.DateField(label='Fecha de última actualización', required=False,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fecha de última actualización'}))
    stockactual=forms.IntegerField(label='Stock actual', required=False, min_value=0, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stock actual'}))
    stockreservado=forms.IntegerField(label='Stock reservado', required=False, min_value=0, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stock reservado'}))
    stockdisponible=forms.IntegerField(label='Stock disponible', required=False, min_value=0, max_value=9999999,
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Stock disponible'}))
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all())
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    
    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CrearProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('codigo_de_producto', css_class='custom-class'),
            Field('descripcion', rows=4, css_class='custom-class'),
            Field('formato', css_class='custom-class'),
            Field('anchoXlongitud', css_class='custom-class'),
            Field('ancho', css_class='custom-class'),
            Field('longitud', css_class='custom-class'),
            Field('buje', css_class='custom-class'),
            Field('codigo', css_class='custom-class'),
            Field('minimo', css_class='custom-class'),
            Field('stockmin', css_class='custom-class'),
            Field('stockmax', css_class='custom-class'),
            Field('existencia', css_class='custom-class'),
            Field('tiempo_de_reposicion', min=0),
            Field('moneda', css_class='custom-class'),
            Field('iva', css_class='custom-class'),
            Field('precio_de_venta', css_class='custom-class'),
            Field('es_accesorio', css_class='custom-class'),
            Field('codigo_de_origen', css_class='custom-class'),
            Field('tipo_de_unidad', css_class='custom-class'),
            Field('utilidad', css_class='custom-class'),
            Field('precio_de_costo', css_class='custom-class'),
            Field('idcliente', css_class='custom-class'),
            Field('fecha_ultima_actualizacion', css_class='custom-class'),
            Field('stockactual', css_class='custom-class'),
            Field('stockreservado', css_class='custom-class'),
            Field('stockdisponible', css_class='custom-class'),
            Field('articulo', css_class='custom-class'),
            Field('material', css_class='custom-class'),

        )


class ActualizarStockForm(forms.ModelForm):
    codigo_de_producto = forms.CharField(label='Código de producto', required=True, min_length=13, max_length=13,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código de 13 dígitos'}))

    # ... otros campos

    class Meta:
        model = Producto
        fields = ['codigo_de_producto', 'stockactual', 'stockreservado', 'stockdisponible']

    def clean_codigo_de_producto(self):
        # Puedes personalizar la validación aquí si es necesario
        return self.cleaned_data['codigo_de_producto']




class SeleccionarProductoForm(forms.Form):
    familia = forms.ModelChoiceField(queryset=Familia.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.none(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))
    material = forms.ModelChoiceField(queryset=Material.objects.none(), empty_label=None, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super(SeleccionarProductoForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].queryset = Articulo.objects.none()
        self.fields['material'].queryset = Material.objects.none()

        if 'familia' in self.data:
            try:
                familia_id = int(self.data.get('familia'))
                self.fields['articulo'].queryset = Articulo.objects.filter(familia_id=familia_id)
            except (ValueError, TypeError):
                pass
        if 'articulo' in self.data:
            try:
                articulo_id = int(self.data.get('articulo'))
                self.fields['material'].queryset = Material.objects.filter(articulo_id=articulo_id)
            except (ValueError, TypeError):
                pass
