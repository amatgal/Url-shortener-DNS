# sync_dns.py
import requests
import json
import os
from config import *

def get_zone_id(domain):
    try:
        r = requests.get(f"{IONOS_API_URL}/zones", headers=API_HEADERS)
        if r.status_code == 200:
            for z in r.json():
                if z['name'] == domain: return z['id']
    except Exception as e:
        print(f"Error conexión: {e}")
    return None

def sync():
    print("--- Sync Start ---")
    if not os.path.exists(PENDING_FILE): return
    
    with open(PENDING_FILE, 'r') as f: pending = json.load(f)
    if not pending: return

    zone_id = get_zone_id(BASE_DOMAIN)
    if not zone_id:
        print("Error: No Zone ID")
        return

    synced = []
    if os.path.exists(SYNCED_FILE):
        with open(SYNCED_FILE, 'r') as f: synced = json.load(f)
    
    still_pending = []

    for rec in pending:
        # Payload estricto para IONOS
        payload = [{
            "name": rec["fqdn"],
            "type": "TXT",
            "content": f'"{rec["long_url"]}"', # Comillas obligatorias
            "ttl": 3600,
            "disabled": False
        }]
        
        try:
            url = f"{IONOS_API_URL}/zones/{zone_id}/records"
            r = requests.post(url, headers=API_HEADERS, json=payload)
            if r.status_code in [200, 201]:
                print(f"Subido: {rec['short_code']}")
                synced.append(rec)
            else:
                print(f"Error API {r.status_code}: {r.text}")
                still_pending.append(rec)
        except Exception as e:
            print(f"Excepción: {e}")
            still_pending.append(rec)

    with open(PENDING_FILE, 'w') as f: json.dump(still_pending, f, indent=4)
    with open(SYNCED_FILE, 'w') as f: json.dump(synced, f, indent=4)
    print("--- Sync End ---")

if __name__ == "__main__":
    sync()