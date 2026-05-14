import { useState, useMemo, useEffect } from "react";
import { Map, List, TrendingDown, LocateFixed, MapPin, Wifi, WifiOff } from "lucide-react";
import { SearchBar } from "./components/SearchBar";
import { FilterPanel } from "./components/FilterPanel";
import { MapView } from "./components/MapView";
import { ListView } from "./components/ListView";
import { FuelType, getSelectedFuelKey, getPriceStats } from "./utils/priceHelpers";
import { fetchEstaciones, fetchCercanos, GrifoConPrecios } from "./utils/api";

const UNI_LOCATION = {
  lat: -12.0207,
  lng: -77.0506,
  label: "UNI - Av. Túpac Amaru 210",
  source: "simulada" as const,
};


export default function App() {
  const [searchQuery, setSearchQuery]       = useState("");
  const [selectedFuelType, setSelectedFuelType] = useState<FuelType>("Regular");
  const [selectedBrand, setSelectedBrand]   = useState("Todas");
  const [viewMode, setViewMode]             = useState<"map" | "list">("map");
  const [selectedStation, setSelectedStation] = useState<GrifoConPrecios | null>(null);
  const [userLocation, setUserLocation]     = useState(UNI_LOCATION);
  const [locationStatus, setLocationStatus] = useState("Ubicación simulada en la UNI");
  const [estaciones, setEstaciones]         = useState<GrifoConPrecios[]>([]);
  const [cargando, setCargando]             = useState(true);
  const [errorGrifos, setErrorGrifos]       = useState(false);
  const [errorPrecios, setErrorPrecios]     = useState(false);
  const [errorUbicacion, setErrorUbicacion] = useState(false);
  const [distances, setDistances]           = useState<Record<string, number>>({});

  useEffect(() => {
    setCargando(true);
    fetchEstaciones()
      .then((data: any) => {
        setEstaciones(data.estaciones || []);
        setErrorGrifos(data.errorGrifos);
        setErrorPrecios(data.errorPrecios);
      })
      .catch(() => {
        setEstaciones([]);
        setErrorGrifos(true);
        setErrorPrecios(true);
      })
      .finally(() => setCargando(false));
  }, []);

  useEffect(() => {
    fetchCercanos(userLocation.lat, userLocation.lng, 50)
      .then((res: any) => {
         const distMap: Record<string, number> = {};
         res.grifos.forEach((g: any) => {
            distMap[g.grifo_id] = g.distancia_km;
         });
         setDistances(distMap);
         setErrorUbicacion(false);
      })
      .catch(() => {
         setDistances({});
         setErrorUbicacion(true);
      });
  }, [userLocation]);

  const selectedFuelKey = useMemo(() => getSelectedFuelKey(selectedFuelType), [selectedFuelType]);

  const filteredStations = useMemo(() => {
    return estaciones.filter((station) => {
      const normalizedSearch = searchQuery.trim().toLowerCase();
      const matchesSearch =
        normalizedSearch === "" ||
        station.name.toLowerCase().includes(normalizedSearch) ||
        station.district.toLowerCase().includes(normalizedSearch) ||
        station.address.toLowerCase().includes(normalizedSearch) ||
        station.brand.toLowerCase().includes(normalizedSearch);
      const matchesBrand = selectedBrand === "Todas" || station.brand === selectedBrand;
      return matchesSearch && matchesBrand;
    });
  }, [estaciones, searchQuery, selectedBrand]);

  const priceStats = useMemo(
    () => getPriceStats(filteredStations, selectedFuelKey),
    [filteredStations, selectedFuelKey]
  );

  const lowestPrices = useMemo(() => {
    if (filteredStations.length === 0) return null;
    return {
      regular: Math.min(...filteredStations.map((s) => s.prices.regular)),
      premium: Math.min(...filteredStations.map((s) => s.prices.premium)),
      diesel:  Math.min(...filteredStations.map((s) => s.prices.diesel)),
    };
  }, [filteredStations]);


  // Marcas derivadas de las estaciones reales cargadas desde ms-grifos
  const marcasDisponibles = useMemo(() => {
    return Array.from(new Set(estaciones.map((s) => s.brand))).sort();
  }, [estaciones]);
  // Cuando el usuario usa GPS real, ordena por distancia.
  // Cuando usa ubicación simulada (UNI), ordena por precio.
  const orderedStations = useMemo(() => {
    if (userLocation.source === "real") {
      return [...filteredStations].sort((a, b) => {
        const distA = distances[a.id] ?? 999;
        const distB = distances[b.id] ?? 999;
        return distA - distB;
      });
    }
    return [...filteredStations].sort(
      (a, b) => a.prices[selectedFuelKey] - b.prices[selectedFuelKey]
    );
  }, [filteredStations, selectedFuelKey, userLocation, distances]);

  const requestUserLocation = () => {
    if (!navigator.geolocation) {
      setLocationStatus("Tu navegador no soporta geolocalización.");
      return;
    }
    setLocationStatus("Solicitando ubicación real...");
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          label: "Tu ubicación real",
          source: "real",
        });
        setLocationStatus("Usando tu ubicación real");
      },
      () => {
        setUserLocation(UNI_LOCATION);
        setLocationStatus("No se pudo obtener la ubicación. Se usa la UNI.");
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 60000 }
    );
  };

  return (
    <div className="w-full h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex flex-col overflow-hidden">
      <header className="bg-white shadow-sm border-b border-border flex-shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center">
                <TrendingDown className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">Facilito UNI</h1>
                <p className="text-sm text-muted-foreground">Compara precios de combustible en Lima</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${
                errorGrifos || errorPrecios || errorUbicacion
                  ? "bg-red-50 text-red-600 border border-red-200"
                  : "bg-green-50 text-green-600 border border-green-200"
              }`}>
                {errorGrifos || errorPrecios || errorUbicacion
                  ? <><WifiOff className="w-3.5 h-3.5" /> Error en microservicios</>
                  : <><Wifi className="w-3.5 h-3.5" /> Microservicios activos</>
                }
              </div>

              <div className="flex bg-secondary rounded-xl p-1">
                <button
                  onClick={() => setViewMode("map")}
                  className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
                    viewMode === "map"
                      ? "bg-white shadow-sm text-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Map className="w-4 h-4" />
                  <span className="text-sm font-medium hidden sm:inline">Mapa</span>
                </button>
                <button
                  onClick={() => setViewMode("list")}
                  className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
                    viewMode === "list"
                      ? "bg-white shadow-sm text-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <List className="w-4 h-4" />
                  <span className="text-sm font-medium hidden sm:inline">Lista</span>
                </button>
              </div>
            </div>
          </div>
          <SearchBar value={searchQuery} onChange={setSearchQuery} />
        </div>
      </header>

      <main className="flex-1 overflow-auto">
        {cargando ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-3">
              <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-muted-foreground text-sm">Conectando con microservicios...</p>
            </div>
          </div>
        ) : (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {errorGrifos && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">
                <strong>Error en ms-grifos:</strong> No se pudo conectar al catálogo de estaciones. Ejecuta <code>iniciar-servicios.bat</code>.
              </div>
            )}
            {errorPrecios && !errorGrifos && (
              <div className="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-xl text-sm text-orange-700">
                <strong>Error en ms-precios:</strong> No se pudo conectar al servicio de precios. Los precios mostrados no están disponibles.
              </div>
            )}
            {errorUbicacion && !errorGrifos && (
              <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-xl text-sm text-yellow-700">
                <strong>Error en ms-ubicacion:</strong> No se pudo conectar al servicio de distancias. El ordenamiento por cercanía no funcionará.
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 min-h-[600px]">
              <aside className="lg:col-span-1 space-y-4">
                <FilterPanel
                  selectedFuelType={selectedFuelType}
                  selectedBrand={selectedBrand}
                  onFuelTypeChange={(type) => setSelectedFuelType(type as FuelType)}
                  onBrandChange={setSelectedBrand}
                  brands={marcasDisponibles}
                />

                <div className="bg-white rounded-2xl p-5 shadow-sm">
                  <div className="flex items-center gap-2 mb-3">
                    <MapPin className="w-5 h-5 text-blue-600" />
                    <h3 className="font-semibold text-foreground">Ubicación</h3>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">
                    {userLocation.label}
                    <span className="ml-1 text-xs">({userLocation.source})</span>
                  </p>
                  <button
                    onClick={requestUserLocation}
                    className="w-full rounded-xl bg-blue-600 px-3 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <LocateFixed className="w-4 h-4" />
                    Usar mi ubicación real
                  </button>
                  <p className="mt-2 text-xs text-muted-foreground">{locationStatus}</p>
                </div>

                <div className="bg-white rounded-2xl p-5 shadow-sm">
                  <h3 className="font-semibold text-foreground mb-3">Mejores precios</h3>
                  {lowestPrices ? (
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-blue-600">Regular</span>
                        <span className="font-semibold text-blue-700">S/ {lowestPrices.regular.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-purple-600">Premium</span>
                        <span className="font-semibold text-purple-700">S/ {lowestPrices.premium.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-green-600">Diésel</span>
                        <span className="font-semibold text-green-700">S/ {lowestPrices.diesel.toFixed(2)}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-muted-foreground">No hay datos disponibles</p>
                  )}
                </div>

                <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-5 text-white shadow-sm">
                  <div className="text-3xl font-bold mb-1">{filteredStations.length}</div>
                  <div className="text-sm opacity-90">Estaciones encontradas</div>
                  <div className="text-xs opacity-70 mt-1">
                    {userLocation.source === "real" ? "Ordenado por cercanía a ti" : errorGrifos ? "Sin datos" : "Ordenado por precio"}
                  </div>
                </div>
              </aside>

              <div className="lg:col-span-3 h-[700px]">
                {viewMode === "map" ? (
                  <MapView
                    stations={orderedStations}
                    selectedStation={selectedStation}
                    selectedFuelKey={selectedFuelKey}
                    userLocation={userLocation}
                    minPrice={priceStats?.min}
                    maxPrice={priceStats?.max}
                    onStationSelect={setSelectedStation}
                  />
                ) : (
                  <ListView
                    stations={orderedStations}
                    selectedStation={selectedStation}
                    selectedFuelKey={selectedFuelKey}
                    userLocation={userLocation}
                    minPrice={priceStats?.min}
                    maxPrice={priceStats?.max}
                    onStationSelect={setSelectedStation}
                  />
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
