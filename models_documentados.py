"""
Módulo: users/models.py
Aplicación: users
Descripción: Modelos de usuario personalizados para la plataforma Event Planner.

Reemplaza el modelo de usuario estándar de Django por uno basado en
email como identificador principal, con soporte para roles de cliente y proveedor.

Autor: Equipo Event Planner
Versión: 1.0.0
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario.

    Sobrescribe BaseUserManager para utilizar email como campo
    de autenticación principal en lugar de username.

    Métodos:
        create_user: Crea un usuario estándar.
        create_superuser: Crea un superusuario con permisos de administrador.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el email y contraseña dados.

        Args:
            email (str): Dirección de correo electrónico del usuario.
                         Debe ser única en la base de datos.
            password (str, optional): Contraseña en texto plano.
                                      Se almacena como hash. Default: None.
            **extra_fields: Campos adicionales del modelo Usuario
                            (ej. es_proveedor, es_cliente).

        Returns:
            Usuario: Instancia del usuario recién creado y guardado.

        Raises:
            ValueError: Si el email no es proporcionado.

        Ejemplo:
            >>> usuario = Usuario.objects.create_user(
            ...     email='cliente@ejemplo.com',
            ...     password='MiPassword123!'
            ... )
        """
        if not email:
            raise ValueError('El usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos de staff y superuser.

        Utilizado por el comando `python manage.py createsuperuser`.

        Args:
            email (str): Correo electrónico del superusuario.
            password (str, optional): Contraseña en texto plano. Default: None.
            **extra_fields: Campos adicionales. Se fuerzan:
                            is_staff=True, is_superuser=True.

        Returns:
            Usuario: Instancia del superusuario creado.

        Ejemplo:
            >>> admin = Usuario.objects.create_superuser(
            ...     email='admin@eventplanner.com',
            ...     password='AdminPass123!'
            ... )
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para la plataforma Event Planner.

    Extiende AbstractUser eliminando el campo `username` y usando
    el `email` como identificador principal de autenticación.
    Agrega campos de rol para distinguir entre clientes y proveedores.

    Attributes:
        username (None): Campo deshabilitado. El email cumple su función.
        email (EmailField): Correo electrónico único. Campo de autenticación principal.
        es_proveedor (BooleanField): True si el usuario puede publicar servicios.
                                     Default: False.
        es_cliente (BooleanField): True si el usuario es un cliente/asistente.
                                   Default: True.
        objects (UsuarioManager): Manager personalizado para creación de usuarios.

    Meta:
        USERNAME_FIELD = 'email': Define el email como campo de login.
        REQUIRED_FIELDS = []: Sin campos adicionales obligatorios en createsuperuser.

    Tabla en BD:
        users_usuario

    Ejemplo de uso:
        >>> # Verificar si un usuario puede publicar servicios
        >>> if usuario.es_proveedor:
        ...     # Mostrar botón "Crear servicio"
        ...     pass

        >>> # Obtener todos los proveedores activos
        >>> proveedores = Usuario.objects.filter(es_proveedor=True, is_active=True)

    Relaciones:
        - Servicio.proveedor → ForeignKey → Usuario
          Un usuario proveedor puede tener múltiples servicios.
    """
    username = None

    email = models.EmailField(unique=True)

    es_proveedor = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()


# ─────────────────────────────────────────────────────────────
# Módulo: events/models.py
# ─────────────────────────────────────────────────────────────

"""
Módulo: events/models.py
Aplicación: events
Descripción: Modelos para la gestión de servicios de eventos.

Define el modelo Servicio que representa una oferta publicada
por un proveedor en la plataforma marketplace.

Autor: Equipo Event Planner
Versión: 1.0.0
"""

from django.db import models
from django.conf import settings


class Servicio(models.Model):
    """
    Modelo que representa un servicio ofrecido por un proveedor de eventos.

    Los servicios son publicados por usuarios con rol proveedor (`es_proveedor=True`)
    y son visibles públicamente en el listado de la plataforma.

    Attributes:
        proveedor (ForeignKey → Usuario): Usuario proveedor que publica el servicio.
            Al eliminar el usuario, se eliminan en cascada todos sus servicios.
        nombre (CharField): Nombre descriptivo del servicio. Máximo 150 caracteres.
        descripcion (TextField): Descripción detallada del servicio ofrecido.
        categoria (CharField): Categoría del servicio (ej. Fotografía, Catering).
                               Máximo 100 caracteres.
        ciudad (CharField): Ciudad donde se presta el servicio. Máximo 100 caracteres.
        precio_referencia (DecimalField): Precio orientativo en COP.
                                          Hasta 10 dígitos, 2 decimales.
        telefono_contacto (CharField): Número de contacto del proveedor.
                                       Máximo 20 caracteres.
        activo (BooleanField): Controla la visibilidad del servicio. Default: True.
        fecha_creacion (DateTimeField): Timestamp de creación. Se asigna automáticamente.

    Tabla en BD:
        events_servicio

    Ejemplo de creación:
        >>> from users.models import Usuario
        >>> from events.models import Servicio
        >>> proveedor = Usuario.objects.get(email='foto@ejemplo.com')
        >>> servicio = Servicio.objects.create(
        ...     proveedor=proveedor,
        ...     nombre='Fotografía para bodas',
        ...     descripcion='Cobertura completa, álbum digital incluido.',
        ...     categoria='Fotografía',
        ...     ciudad='Bogotá',
        ...     precio_referencia=1500000.00,
        ...     telefono_contacto='3001234567'
        ... )

    Ejemplo de consulta:
        >>> # Todos los servicios activos en Bogotá
        >>> Servicio.objects.filter(activo=True, ciudad='Bogotá')

    Relaciones:
        - proveedor → users.Usuario (ForeignKey, CASCADE)
    """
    proveedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)

    precio_referencia = models.DecimalField(max_digits=10, decimal_places=2)
    telefono_contacto = models.CharField(max_length=20)

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Representación legible del servicio.

        Returns:
            str: Nombre del servicio.

        Ejemplo:
            >>> str(servicio)
            'Fotografía para bodas'
        """
        return self.nombre
