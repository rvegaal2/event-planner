"""
Módulo: users/views.py
Aplicación: users
Descripción: Vistas para el registro de usuarios en la plataforma Event Planner.

Autor: Equipo Event Planner
Versión: 1.0.0
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroUsuarioForm


def registro(request):
    """
    Vista para el registro de nuevos usuarios en la plataforma.

    Maneja el formulario de registro que permite crear cuentas con
    dos roles posibles: cliente o proveedor.

    Flujo:
        - GET:  Renderiza el formulario vacío de registro.
        - POST: Valida el formulario; si es válido, crea el usuario,
                inicia sesión automáticamente y redirige al listado
                de servicios. Si no es válido, re-renderiza el formulario
                con los errores correspondientes.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.
            - request.method (str): Método HTTP ('GET' o 'POST').
            - request.POST (QueryDict): Datos enviados por el formulario.

    Returns:
        HttpResponse: Respuesta HTTP con el template renderizado.
            - En GET o POST inválido: template 'users/registro.html'
              con el formulario en el contexto.
            - En POST válido: redirección HTTP 302 a 'lista_servicios'.

    Raises:
        No lanza excepciones directas; los errores de validación
        son manejados internamente por Django Forms.

    Ejemplo de uso (POST exitoso):
        Datos enviados:
            email=usuario@ejemplo.com
            tipo_usuario=proveedor
            password1=MiPassword123!
            password2=MiPassword123!
        Resultado:
            - Usuario creado con es_proveedor=True
            - Sesión iniciada
            - Redirección a /services/

    Template:
        users/registro.html

    Contexto del template:
        form (RegistroUsuarioForm): Instancia del formulario, con o sin errores.
    """
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_servicios')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'users/registro.html', {'form': form})
