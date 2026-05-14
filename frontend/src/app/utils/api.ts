// api.ts — Capa de comunicación con los microservicios
//
// Cada función llama al microservicio correspondiente.
// Si los servicios no están corriendo, cae al modo offline con datos locales.

const MS_GRIFOS   = "http://localhost:8001";
const MS_PRECIOS  = "http://localhost:8002";
const MS_UBICACION = "http://localhost:8003";

// --- Tipos ---

export interface Grifo {
  id: string;
  nombre: string;
  marca: string;
  distrito: string;
  direccion: string;
  lat: number;
  lng: number;
  rating: number;
  servicios: string[];
}

export interface PreciosGrifo {
  regular: number;
  premium: number;
  diesel: number;
}

export interface GrifoConPrecios extends Grifo {
  prices: PreciosGrifo; // mismo nombre que usa el frontend original
  name: string;         // alias para compatibilidad
  brand: string;
  district: string;
  address: string;
}

// --- ms-grifos ---

export async function fetchGrifos(params?: {
  marca?: string;
  distrito?: string;
  q?: string;
}): Promise<Grifo[]> {
  const url = new URL(`${MS_GRIFOS}/grifos`);
  if (params?.marca)    url.searchParams.set("marca", params.marca);
  if (params?.distrito) url.searchParams.set("distrito", params.distrito);
  if (params?.q)        url.searchParams.set("q", params.q);

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error("ms-grifos no responde");
  const data = await res.json();
  return data.grifos;
}

export async function fetchMarcas(): Promise<string[]> {
  const res = await fetch(`${MS_GRIFOS}/marcas`);
  if (!res.ok) throw new Error("ms-grifos: error al obtener marcas");
  const data = await res.json();
  return data.marcas;
}

// --- ms-precios ---

export async function fetchPrecios(): Promise<Record<string, PreciosGrifo>> {
  const res = await fetch(`${MS_PRECIOS}/precios`);
  if (!res.ok) throw new Error("ms-precios no responde");
  const data = await res.json();
  // Convertir array a mapa id -> precios
  const mapa: Record<string, PreciosGrifo> = {};
  for (const item of data.precios) {
    mapa[item.grifo_id] = item.precios;
  }
  return mapa;
}

export async function fetchMejoresPrecios() {
  const res = await fetch(`${MS_PRECIOS}/precios/mejor/por-tipo`);
  if (!res.ok) throw new Error("ms-precios: error en mejores precios");
  return res.json();
}

// --- ms-ubicacion ---

export async function fetchCercanos(lat: number, lng: number, radioKm = 5) {
  const url = `${MS_UBICACION}/cercanos?lat=${lat}&lng=${lng}&radio_km=${radioKm}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("ms-ubicacion no responde");
  return res.json();
}

// --- Helper: combina grifos + precios en un objeto que entiende el frontend ---

export async function fetchEstaciones(params?: {
  marca?: string;
  q?: string;
}): Promise<{estaciones: GrifoConPrecios[], errorGrifos: boolean, errorPrecios: boolean}> {
  const [grifosResult, preciosResult] = await Promise.allSettled([
    fetchGrifos(params),
    fetchPrecios(),
  ]);

  const errorGrifos = grifosResult.status === 'rejected';
  const errorPrecios = preciosResult.status === 'rejected';

  const grifos = grifosResult.status === 'fulfilled' ? grifosResult.value : [];
  const precios = preciosResult.status === 'fulfilled' ? preciosResult.value : {};

  const estaciones = grifos.map((g) => ({
    ...g,
    name: g.nombre,
    brand: g.marca,
    district: g.distrito,
    address: g.direccion,
    services: g.servicios ?? [],   // StationCard usa 'services', el API devuelve 'servicios'
    prices: precios[g.id] ?? { regular: 0, premium: 0, diesel: 0 },
  }));

  return { estaciones, errorGrifos, errorPrecios };
}
