🎉 Event Planner Platform

Aplicación web diseñada para centralizar, optimizar y digitalizar el ecosistema de organizadores de eventos en Colombia, conectando organizadores, proveedores y asistentes en una sola plataforma.


🚀 Descripción del Proyecto

Actualmente, el gremio de event planners opera de forma fragmentada mediante grupos de WhatsApp y Facebook, lo que genera:

Desorganización en la comunicación
Baja visibilidad de servicios
Dificultad para encontrar proveedores
Procesos manuales poco eficientes

Este proyecto propone una solución tipo marketplace inspirada en modelos como Airbnb, enfocada en:

Oferta y demanda de servicios de eventos
Gestión integral de eventos
Comunicación directa entre actores


🎯 Objetivo

Desarrollar una aplicación web que permita:

Facilitar la búsqueda y contratación de servicios
Mejorar la comunicación entre usuarios
Optimizar la gestión logística de eventos


🧩 Funcionalidades Principales

👤 Gestión de Usuarios
Registro y autenticación (JWT)
Roles:
Organizadores
Clientes (visitantes)
Colaboradores (RBAC)
📅 Gestión de Eventos
Crear, editar, duplicar y eliminar eventos
Publicar / ocultar eventos
Generación de Landing Page personalizada
Control de visibilidad
👥 Gestión de Asistentes
Registro manual de asistentes
Listado y exportación
Confirmación de asistencia (check-in)
🔍 Búsqueda y Descubrimiento
Página pública de eventos
Filtros por:
Categoría
Fecha
Ubicación
Motor de búsqueda por palabras clave
💬 Sistema de Chat
Comunicación en tiempo real
Bandeja de mensajes
Notificaciones
Bloqueo de usuarios
Archivado de conversaciones
🤝 Gestión de Terceros
Registro de clientes y proveedores
Asociación a eventos
Gestión de cotizaciones
Generación de presupuestos (PDF)


🏗️ Arquitectura
Enfoque
Arquitectura monolítica
Framework principal: Django
Componentes
Frontend
Django Templates + HTMX
HTML, CSS, JavaScript
Backend
Django (Python)
API REST
Base de Datos
Producción: PostgreSQL
Desarrollo: SQLite
Infraestructura
Despliegue: Render
Soporte para:
WebSockets (Django Channels)
Redis (chat en tiempo real)


⚙️ Requisitos No Funcionales Clave
⏱️ Tiempo de respuesta < 2s
🔐 Autenticación segura con JWT
🔑 Control de acceso (RBAC)
🔒 Cifrado de datos (TLS)
📈 Soporte para alta concurrencia (chat)
📱 Diseño responsive
💾 Backups diarios
🇨🇴 Cumplimiento Ley 1581 de 2012
🧪 Metodología de Desarrollo


Se utiliza Scrum con:

Sprints semanales
Roles:
Product Owner
Scrum Master
Equipo de desarrollo
Herramientas
GitHub (control de versiones)
Trello (gestión de tareas)
Notion (documentación)
Slack (comunicación)
Google Meet (reuniones)


📈 Beneficios Esperados
Centralización del gremio
Mayor visibilidad comercial
Reducción de tiempos operativos
Formalización del sector
Escalabilidad a otras ciudades


👥 Stakeholders
Organizadores de eventos
Clientes (asistentes)
Proveedores
Administradores de plataforma
Entidades regulatorias


🔄 Flujo de Trabajo
Uso de ramas por desarrollador
Pull Requests para integración
Validación con ESLint y Prettier


📚 Referencias
Ley 1581 de 2012 (Protección de Datos - Colombia)
Scrum Framework
Documentación oficial de Django


Equipo de desarrollo:

Nicolas Cueca
Oscar Hernández
Rafael Vega
Alex Guayabo