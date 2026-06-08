# Architecture Decision Records (ADR)

Este documento recoge las decisiones arquitectónicas clave del proyecto.

---

## ADR-001: Uso de Django como framework full-stack monolítico

### Estado
Aceptado  
**Fecha:** 10 de abril  
**Autores:** Equipo de desarrollo  

### Contexto
El equipo tiene 4 desarrolladores y un presupuesto limitado para cumplir a cabalidad todos los requisitos funcionales y no funcionales de un sistema web full-stack para organizadores y visitantes de eventos.

### Decisión
Se adopta el framework **Django**, basado en Python, para el desarrollo full-stack de sistemas web.

El framework incluye:
- Django Templates para la construcción de interfaces
- HTMX para interacciones dinámicas
- Django Channels para WebSockets
- Integración con SendGrid para envío de correos

El sistema se implementa bajo una **arquitectura monolítica** en un único repositorio.

### Consecuencias

**Positivas:**
- Mayor velocidad de desarrollo  
- Integración continua más simple  
- Transaccionalidad ACID incluida en el ORM  

**Negativas:**
- Escalabilidad horizontal limitada  
- Frontend no desacoplado del backend  

### Alternativas descartadas

- **React / Angular:**  
  Requieren librerías adicionales, mayor complejidad y posibles conflictos de versiones.

- **Express.js:**  
  Mayor tiempo de desarrollo al separar frontend y backend.  
  No incluye protección automática contra CSRF, XSS o inyecciones SQL.

- **API Gateway:**  
  Introduce latencia adicional que afecta funcionalidades en tiempo real.

---

## ADR-002: Uso de PostgreSQL en producción y SQLite en desarrollo

### Estado
Aceptado  
**Fecha:** 10 de abril  
**Autores:** Equipo de desarrollo  

### Contexto
El sistema gestiona datos relacionales complejos y requiere:
- Integridad referencial  
- Consultas optimizadas  

### Decisión
- **PostgreSQL** como base de datos principal en producción  
- **SQLite** para desarrollo local por cada desarrollador  

### Consecuencias

**Positivas:**
- Uso de llaves foráneas y restricciones  
- Prevención de datos huérfanos  
- Optimización de consultas mediante índices  

**Negativas:**
- Manejo limitado de datos no estructurados  
- Requiere soluciones adicionales (JSON o base de datos NoSQL)  

### Alternativas descartadas

- **MySQL:**  
  Menor soporte para búsquedas optimizadas y menor cumplimiento de estándares.

- **MongoDB:**  
  Mayor complejidad para mantener relaciones e integridad referencial.

---

## ADR-003: Despliegue en Render

### Estado
Aceptado  
**Fecha:** 14 de abril  
**Autores:** Equipo de desarrollo  

### Contexto
Se requiere:
- Bajo costo  
- Alta disponibilidad (≥ 99.5%)  
- Backups automáticos  
- Simplicidad operativa  

### Decisión
Se utiliza **Render** como plataforma de despliegue.

Incluye:
- PostgreSQL administrado  
- Redis (para Django Channels)  
- Almacenamiento persistente  

### Consecuencias

**Positivas:**
- Configuración sencilla desde GitHub  
- Manejo de variables de entorno  
- SSL incluido  
- Backups diarios  
- Costos predecibles  

**Negativas:**
- Mayor latencia debido a infraestructura compartida  

### Alternativas descartadas

- **Railway:**  
  Menor estabilidad en producción.

- **Heroku:**  
  Mayor costo con menos recursos.

- **AWS:**  
  Alta complejidad operativa y costos elevados.

---