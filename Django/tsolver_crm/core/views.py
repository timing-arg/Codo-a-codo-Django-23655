from core.models import Persona, Prospecto, Producto, Articulo, Material
from .forms import ContactoForm, AltaPersonaForm, AltaProspectoForm, ActualizarStockForm, CrearProductoForm, SeleccionarProductoForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import time, timedelta
from .serializers import PersonaSerializer
from rest_framework import viewsets, permissions
from django.db import IntegrityError
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from datetime import datetime
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, Http404
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)


def index(request):
    context = {
        'nombre_usuario': 'Carlos Perez',
        'fecha': datetime.now(),
        'es_instructor': True,
    }
    return render(request, "core/index.html", context)


def contacto(request):
    if request.method == "POST":
        # Instanciamos un formulario con datos
        formulario = ContactoForm(request.POST)

        # Validarlo
        if formulario.is_valid():
            # Dar de alta la info

            messages.info(request, "Consulta enviada con éxito")

            # p1 = Estudiante(
            #     nombre=formulario.cleaned_data['nombre'],
            #     apellido=formulario.cleaned_data['apellido'],
            #     email=formulario.cleaned_data['mail'],
            #     dni=formulario.cleaned_data['dni'])
            # p1.save()

            return redirect(reverse("prospectos_listado"))

    else:  # GET
        formulario = ContactoForm()

    context = {
        'contacto_form': formulario
    }

    return render(request, "core/contacto.html", context)


def alta_personas(request):
    context = {}

    if request.method == "POST":
        alta_persona_form = AltaPersonaForm(request.POST)

        if alta_persona_form.is_valid():
            nuevo_persona = Persona(
                nombre=alta_prospecto_form.cleaned_data['nombre'],
                apellido=alta_prospecto_form.cleaned_data['apellido'],
                dni=alta_prospecto_form.cleaned_data['dni'],
                email=alta_prospecto_form.cleaned_data['email'],
                legajo=alta_prospecto_form.cleaned_data['legajo'],

            )

            nuevo_persona.save()

            messages.info(request, "Persona dada de alta correctamente")
            return redirect(reverse("personas_listado"))
    else:
        alta_persona_form = AltaPersonaForm()

    context['alta_persona_form'] = AltaPersonaForm

    return render(request, 'core/alta_persona.html', context)


def alta_prospectos(request):
    context = {}

    if request.method == "POST":
        alta_prospecto_form = AltaProspectoForm(request.POST)

        if alta_prospecto_form.is_valid():
            nuevo_prospecto = Prospecto(
                razon_social=alta_prospecto_form.cleaned_data['razon_social'],
                nombre_fantasia=alta_prospecto_form.cleaned_data['nombre_fantasia'],
                estado=alta_prospecto_form.cleaned_data['estado'],
                cuit=alta_prospecto_form.cleaned_data['cuit'],
                cliente=alta_prospecto_form.cleaned_data['cliente'],
                rubro=alta_prospecto_form.cleaned_data['rubro'],
                subrubro=alta_prospecto_form.cleaned_data['subrubro'],

            )

            nuevo_prospecto.save()

            messages.info(request, "Prospecto dado de alta correctamente")
            return redirect(reverse("prospectos_listado"))
    else:
        alta_prospecto_form = AltaProspectoForm()

    context['alta_prospecto_form'] = AltaProspectoForm

    return render(request, 'core/alta_prospecto.html', context)


def prospectos_listado(request):
    listado = Prospecto.objects.all().order_by('dni')
    context = {
        'nombre_usuario': 'Carlos Perez',
        'fecha': datetime.now(),
        'es_instructor': False,
        'listado_prospectos': listado,
        'cant_inscriptos': len(listado),
    }

    return render(request, 'core/prospectos_listado.html', context)


def prospecto_detalle(request, nombre_prospecto):
    return HttpResponse(
        f"""
        <h1>Bienvenid@ {nombre_prospecto} </h1>
        <p>Pagina Personal de usuario</p>
        """
    )


