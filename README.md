# 🔗 DNS URL Shortener (Acortador de URL con IONOS)

Este proyecto implementa un sistema de acortamiento de URLs utilizando **Registros TXT de DNS** en lugar de una base de datos tradicional. Utiliza la API de **IONOS** para publicar los registros y una arquitectura asíncrona para garantizar la rapidez de respuesta.

Todo el entorno se despliega automáticamente sobre una máquina virtual **Ubuntu** gestionada con **Vagrant** ("Zero Touch Deployment").

## 🚀 Características Principales

*   **Arquitectura Híbrida:** Redirección inmediata local (mientras el DNS se propaga) y redirección global vía DNS.
*   **Patrón Worker Asíncrono:** El usuario recibe su enlace al instante. Un script en segundo plano (Cron) se encarga de subir los datos a IONOS cada minuto para no bloquear la interfaz.
*   **Infraestructura como Código (IaC):** Despliegue 100% automatizado con Vagrant. Se instalan dependencias, se configuran servicios (Systemd) y tareas programadas (Cron) automáticamente.
*   **Idempotencia:** Si se intenta acortar una URL existente, el sistema devuelve el código ya generado sin duplicar registros.

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje:** Python 3
*   **Servidor Web:** FastAPI + Uvicorn
*   **Infraestructura:** Vagrant + VirtualBox (Ubuntu 20.04)
*   **API Externa:** IONOS DNS API v1
*   **Automatización:** Systemd (Servicio Web) + Crontab (Sincronización)

## 📂 Estructura del Proyecto

```text
URL-SHORTENER/
├── main.py                 # Backend FastAPI: Maneja el formulario y redirecciones locales
├── sync_dns.py             # Worker: Sube los registros pendientes a IONOS (API)
├── config.py               # Configuración y credenciales (NO INCLUIDO EN REPO)
├── Vagrantfile             # Definición de la infraestructura y aprovisionamiento
├── templates/
│   └── index.html          # Interfaz web del usuario
└── data/                   # Almacenamiento local (JSON) de persistencia