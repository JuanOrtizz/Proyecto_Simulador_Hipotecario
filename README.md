# Proyecto Simulador de Crédito Hipotecario 
## Finanzas Raíz

Este proyecto es un simulador de crédito hipotecario. La idea es que el usuario pueda saber si califica para un crédito según algunos requisitos básicos, y en caso de que sí, obtener un informe de financiamiento con todos los datos calculados.

Está pensado como una herramienta práctica, simple de usar, pero que refleje más o menos cómo sería el análisis real de un crédito.

---

## Objetivos del proyecto

- Mostrar si una persona califica o no para un crédito hipotecario.
- Hacer todos los cálculos necesarios si califica y enviarle un informe por email.
- Tener un sistema de login para acceder al dashboard.
- CRUD para modelos `Solicitudes` y `Consultas`
- Desde el dashboard se pueden ver las solicitudes y consultas que llegan desde los formularios.
- Tiene formularios de contacto para que los usuarios puedan enviar sus datos.

---

## Funcionalidades principales

- Simulación de crédito hipotecario con validaciones en frontend y backend.
- Informes generados automáticamente si califica (Envio por mail con SMTP).
- Login para ver y gestionar la informacion desde el dashboard.
- Dashboard privado con:
  - Tabla de solicitudes (editar, eliminar).
  - Tabla de consultas (contactar, eliminar).
- Endpoints protegidos: para acceder a **Solicitudes** y **Consultas**, hay que estar logueado desde el dashboard para mayor seguridad.
- Formularios públicos para enviar solicitudes y consultas.

---

## Tecnologias Utilizadas
- HTML5
- CSS
- JavaScript
- Python
- Django
- PostgreSQL
---
## Credenciales para el Dashboard
- **Usuario:** adminUces
- **Contraseña:** Uces2025+