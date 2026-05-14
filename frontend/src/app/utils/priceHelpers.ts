import { Station } from "../data/stations";

export type FuelType = "Todos" | "Regular" | "Premium" | "Diésel";
export type FuelKey = "regular" | "premium" | "diesel";
export type PriceLevel = "cheapest" | "middle" | "expensive" | "neutral";

export const fuelKeyByType: Record<Exclude<FuelType, "Todos">, FuelKey> = {
  Regular: "regular",
  Premium: "premium",
  Diésel: "diesel",
};

export function getSelectedFuelKey(selectedFuelType: FuelType): FuelKey {
  if (selectedFuelType === "Premium") return "premium";
  if (selectedFuelType === "Diésel") return "diesel";
  return "regular";
}

export function getFuelLabel(key: FuelKey): string {
  if (key === "regular") return "Regular";
  if (key === "premium") return "Premium";
  return "Diésel";
}

export function getPriceStats(stations: Station[], fuelKey: FuelKey) {
  const prices = stations.map((station) => station.prices[fuelKey]);
  if (prices.length === 0) return null;
  return {
    min: Math.min(...prices),
    max: Math.max(...prices),
  };
}

export function getPriceLevel(price: number, min?: number, max?: number): PriceLevel {
  if (min === undefined || max === undefined || min === max) return "neutral";
  if (price === min) return "cheapest";
  if (price === max) return "expensive";
  return "middle";
}

export function getPriceColorClasses(level: PriceLevel) {
  if (level === "cheapest") {
    return {
      bg: "bg-green-50",
      text: "text-green-700",
      border: "border-green-400",
      badge: "bg-green-100 text-green-700",
      label: "Más barato",
      hex: "#16a34a",
    };
  }
  if (level === "expensive") {
    return {
      bg: "bg-red-50",
      text: "text-red-700",
      border: "border-red-400",
      badge: "bg-red-100 text-red-700",
      label: "Más caro",
      hex: "#dc2626",
    };
  }
  if (level === "middle") {
    return {
      bg: "bg-yellow-50",
      text: "text-yellow-700",
      border: "border-yellow-400",
      badge: "bg-yellow-100 text-yellow-700",
      label: "Intermedio",
      hex: "#eab308",
    };
  }
  return {
    bg: "bg-slate-50",
    text: "text-slate-700",
    border: "border-slate-300",
    badge: "bg-slate-100 text-slate-700",
    label: "Sin comparación",
    hex: "#64748b",
  };
}
