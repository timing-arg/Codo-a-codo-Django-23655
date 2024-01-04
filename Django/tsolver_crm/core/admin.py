from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.http.request import HttpRequest
from core.models import Producto, Persona, Operador, Domicilio, Telefono, Perfil, Prospec, Rubro, Subrubro, Prospecto, Proveedor, Presupuesto, PresupuestoDetalle, Registracion



class TsolverAdminSite(admin.AdminSite):
    site_header = "Sistema de Administración de tisol 1.0"
    site_title = "Administración para superusers"
    index_title = "Administración del sitio"
    empty_value_display = "vacio"



class PersonaAdmin(admin.ModelAdmin):
    list_display = ( 'tipo_documento', 'documento', 'nombre', 'apellido')
    list_editable = ('apellido', 'nombre')
    list_display_links = ['documento']
    search_fields = ['apellido']



#class ProductoAdmin(admin.ModelAdmin):
#    list_display = ( 'codigo_de_producto', 'descripcion', 'formato', 'existencia')
#    list_editable = ('descripcion')
#    list_display_links = ['codigo_de_producto']
#    search_fields = ['descripcion']



@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field == 'estudiantes':
            kwargs["queryset"] = Estudiante.objects.filter().order_by("apellido")

        return super().formfield_for_manytomany(db_field, request, **kwargs)



sitio_admin = TsolverAdminSite(name='administrador')
sitio_admin.register(Persona, PersonaAdmin)
#sitio_admin.register(Producto, ProductoAdmin)
#sitio_admin.register(Operador, OperadorAdmin)
#sitio_admin.register(Domicilio, DomicilioAdmin)
#sitio_admin.register(Telefono, TelefonoAdmin)
#sitio_admin.register(Perfil, PerfilAdmin)
#sitio_admin.register(Prospec, ProspecAdmin)
#sitio_admin.register(Rubro, RubroAdmin)
#sitio_admin.register(Subrubro, SubrubroAdmin) 
#sitio_admin.register(Prospecto, SubrubroAdmin)
#sitio_admin.register(Proveedor, ProveedorAdmin)
#sitio_admin.register(Presupuesto, PresupuestoAdmin) 
#sitio_admin.register(PresupuestoDetalla, PresupuestoDetallaAdmin)
#sitio_admin.register(Registracion, RegistracionAdmin)
#sitio_admin.register(Docente, DocenteAdmin)
#sitio_admin.register(Categoria, CategoriaAdmin)
#sitio_admin.register(Inscripcion, InscripcionAdmin)


#admin.site.register(Estudiante, EstudianteAdmin)
#admin.site.register(Docente)
#admin.site.register(Categoria)
#admin.site.register(Inscripcion)
#admin.site.register(Curso)