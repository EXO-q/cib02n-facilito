import { Station, UserLocation } from "../data/stations";
import { StationCard } from "./StationCard";
import { FuelKey } from "../utils/priceHelpers";

interface ListViewProps {
  stations: Station[];
  selectedStation: Station | null;
  onStationSelect: (station: Station) => void;
  selectedFuelKey: FuelKey;
  userLocation: UserLocation;
  minPrice?: number;
  maxPrice?: number;
}

export function ListView({ stations, selectedStation, onStationSelect, selectedFuelKey, userLocation, minPrice, maxPrice }: ListViewProps) {
  const sortLabel = userLocation.source === "real"
    ? "Ordenado por distancia a tu ubicación"
    : "Ordenado por precio (menor a mayor)";

  return (
    <div className="w-full h-full overflow-y-auto px-1 bg-white rounded-2xl shadow-sm">
      <div className="sticky top-0 z-10 bg-white border-b border-gray-100 px-4 py-2.5">
        <p className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
          <span>{userLocation.source === "real" ? "📍" : "💰"}</span>
          {sortLabel}
        </p>
      </div>
      <div className="space-y-4 p-4">
        {stations.length > 0 ? (
          stations.map((station, index) => (
            <div key={station.id} className="relative">
              {/* Badge de posición */}
              <div className={`absolute -top-2 -left-1 z-10 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white shadow-sm ${
                index === 0 ? "bg-green-500" :
                index === 1 ? "bg-green-400" :
                index === 2 ? "bg-green-300 text-green-900" :
                "bg-gray-300 text-gray-700"
              }`}>
                {index + 1}
              </div>
              <StationCard
                station={station}
                onClick={() => onStationSelect(station)}
                isSelected={selectedStation?.id === station.id}
                selectedFuelKey={selectedFuelKey}
                userLocation={userLocation}
                minPrice={minPrice}
                maxPrice={maxPrice}
              />
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center h-96 text-center">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="font-semibold text-lg mb-2">No se encontraron estaciones</h3>
            <p className="text-sm text-muted-foreground">
              Intenta cambiar los filtros o la búsqueda
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
