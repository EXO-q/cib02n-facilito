import sqlite3
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="ms-precios",
    description="Precios de combustible por estación – Facilito UNI",
    version="1.0.0"
)

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

TIPOS_VALIDOS = {"regular", "premium", "diesel"}
# Fecha simulada de última actualización (en producción vendría de la BD)
ULTIMA_ACTUALIZACION = "2025-04-28T08:00:00"

@app.get("/")
def health():
    return {"servicio": "ms-precios", "estado": "activo", "version": "1.0.0", "fuente": "SQLite"}

@app.get("/precios")
def listar_precios(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo: regular, premium, diesel"),
    ordenar_por: Optional[str] = Query(None, description="Ordenar por tipo de combustible: regular, premium, diesel")
):
    """
    Devuelve todos los precios. El frontend lo usa para calcular
    el mínimo y máximo y pintar los colores verde/amarillo/rojo.
    """
    if tipo and tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo '{tipo}' no válido. Use: regular, premium, diesel"
        )
    if ordenar_por and ordenar_por not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"ordenar_por '{ordenar_por}' no válido. Use: regular, premium, diesel"
        )

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT grifo_id, regular, premium, diesel FROM precios")
    rows = cursor.fetchall()
    conn.close()

    resultado = []
    for r in rows:
        d = dict(r)
        grifo_id = d.pop('grifo_id')
        precios = d
        
        if tipo:
            # Devolver solo el precio del tipo solicitado
            entrada = {
                "grifo_id": grifo_id,
                "precios": {tipo: precios[tipo]},
                "actualizado": ULTIMA_ACTUALIZACION
            }
        else:
            entrada = {"grifo_id": grifo_id, "precios": precios, "actualizado": ULTIMA_ACTUALIZACION}
        resultado.append(entrada)

    if ordenar_por:
        resultado.sort(key=lambda x: x["precios"][ordenar_por])

    return {
        "total": len(resultado),
        "fuente": "SQLite",
        "actualizado": ULTIMA_ACTUALIZACION,
        "precios": resultado
    }

@app.get("/precios/mejor/por-tipo")
def mejores_precios():
    """
    Devuelve el precio más bajo de cada tipo de combustible
    y qué grifo lo ofrece. Útil para el panel de 'Mejores precios'.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    mejor = {}
    for tipo in ["regular", "premium", "diesel"]:
        cursor.execute(f"SELECT grifo_id, {tipo} as precio FROM precios ORDER BY {tipo} ASC LIMIT 1")
        row = cursor.fetchone()
        if row:
            mejor[tipo] = {"precio": row["precio"], "grifo_id": row["grifo_id"]}
        else:
            mejor[tipo] = None
    conn.close()

    return {"mejores_precios": mejor, "actualizado": ULTIMA_ACTUALIZACION}

@app.get("/precios/{grifo_id}")
def precios_por_grifo(grifo_id: str):
    """Precios de una estación específica."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT regular, premium, diesel FROM precios WHERE grifo_id = ?", (grifo_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"No hay precios registrados para el grifo '{grifo_id}'"
        )
        
    return {
        "grifo_id": grifo_id,
        "precios": dict(row),
        "fuente": "SQLite",
        "actualizado": ULTIMA_ACTUALIZACION
    }
