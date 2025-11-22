# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import random
import string
import os
from config import PENDING_FILE, SYNCED_FILE, BASE_DOMAIN

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Helpers
def load_json(filepath):
    if not os.path.exists(filepath): return []
    with open(filepath, "r") as f:
        try: return json.load(f)
        except: return []

def save_json(filepath, data):
    with open(filepath, "w") as f: json.dump(data, f, indent=4)

def generate_short_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

def find_existing_url(long_url):
    records = load_json(PENDING_FILE) + load_json(SYNCED_FILE)
    for r in records:
        if r["long_url"] == long_url: return r
    return None

def find_url_by_code(code):
    records = load_json(PENDING_FILE) + load_json(SYNCED_FILE)
    for r in records:
        if r["short_code"] == code: return r["long_url"]
    return None

# Rutas
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten", response_class=HTMLResponse)
async def shorten(request: Request, long_url: str = Form(...)):
    existing = find_existing_url(long_url)
    if existing:
        code = existing["short_code"]
        is_new = False
    else:
        code = generate_short_code()
        new_rec = {
            "short_code": code,
            "long_url": long_url,
            "fqdn": f"{code}.{BASE_DOMAIN}"
        }
        pending = load_json(PENDING_FILE)
        pending.append(new_rec)
        save_json(PENDING_FILE, pending)
        is_new = True

    local_link = f"http://{request.base_url.hostname}:8000/{code}"
    dns_link = f"http://{code}.{BASE_DOMAIN}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "short_code": code,
        "long_url": long_url,
        "local_link": local_link,
        "dns_link": dns_link,
        "message": "Creado exitosamente" if is_new else "Ya existía"
    })

@app.get("/{short_code}")
async def redirect(short_code: str):
    url = find_url_by_code(short_code)
    if url: return RedirectResponse(url)
    return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)