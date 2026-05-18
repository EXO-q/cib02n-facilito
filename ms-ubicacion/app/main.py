# ms-ubicacion — Microservicio de Geolocalización
# Puerto: 8003
#
# Responsabilidad: calcular distancias y devolver grifos ordenados
# por proximidad a una coordenada dada.
# En Facilito real este servicio recibe la ubicación GPS del usuario
# y consulta al ms-grifos para hacer el ranking de cercanía.

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import math
import httpx
import logging

logger = logging.getLogger("ms-ubicacion")

app = FastAPI(
    title="ms-ubicacion",
    description="Geolocalización y cálculo de distancias – Facilito UNI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Coordenadas de referencia de la UNI (punto por defecto)
UNI_LAT = -12.0207
UNI_LNG = -77.0506

# URL del microservicio de catálogo.
# BUGFIX: el original duplicaba las coordenadas de los 38 grifos en un dict
# COORDENADAS local. Eso crea dos fuentes de verdad que pueden desincronizarse
# (si se agrega/edita un grifo en ms-grifos, ms-ubicacion queda desactualizado).
# La solución correcta es obtener las coordenadas desde ms-grifos en tiempo real.
MS_GRIFOS_URL = "http://ms-grifos:8001"

# Tiempo máximo de espera para llamadas a ms-grifos (segundos).
# Si ms-grifos no responde en este tiempo, devolvemos error controlado.
TIMEOUT_SEGUNDOS = 3.0


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Fórmula de Haversine para calcular distancia en km entre dos puntos GPS.
    Es la misma que usa Google Maps para distancias en línea recta.
    """
    R = 6371  # radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlng / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def _obtener_grifos() -> list[dict]:
    """
    Llama a ms-grifos para obtener el catálogo completo.

    RESILIENCIA: usa un timeout corto y captura todas las excepciones de red
    para que ms-ubicacion no se caiga cuando ms-grifos no está disponible.
    Si falla, lanza HTTPException 503 con un mensaje claro para el cliente,
    en vez de propagar un error 500 genérico o colgar la petición.
    """
    try:
        with httpx.Client(timeout=TIMEOUT_SEGUNDOS) as client:
            resp = client.get(f"{MS_GRIFOS_URL}/grifos")
            resp.raise_for_status()
            data = resp.json()
            return data.get("grifos", [])
    except httpx.TimeoutException:
        logger.error("ms-grifos no respondió en %.1fs", TIMEOUT_SEGUNDOS)
        raise HTTPException(
            status_code=503,
            detail="El servicio de catálogo (ms-grifos) no está disponible en este momento. Intenta de nuevo."
        )
    except httpx.HTTPStatusError as exc:
        logger.error("ms-grifos devolvió error %s", exc.response.status_code)
        raise HTTPException(
            status_code=502,
            detail=f"ms-grifos respondió con error {exc.response.status_code}."
        )
    except Exception as exc:
        logger.error("Error inesperado al contactar ms-grifos: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="No se pudo contactar el servicio de catálogo. Intenta de nuevo."
        )


@app.get("/")
def health():
    return {"servicio": "ms-ubicacion", "estado": "activo", "version": "1.0.0"}


@app.get("/cercanos")
def grifos_cercanos(
    lat: float = Query(UNI_LAT, description="Latitud del usuario"),
    lng: float = Query(UNI_LNG, description="Longitud del usuario"),
    radio_km: float = Query(5.0, description="Radio de búsqueda en kilómetros", gt=0),
    limite: int = Query(10, description="Máximo de resultados a devolver", ge=1, le=100)
):
    """
    Recibe la ubicación del usuario y devuelve los grifos ordenados
    por distancia, filtrando los que estén dentro del radio indicado.
    El frontend llama a este endpoint cuando el usuario activa su GPS.

    BUGFIX: antes usaba un dict COORDENADAS hardcodeado (copia desincronizada
    de ms-grifos). Ahora obtiene los datos en tiempo real desde ms-grifos,
    eliminando la duplicación. Si ms-grifos no está disponible, devuelve
    un 503 claro en lugar de caerse o devolver datos desactualizados.
    """
    grifos = _obtener_grifos()

    resultado = []
    for g in grifos:
        # Algunos grifos podrían no tener lat/lng si ms-grifos falla parcialmente
        if "lat" not in g or "lng" not in g:
            continue
        distancia = haversine(lat, lng, g["lat"], g["lng"])
        if distancia <= radio_km:
            resultado.append({
                "grifo_id": g["id"],
                "nombre": g["nombre"],
                "marca": g["marca"],
                "distrito": g["distrito"],
                "direccion": g["direccion"],
                "distancia_km": round(distancia, 2),
                "lat": g["lat"],
                "lng": g["lng"]
            })

    # BUGFIX: el ordenamiento ya existía, pero al usar datos de ms-grifos
    # ahora es coherente con el catálogo real; antes podía dar distancias
    # distintas si las coordenadas en COORDENADAS y en GRIFOS divergían.
    resultado.sort(key=lambda x: x["distancia_km"])

    return {
        "origen": {"lat": lat, "lng": lng},
        "radio_km": radio_km,
        "total_encontrados": len(resultado),
        "grifos": resultado[:limite]
    }


@app.get("/distancia")
def calcular_distancia(
    origen_lat: float = Query(..., description="Latitud de origen"),
    origen_lng: float = Query(..., description="Longitud de origen"),
    destino_lat: float = Query(..., description="Latitud del grifo"),
    destino_lng: float = Query(..., description="Longitud del grifo")
):
    """Calcula la distancia exacta entre dos puntos GPS."""
    km = haversine(origen_lat, origen_lng, destino_lat, destino_lng)
    return {
        "distancia_km": round(km, 3),
        "distancia_m": round(km * 1000),
        "origen": {"lat": origen_lat, "lng": origen_lng},
        "destino": {"lat": destino_lat, "lng": destino_lng}
    }


@app.get("/referencia/uni")
def ubicacion_uni():
    """Devuelve las coordenadas de referencia de la UNI."""
    return {
        "nombre": "UNI - Av. Túpac Amaru 210",
        "lat": UNI_LAT,
        "lng": UNI_LNG,
        "distrito": "Rímac"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)
