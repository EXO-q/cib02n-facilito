import { MapPin, Star, Navigation } from "lucide-react";
import { Station, UserLocation } from "../data/stations";
import {
  FuelKey,
  getFuelLabel,
  getPriceColorClasses,
  getPriceLevel,
} from "../utils/priceHelpers";

interface StationCardProps {
  station: Station;
  onClick?: () => void;
  isSelected?: boolean;
  selectedFuelKey: FuelKey;
  userLocation: UserLocation;
  minPrice?: number;
  maxPrice?: number;
}

function distanceKm(a: { lat: number; lng: number }, b: { lat: number; lng: number }) {
  const R = 6371;
  const dLat = ((b.lat - a.lat) * Math.PI) / 180;
  const dLng = ((b.lng - a.lng) * Math.PI) / 180;
  const lat1 = (a.lat * Math.PI) / 180;
  const lat2 = (b.lat * Math.PI) / 180;
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}

export function StationCard({
  station,
  onClick,
  isSelected = false,
  selectedFuelKey,
  userLocation,
  minPrice,
  maxPrice,
}: StationCardProps) {
  const selectedPrice = station.prices[selectedFuelKey];
  const priceLevel = getPriceLevel(selectedPrice, minPrice, maxPrice);
  const colors = getPriceColorClasses(priceLevel);
  const km = distanceKm(userLocation, station);

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all cursor-pointer border-2 ${
        isSelected ? "border-primary" : colors.border
      }`}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-foreground mb-1">{station.name}</h3>
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <MapPin className="w-4 h-4" />
              {station.district}
            </span>
            <span className="text-blue-600 font-medium">≈ {km.toFixed(1)} km</span>
          </div>
        </div>
        <div className="flex items-center gap-1 bg-amber-50 px-2.5 py-1 rounded-lg">
          <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
          <span className="text-sm font-medium text-amber-700">{station.rating}</span>
        </div>
      </div>

      <p className="text-sm text-muted-foreground mb-4">{station.address}</p>

      <div className={`rounded-2xl p-4 mb-4 border ${colors.border} ${colors.bg}`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-muted-foreground">Precio seleccionado</div>
            <div className="text-sm font-semibold text-foreground">{getFuelLabel(selectedFuelKey)}</div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold ${colors.text}`}>S/ {selectedPrice.toFixed(2)}</div>
            <span className={`text-xs px-2 py-0.5 rounded-full ${colors.badge}`}>{colors.label}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-4">
        <div className={`rounded-xl p-3 text-center ${selectedFuelKey === "regular" ? colors.bg : "bg-blue-50"}`}>
          <div className="text-xs text-blue-600 mb-1">Regular</div>
          <div className="text-base font-semibold text-blue-700">S/ {station.prices.regular.toFixed(2)}</div>
        </div>
        <div className={`rounded-xl p-3 text-center ${selectedFuelKey === "premium" ? colors.bg : "bg-purple-50"}`}>
          <div className="text-xs text-purple-600 mb-1">Premium</div>
          <div className="text-base font-semibold text-purple-700">S/ {station.prices.premium.toFixed(2)}</div>
        </div>
        <div className={`rounded-xl p-3 text-center ${selectedFuelKey === "diesel" ? colors.bg : "bg-green-50"}`}>
          <div className="text-xs text-green-600 mb-1">Diésel</div>
          <div className="text-base font-semibold text-green-700">S/ {station.prices.diesel.toFixed(2)}</div>
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5 mb-3">
        {station.services.map((service, idx) => (
          <span key={idx} className="text-xs bg-secondary text-secondary-foreground px-2.5 py-1 rounded-full">
            {service}
          </span>
        ))}
      </div>

      <button
        onClick={(e) => {
          e.stopPropagation();
          window.open(
            `https://www.google.com/maps/dir/?api=1&destination=${station.lat},${station.lng}`,
            "_blank"
          );
        }}
        className="w-full bg-primary text-primary-foreground rounded-xl py-2.5 flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors"
      >
        <Navigation className="w-4 h-4" />
        <span className="text-sm font-medium">Cómo llegar</span>
      </button>
    </div>
  );
}