def prospectos_historico(request, year):
    return HttpResponse(f'<h1>Histórico de prospectos del año: {year}</h1>')


def prospectos_historico_2017(request):
    return HttpResponse('<h1>Histórico de presupuestos de clientes</h1>')


def prospectos_estado(request, estado):
    return HttpResponse(f'Filtrar prospectos por estado: {estado}')


def gestion_de_stock(request, stock):
    return HttpResponse(f'Filtrar stock: {stock}')


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


@login_required
def crear_producto(request):
    context = {}

    if request.method == "POST":
        crear_producto_form = CrearProductoForm(request.POST)

        if crear_producto_form.is_valid():
            nuevo_producto = crear_producto_form.save(commit=False)

            # Obtener los objetos de Articulo y Material
            articulo_obj = crear_producto_form.cleaned_data['articulo']
            material_obj = crear_producto_form.cleaned_data['material']

            # Asignar los objetos a los campos correspondientes
            nuevo_producto.articulo = articulo_obj
            nuevo_producto.material = material_obj

            try:
                nuevo_producto.save()
            except IntegrityError as ie:
                messages.error(
                    request, f"Ocurrió un error al intentar dar de alta al producto: {ie}")
                return redirect(reverse("ver_productos"))

            messages.info(request, "Producto dado de alta correctamente")
            return redirect(reverse("ver_productos"))

    else:
        crear_producto_form = CrearProductoForm()

    return render(request, 'core/crear_producto.html', {'form': crear_producto_form})


def obtener_producto(request, codigo_de_producto):
    try:
        producto = Producto.objects.get(codigo_de_producto=codigo_de_producto)
        data = {
            'descripcion': producto.descripcion,
            'stockactual': producto.stockactual,
            'stockreservado': producto.stockreservado,
            'stockdisponible': producto.stockdisponible,
        }

        return JsonResponse(data)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def editar_producto(request, codigo_de_producto):
    producto = get_object_or_404(
        Producto, codigo_de_producto=codigo_de_producto)

    if request.method == "POST":
        form = CrearProductoForm(request.POST, instance=producto)
        if form.is_valid():
            # Obtener la instancia de Articulo y Material antes de guardar el formulario
            articulo_instance = form.cleaned_data['articulo']
            material_instance = form.cleaned_data['material']
            # Asignar la instancia de Articulo al campo 'articulo'
            form.instance.articulo = articulo_instance
            # Asignar la instancia de Material al campo 'material'
            form.instance.material = material_instance

            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
            # Cambia 'lista_de_productos' con el nombre de tu vista de lista
            return redirect('ver_productos')
        else:
            messages.error(
                request, "Error en el formulario. Por favor, corrige los errores.")

    else:
        form = CrearProductoForm(instance=producto)

    context = {'form': form, 'producto': producto}
    return render(request, 'core/editar_producto.html', context)


@login_required
def eliminar_producto(request, codigo_de_producto):
    producto = get_object_or_404(
        Producto, codigo_de_producto=codigo_de_producto)

    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')  # Ajusta según tu aplicación

    return render(request, 'core/eliminar_producto.html', {'codigo_de_producto': codigo_de_producto})


@login_required
def seleccionar_producto(request):
    form = SeleccionarProductoForm()

    if request.method == 'POST':
        form = SeleccionarProductoForm(request.POST)

    return render(request, 'core/abm_articulos_y_productos.html', {'form': form})


@login_required
def cargar_opciones_articulos(request):
    familia_id = request.GET.get('idfamilia')
    # Corrige el nombre de la variable aquí
    articulos = Articulo.objects.filter(familia_id=familia_id)
    data = [{'id': articulo.idarticulo, 'descripcion': articulo.articulo_descripcion}
            for articulo in articulos]
    print(data)  # Agrega esta línea para imprimir en la consola del servidor Django
    return JsonResponse({'opciones': data})


