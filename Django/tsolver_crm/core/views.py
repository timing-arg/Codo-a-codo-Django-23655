from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import ContactoForm, AltaPersonaForm , AltaProspectoForm
from .models import Prospecto


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
