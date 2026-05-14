export interface FuelPrice {
  regular: number;
  premium: number;
  diesel: number;
}

export interface Station {
  id: string;
  name: string;
  brand: string;
  district: string;
  address: string;
  lat: number;
  lng: number;
  prices: FuelPrice;
  rating: number;
  services: string[];
}

export interface UserLocation {
  lat: number;
  lng: number;
  label: string;
  source: "simulada" | "real";
}

export const defaultUserLocation: UserLocation = {
  lat: -12.0207,
  lng: -77.0506,
  label: "UNI - Av. Túpac Amaru 210",
  source: "simulada",
};
