import { Station, UserLocation } from "../data/stations";
import { Navigation, Star, MapPin } from "lucide-react";
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  FuelKey,
  getFuelLabel,
  getPriceColorClasses,
  getPriceLevel,
} from "../utils/priceHelpers";

interface MapViewProps {
  stations: Station[];
  selectedStation: Station | null;
  selectedFuelKey: FuelKey;
  userLocation: UserLocation;
  minPrice?: number;
  maxPrice?: number;
  onStationSelect: (station: Station) => void;
}

function buildPriceIcon(color: string, selected: boolean) {
  const size = selected ? 42 : 32;
  return L.divIcon({
    className: "custom-price-marker",
    html: `<div style="width:${size}px;height:${size}px;border-radius:9999px;background:${color};border:3px solid white;box-shadow:0 8px 18px rgba(15,23,42,.28);display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:13px;">S/</div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, -size / 2],
  });
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

export function MapView({
  stations,
  selectedStation,
  selectedFuelKey,
  userLocation,
  minPrice,
  maxPrice,
  onStationSelect,
}: MapViewProps) {
  const handleNavigate = (station: Station) => {
    window.open(
      `https://www.google.com/maps/dir/?api=1&destination=${station.lat},${station.lng}`,
      "_blank"
    );
  };

  const center: [number, number] = [userLocation.lat, userLocation.lng];

  return (
    <div className="w-full h-full rounded-2xl overflow-hidden shadow-sm bg-white flex flex-col">
      <div className="p-5 border-b border-border flex-shrink-0">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="text-xl font-semibold text-foreground">Mapa de estaciones cerca de la UNI</h3>
            <p className="text-sm text-muted-foreground">
              Mostrando {stations.length} estaciones disponibles · Combustible: {getFuelLabel(selectedFuelKey)}
            </p>
          </div>
          <div className="flex flex-wrap gap-2 text-xs font-medium">
            <span className="px-3 py-1 rounded-full bg-blue-100 text-blue-700">Azul: tu ubicación</span>
            <span className="px-3 py-1 rounded-full bg-green-100 text-green-700">Verde: más barato</span>
            <span className="px-3 py-1 rounded-full bg-yellow-100 text-yellow-700">Amarillo: intermedio</span>
            <span className="px-3 py-1 rounded-full bg-red-100 text-red-700">Rojo: más caro</span>
          </div>
        </div>
      </div>

      <div className="relative flex-1 min-h-[520px]">
        <MapContainer center={center} zoom={13} scrollWheelZoom className="w-full h-full z-0">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <CircleMarker
            center={[userLocation.lat, userLocation.lng]}
            pathOptions={{ color: "#2563eb", fillColor: "#3b82f6", fillOpacity: 0.85 }}
            radius={10}
          >
            <Popup>
              <div className="min-w-[180px]">
                <div className="font-bold text-slate-900">{userLocation.label}</div>
                <div className="text-xs text-slate-500">Ubicación {userLocation.source}</div>
              </div>
            </Popup>
          </CircleMarker>

          {stations.map((station) => {
            const price = station.prices[selectedFuelKey];
            const level = getPriceLevel(price, minPrice, maxPrice);
            const colors = getPriceColorClasses(level);
            const selected = selectedStation?.id === station.id;
            const km = distanceKm(userLocation, station);

            return (
              <Marker
                key={station.id}
                position={[station.lat, station.lng]}
                icon={buildPriceIcon(colors.hex, selected)}
                eventHandlers={{ click: () => onStationSelect(station) }}
              >
                <Popup>
                  <div className="min-w-[230px] space-y-2">
                    <div>
                      <div className="font-bold text-slate-900">{station.name}</div>
                      <div className="text-xs text-slate-500">{station.address}</div>
                      <div className="text-xs text-blue-600 mt-1">Aprox. {km.toFixed(1)} km desde tu ubicación</div>
                    </div>
                    <div className={`rounded-xl border ${colors.border} ${colors.bg} p-3`}>
                      <div className="text-xs text-slate-500">{getFuelLabel(selectedFuelKey)}</div>
                      <div className={`text-xl font-bold ${colors.text}`}>S/ {price.toFixed(2)}</div>
                      <div className={`inline-block mt-1 px-2 py-0.5 rounded-full text-xs ${colors.badge}`}>
                        {colors.label}
                      </div>
                    </div>
                    <button
                      onClick={() => handleNavigate(station)}
                      className="w-full rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white"
                    >
                      Cómo llegar
                    </button>
                  </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>

        {selectedStation && (
          <div className="absolute left-4 bottom-4 z-[500] w-[calc(100%-2rem)] max-w-sm rounded-2xl bg-white/95 p-4 shadow-xl backdrop-blur">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h4 className="font-bold text-slate-900">{selectedStation.name}</h4>
                <p className="text-xs text-slate-500">{selectedStation.district}</p>
              </div>
              <div className="flex items-center gap-1 rounded-lg bg-amber-50 px-2 py-1 text-amber-700">
                <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                <span className="text-sm font-semibold">{selectedStation.rating}</span>
              </div>
            </div>
            <p className="mt-2 text-sm text-slate-600">{selectedStation.address}</p>
            <p className="mt-2 flex items-center gap-1 text-sm text-blue-600">
              <MapPin className="h-4 w-4" />
              Aprox. {distanceKm(userLocation, selectedStation).toFixed(1)} km desde tu ubicación
            </p>
            <button
              onClick={() => handleNavigate(selectedStation)}
              className="mt-3 flex w-full items-center justify-center gap-2 rounded-xl bg-primary py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90"
            >
              <Navigation className="h-4 w-4" />
              Abrir ruta en Google Maps
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
