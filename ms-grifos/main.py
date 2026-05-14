import sqlite3
import json
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(
    title="ms-grifos",
    description="Catálogo de estaciones de servicio – Facilito UNI",
    version="1.0.0"
)

# CORS abierto para que el frontend pueda consumirlo desde localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'facilito.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def health():
    return {"servicio": "ms-grifos", "estado": "activo", "version": "1.0.0", "fuente": "SQLite"}

@app.get("/grifos")
def listar_grifos(
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    distrito: Optional[str] = Query(None, description="Filtrar por distrito"),
    q: Optional[str] = Query(None, description="Búsqueda por nombre, dirección o distrito")
):
    """
    Devuelve el catálogo de estaciones con filtros opcionales.
    El frontend llama a este endpoint al cargar la app y cuando el usuario filtra.
    """
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM estaciones WHERE 1=1"
    params = []

    if marca:
        query += " AND LOWER(marca) = ?"
        params.append(marca.lower())

    if distrito:
        query += " AND LOWER(distrito) = ?"
        params.append(distrito.lower())

    if q:
        q_lower = f"%{q.lower()}%"
        query += " AND (LOWER(nombre) LIKE ? OR LOWER(distrito) LIKE ? OR LOWER(direccion) LIKE ? OR LOWER(marca) LIKE ?)"
        params.extend([q_lower, q_lower, q_lower, q_lower])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for r in rows:
        d = dict(r)
        d['servicios'] = json.loads(d['servicios'])
        resultado.append(d)

    return {"total": len(resultado), "grifos": resultado}

@app.get("/grifos/{grifo_id}")
def obtener_grifo(grifo_id: str):
    """Detalle de un grifo específico por ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estaciones WHERE id = ?", (grifo_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Grifo '{grifo_id}' no encontrado")
    
    d = dict(row)
    d['servicios'] = json.loads(d['servicios'])
    return d

@app.get("/marcas")
def listar_marcas():
    """Devuelve las marcas disponibles para el panel de filtros."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT marca FROM estaciones ORDER BY marca")
    marcas = [r['marca'] for r in cursor.fetchall()]
    conn.close()
    return {"marcas": marcas}

@app.get("/distritos")
def listar_distritos():
    """Devuelve los distritos disponibles para el panel de filtros."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT distrito FROM estaciones ORDER BY distrito")
    distritos = [r['distrito'] for r in cursor.fetchall()]
    conn.close()
    return {"distritos": distritos}