def ver_productos(request):
    # Obtén la lista de productos desde la base de datos
    productos = Producto.objects.all()

    context = {
        'core_productos': productos,  # Pasa la lista de productos en el contexto
    }

    return render(request, 'core/ver_productos.html', context)


def actualizar_producto(request, codigo_de_producto):
    try:
        # Obtener el producto por su código
        producto = Producto.objects.get(codigo_de_producto=codigo_de_producto)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado.")
        return redirect(reverse("gestion_de_stock"))
    except Producto.MultipleObjectsReturned:
        messages.error(request, "Error: Múltiples productos encontrados.")
        return redirect(reverse("gestion_de_stock"))

    if request.method == "POST":
        form = ActualizarStockForm(request.POST, instance=producto)

        if form.is_valid():
            # Excluir campos específicos del formulario antes de la validación
            form.cleaned_data.pop('descripcion', None)
            form.cleaned_data.pop('codigo_de_producto', None)

            # Actualizar el stock del producto
            Producto.objects.filter(pk=producto.pk).update(**form.cleaned_data)

            messages.success(request, "Stock actualizado correctamente.")
            # Redirige a la página deseada
            return HttpResponseRedirect(reverse('gestion_de_stock'))

    else:
        form = ActualizarStockForm(instance=producto)

    context = {'form': form, 'producto': producto}
    return render(request, 'core/actualizar_stock.html', context)


def actualizar_stock(request):
    if request.method == "POST":
        form = ActualizarStockForm(request.POST)

        if form.is_valid():
            try:
                # Obtener el producto por su código
                producto = Producto.objects.get(
                    codigo_de_producto=form.cleaned_data['codigo_de_producto'])

                # Mostrar el formulario prellenado
                return render(request, 'core/actualizar_stock.html', {'form': form, 'producto': producto})

            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.")
            except Producto.MultipleObjectsReturned:
                messages.error(
                    request, "Error: Múltiples productos encontrados.")
            except IntegrityError as e:
                messages.error(request, f"Error de integridad: {e}")
        else:
            messages.error(request, "Formulario no válido.")
    else:
        form = ActualizarStockForm()

    context = {'form': form}
    return render(request, 'core/actualizar_stock.html', context)


def actualizar_stock_submit(request):
    if request.method == "POST":
        form = ActualizarStockForm(request.POST)
        if form.is_valid():
            try:
                if 'submit_buscar' in request.POST:
                    # Lógica para buscar el producto
                    logger.debug("Submit Buscar")
                    pass
                elif 'submit_actualizar' in request.POST:
                    # Lógica para actualizar el stock
                    logger.debug("Submit Actualizar")

                    # Obtener el producto por su código
                    codigo_de_producto = form.cleaned_data['codigo_de_producto']
                    producto = Producto.objects.get(
                        codigo_de_producto=codigo_de_producto)

                    # Actualizar el stock del producto directamente
                    producto.stockactual = form.cleaned_data['stockactual']
                    producto.stockreservado = form.cleaned_data['stockreservado']

                    # Calcular stockdisponible
                    producto.stockdisponible = producto.stockactual - producto.stockreservado

                    # Validar valores de stock, por ejemplo, no permitir números negativos
                    if producto.stockactual < 0 or producto.stockreservado < 0 or producto.stockdisponible < 0:
                        messages.error(
                            request, "Los valores de stock no pueden ser negativos.")
                    else:
                        producto.save()

                        messages.success(
                            request, "Stock actualizado correctamente.")
                        # Redirige a la página deseada
                        return HttpResponseRedirect(reverse('gestion_de_stock'))

            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.")
            except IntegrityError as e:
                messages.error(request, f"Error de integridad: {e}")
        else:
            # Si el formulario no es válido, manejar errores personalizados si es necesario
            # Puedes acceder a los errores del formulario con form.errors
            messages.error(
                request, "Formulario no válido. Revise los datos ingresados.")
    return HttpResponseRedirect(reverse('actualizar_stock'))
