# config.py
import os

# ==============================================================================
# DATOS DE IONOS - ¡MODIFICA ESTO!
# ==============================================================================

# 1. Tu Prefijo Público (API Key)
# ##### CAMBIAR AQUÍ #####
IONOS_PREFIX = "Aqui poner tu clave publica" 

# 2. Tu Clave Secreta (API Secret)
# ##### CAMBIAR AQUÍ #####
IONOS_SECRET = "Aqui poner tu clave secreta"

# 3. Tu Dominio (Ej: midominio.com)
# ##### CAMBIAR AQUÍ #####
BASE_DOMAIN = "aqui poner el nombre de tu dominio"

# ==============================================================================
# CONFIGURACIÓN TÉCNICA (NO TOCAR)
# ==============================================================================
IONOS_API_URL = "https://api.hosting.ionos.com/dns/v1"
API_HEADERS = {
    "X-API-Key": f"{IONOS_PREFIX}.{IONOS_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Rutas absolutas para que funcione bien con Systemd y Cron
BASE_DIR = "/vagrant"
PENDING_FILE = os.path.join(BASE_DIR, "data/pending_records.json")
SYNCED_FILE = os.path.join(BASE_DIR, "data/synced_records.json")