from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .models import Familia, Articulo, Material, Producto
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
    class Meta:
        model = Producto
        fields = '__all__'

class ActualizarStockForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_de_producto', 'stockactual', 'stockreservado', 'stockdisponible']