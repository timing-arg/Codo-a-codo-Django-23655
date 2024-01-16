from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, Http404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from datetime import datetime
from .forms import ContactoForm, AltaPersonaForm , AltaProspectoForm, ActualizarStockForm, CrearProductoForm
from .models import Persona, Prospecto, Producto
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db import IntegrityError
from rest_framework import viewsets, permissions
from .serializers import PersonaSerializer
from datetime import time, timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404



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

    else: # GET
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
                nombre = alta_prospecto_form.cleaned_data['nombre'],
                apellido = alta_prospecto_form.cleaned_data['apellido'],
                dni = alta_prospecto_form.cleaned_data['dni'],
                email = alta_prospecto_form.cleaned_data['email'],
                legajo = alta_prospecto_form.cleaned_data['legajo'],

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
                razon_social = alta_prospecto_form.cleaned_data['razon_social'],
                nombre_fantasia = alta_prospecto_form.cleaned_data['nombre_fantasia'],
                estado = alta_prospecto_form.cleaned_data['estado'],
                cuit = alta_prospecto_form.cleaned_data['cuit'],
                cliente = alta_prospecto_form.cleaned_data['cliente'],
                rubro = alta_prospecto_form.cleaned_data['rubro'],
                subrubro = alta_prospecto_form.cleaned_data['subrubro'],
                
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
        crear_producto_form = CrearProductoForm(request.POST)  # Corregido aquí

        if crear_producto_form.is_valid():
            nuevo_producto = Producto(
                codigo_de_producto=crear_producto_form.cleaned_data['codigo_de_producto'],  # Corregido aquí
                descripcion=crear_producto_form.cleaned_data['descripcion'],
                formato=crear_producto_form.cleaned_data['formato'],
                anchoXlongitud=crear_producto_form.cleaned_data['anchoXlongitud'],
                ancho=crear_producto_form.cleaned_data['ancho'],
                longitud=crear_producto_form.cleaned_data['longitud'],
                buje=crear_producto_form.cleaned_data['buje'],
                codigo=crear_producto_form.cleaned_data['codigo'],
                minimo=crear_producto_form.cleaned_data['minimo'],
                stockmin=crear_producto_form.cleaned_data['stockmin'],
                stockmax=crear_producto_form.cleaned_data['stockmax'],
                existencia=crear_producto_form.cleaned_data['existencia'],
                tiempo_de_reposicion=crear_producto_form.cleaned_data['tiempo_de_reposicion'],
                moneda=crear_producto_form.cleaned_data['moneda'],
                iva=crear_producto_form.cleaned_data['iva'],
                precio_de_venta=crear_producto_form.cleaned_data['precio_de_venta'],
                es_accesorio=crear_producto_form.cleaned_data['es_accesorio'],
                codigo_de_origen=crear_producto_form.cleaned_data['codigo_de_origen'],
                tipo_de_unidad=crear_producto_form.cleaned_data['tipo_de_unidad'],
                utilidad=crear_producto_form.cleaned_data['utilidad'],
                precio_de_costo=crear_producto_form.cleaned_data['precio_de_costo'],
                idcliente=crear_producto_form.cleaned_data['idcliente'],
                fecha_ultima_actualizacion=crear_producto_form.cleaned_data['fecha_ultima_actualizacion'],
                stockactual=crear_producto_form.cleaned_data['stockactual'],
                stockreservado=crear_producto_form.cleaned_data['stockreservado'],
                stockdisponible=crear_producto_form.cleaned_data['stockdisponible'],
                articulo_id=crear_producto_form.cleaned_data['articulo_id'],
                material_id=crear_producto_form.cleaned_data['material_id'],
            )

            nuevo_producto.save()

            try:
                nuevo_producto.save()

            except IntegrityError as ie:
                messages.error(request, "Ocurrió un error al intentar dar de alta al producto")
                return redirect(reverse("listado_producto"))

            messages.info(request, "Producto dado de alta correctamente")
            return redirect(reverse("listado_producto"))
    else:
        crear_producto_form = CrearProductoForm()  # Corregido aquí

    context['crear_producto_form'] = crear_producto_form  # Corregido aquí

    return render(request, 'core/crear_producto.html', context)




def editar_producto(request, codigo_de_producto):
    producto = get_object_or_404(Producto, codigo_de_producto=codigo_de_producto)

    if request.method == "POST":
        form = CrearProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
            return redirect('ver_productos')  # Cambia 'lista_de_productos' con el nombre de tu vista de lista
        else:
            messages.error(request, "Error en el formulario. Por favor, corrige los errores.")

    else:
        form = CrearProductoForm(instance=producto)

    context = {'form': form, 'producto': producto}
    return render(request, 'core/editar_producto.html', context)




@login_required
def eliminar_producto(request, codigo_de_producto):
    producto = get_object_or_404(Producto, codigo_de_producto=codigo_de_producto)

    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')  # Ajusta según tu aplicación

    return render(request, 'core/eliminar_producto.html', {'codigo_de_producto': codigo_de_producto})




@login_required
def seleccionar_producto(request):
    if request.method == 'POST':
        form = SeleccionarProductoForm(request.POST, producto_disponibles=request.session['productos_disponibles'])
        if form.is_valid():
            producto = form.cleaned_data['producto']
            turno.paciente = Paciente.objects.get(user=request.user)
            turno.save()
            return redirect('ver_productos', username=request.user.username)
    else:
        form = SeleccionarTurnoForm(turnos_disponibles=request.session['turnos_disponibles'])
    return render(request, 'core/seleccionar_turno.html', {'form': form})



def ver_productos(request):
    # Obtén la lista de productos desde la base de datos
    productos = Producto.objects.all()

    context = {
        'core_productos': productos,  # Pasa la lista de productos en el contexto
    }

    return render(request, 'core/ver_productos.html', context)




def actualizar_stock(request):
    if request.method == "POST":
        form = ActualizarStockForm(request.POST)
        print("aca estoy")
        if form.is_valid():
            try:
                codigo_de_producto = form.cleaned_data['codigo_de_producto']

                # Buscar el producto por su código
                producto = Producto.objects.get(codigo_de_producto=codigo_de_producto)

                # Prellenar el formulario con los valores actuales
                form = ActualizarStockForm(initial={
                    'stockactual': producto.stockactual,
                    'stockreservado': producto.stockreservado,
                    'stockdisponible': producto.stockdisponible,
                })

                if 'submit_actualizar' in request.POST:
                    # Si se envió el formulario para actualizar, actualiza el stock
                    form = ActualizarStockForm(request.POST)
                    if form.is_valid():
                        stockactual = form.cleaned_data['stockactual']
                        stockreservado = form.cleaned_data['stockreservado']
                        stockdisponible = form.cleaned_data['stockdisponible']

                        # Actualizar el stock del producto
                        producto.stockactual = stockactual
                        producto.stockreservado = stockreservado
                        producto.stockdisponible = stockdisponible
                        producto.save()

                        # Resto de la lógica...

                        messages.success(request, "Stock actualizado correctamente.")
                        return HttpResponseRedirect(reverse('nombre_de_tu_vista'))  # Redirige a la página deseada
                else:
                    # Si solo se ingresó el código de producto, muestra el formulario prellenado
                    return render(request, 'core/actualizar_stock.html', {'form': form, 'producto': producto})

            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado.")
            except IntegrityError as e:
                messages.error(request, f"Error de integridad: {e}")
        else:
            messages.error(request, "Formulario no válido.")
    else:
        form = ActualizarStockForm()

    context = {'form': form}
    return render(request, 'core/actualizar_stock.html', context)
