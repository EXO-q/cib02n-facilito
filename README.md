# Facilito UNI – Simulador con Microservicios

Proyecto de Ingeniería de Software – UNI 2025

---

## Descripción

Simulación de la app Facilito (comparador de precios de combustible en Lima) usando
una arquitectura de microservicios. El objetivo fue replicar cómo Facilito separa
sus responsabilidades en servicios independientes.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│              http://localhost:5173                       │
│  Consume los 3 microservicios al cargar la app          │
└────────────┬──────────────┬──────────────┬──────────────┘
             │              │              │
     fetch()      fetch()        fetch()
             │              │              │
    ┌────────▼───┐  ┌───────▼────┐  ┌─────▼──────────┐
    │ ms-grifos  │  │ ms-precios │  │ ms-ubicacion   │
    │ :8001      │  │ :8002      │  │ :8003          │
    │            │  │            │  │                │
    │ Catálogo   │  │ Precios    │  │ Distancias     │
    │ de grifos  │  │ OSINERGMIN │  │ Haversine GPS  │
    └────────────┘  └────────────┘  └────────────────┘
```

Cada microservicio tiene **una sola responsabilidad** y corre en un proceso/puerto
independiente. Si uno cae, los demás siguen funcionando. El frontend maneja el
caso en que los servicios no estén disponibles (modo offline con datos locales).

---

## Microservicios

| Servicio | Puerto | Responsabilidad | Equivalente en Facilito real |
|---|---|---|---|
| ms-grifos | 8001 | Catálogo de estaciones, filtros por marca/distrito | Base de datos de grifos registrados |
| ms-precios | 8002 | Precios por tipo de combustible | Integración con API de OSINERGMIN |
| ms-ubicacion | 8003 | Distancias GPS, grifos cercanos | Servicio de geolocalización |

---

## Cómo ejecutar

### 1. Instalar dependencias Python (una sola vez)

```bash
pip install -r requirements.txt
```

### 2. Levantar los microservicios

**Windows:**
```
iniciar-servicios.bat
```
Se abrirán 3 ventanas de consola, una por servicio.

**Mac/Linux:**
```bash
chmod +x iniciar-servicios.sh
./iniciar-servicios.sh
```

### 3. Levantar el frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Abre http://localhost:5173

---

## Documentación automática de los servicios (Swagger)

FastAPI genera documentación interactiva automáticamente. Muy útil para la sustentación.

- http://localhost:8001/docs — ms-grifos
- http://localhost:8002/docs — ms-precios
- http://localhost:8003/docs — ms-ubicacion

---

## Endpoints principales

### ms-grifos (8001)
- `GET /grifos` — lista todos los grifos (soporta ?marca=Repsol, ?q=rimac)
- `GET /grifos/{id}` — detalle de un grifo
- `GET /marcas` — lista de marcas disponibles
- `GET /distritos` — lista de distritos

### ms-precios (8002)
- `GET /precios` — todos los precios (soporta ?ordenar_por=regular)
- `GET /precios/{id}` — precios de un grifo específico
- `GET /precios/mejor/por-tipo` — precio más bajo de cada combustible

### ms-ubicacion (8003)
- `GET /cercanos?lat=-12.02&lng=-77.05` — grifos dentro de 5km
- `GET /distancia?origen_lat=...&destino_lat=...` — distancia exacta entre dos puntos
- `GET /referencia/uni` — coordenadas de la UNI

---

## Por qué esto es una arquitectura de microservicios

- Cada servicio tiene **una sola responsabilidad** (principio SRP)
- Corren en **procesos y puertos distintos** — son independientes entre sí
- Se comunican por **HTTP/REST**, igual que en sistemas distribuidos reales
- El frontend no sabe de dónde vienen los datos, solo llama a las APIs
- Si ms-precios cae, ms-grifos y ms-ubicacion siguen funcionando
- Se pueden desplegar, escalar y actualizar por separado

En Facilito real la diferencia es que ms-precios llamaría periódicamente a la
API de OSINERGMIN, y ms-ubicacion consultaría a ms-grifos internamente para
no duplicar el catálogo. Aquí ambos tienen copia local por simplicidad.

---

## Integrantes

- [Nombre 1]
- [Nombre 2]
- [Nombre 3]
