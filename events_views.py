"""
Módulo: events/views.py
Aplicación: events
Descripción: Vistas para la gestión de servicios de eventos en la plataforma Event Planner.

Provee las vistas para listar todos los servicios disponibles públicamente
y para que los proveedores autenticados creen nuevos servicios.

Autor: Equipo Event Planner
Versión: 1.0.0
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Servicio
from .forms import ServicioForm


def lista_servicios(request):
    """
    Vista pública que muestra el listado de todos los servicios disponibles.

    No requiere autenticación. Recupera todos los objetos Servicio
    de la base de datos y los pasa al template para su visualización.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.

    Returns:
        HttpResponse: Renderiza el template 'events/lista_servicios.html'
            con el queryset completo de servicios.

    Contexto del template:
        servicios (QuerySet[Servicio]): Todos los servicios registrados
            en la base de datos, sin filtros.

    Ejemplo de consulta SQL generada (ORM Django):
        SELECT * FROM events_servicio;

    Template:
        events/Lista_servicios.html

    URL:
        /services/  →  name='lista_servicios'
    """
    servicios = Servicio.objects.all()
    return render(request, 'events/lista_servicios.html', {'servicios': servicios})


@login_required
def crear_servicio(request):
    """
    Vista protegida para que los proveedores creen nuevos servicios.

    Requiere que el usuario esté autenticado (`@login_required`).
    Adicionalmente, verifica que el usuario tenga el rol de proveedor
    (`es_proveedor=True`). Si el usuario es cliente, redirige al listado.

    Flujo:
        - Sin autenticación: redirige automáticamente a la URL de login.
        - Autenticado como cliente: redirige a 'lista_servicios'.
        - GET (proveedor): renderiza el formulario vacío.
        - POST válido (proveedor): guarda el servicio asignando el
          usuario actual como proveedor y redirige al listado.
        - POST inválido: re-renderiza el formulario con errores.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP de Django.
            - request.user (Usuario): Usuario autenticado actualmente.
            - request.method (str): Método HTTP ('GET' o 'POST').
            - request.POST (QueryDict): Datos del formulario en POST.

    Returns:
        HttpResponse:
            - Redirección 302 a 'lista_servicios' si el usuario es cliente.
            - Template 'events/crear_servicio.html' con el formulario (GET o POST inválido).
            - Redirección 302 a 'lista_servicios' si el servicio fue creado exitosamente.

    Raises:
        No lanza excepciones directas. Los errores de validación
        son capturados por Django Forms.

    Ejemplo de uso (POST exitoso):
        Usuario autenticado: proveedor@ejemplo.com (es_proveedor=True)
        Datos enviados:
            nombre=Fotografía para bodas
            descripcion=Cobertura completa del evento
            categoria=Fotografía
            ciudad=Bogotá
            precio_referencia=1500000
            telefono_contacto=3001234567
        Resultado:
            - Servicio creado con proveedor=request.user
            - Redirección a /services/

    Nota:
        El campo `proveedor` del modelo Servicio NO se incluye en el formulario
        (ServicioForm). Se asigna manualmente con `servicio.proveedor = request.user`
        antes de guardar en base de datos.

    Decoradores:
        @login_required: Redirige a LOGIN_URL si el usuario no está autenticado.

    Template:
        events/crear_servicio.html

    Contexto del template:
        form (ServicioForm): Formulario con o sin errores de validación.

    URL:
        /services/crear/  →  name='crear_servicio'
    """
    if not request.user.es_proveedor:
        return redirect('lista_servicios')

    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.proveedor = request.user
            servicio.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm()

    return render(request, 'events/crear_servicio.html', {'form': form})
