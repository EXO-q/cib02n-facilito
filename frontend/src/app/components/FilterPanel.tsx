import { SlidersHorizontal, Fuel } from "lucide-react";

interface FilterPanelProps {
  selectedFuelType: string;
  selectedBrand: string;
  onFuelTypeChange: (type: string) => void;
  onBrandChange: (brand: string) => void;
  brands?: string[];
}

export function FilterPanel({
  selectedFuelType,
  selectedBrand,
  onFuelTypeChange,
  onBrandChange,
  brands = [],
}: FilterPanelProps) {
  const fuelTypes = ["Todos", "Regular", "Premium", "Diésel"];

  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <SlidersHorizontal className="w-5 h-5 text-primary" />
        <h3 className="font-semibold text-foreground">Filtros</h3>
      </div>

      <div className="mb-5">
        <div className="flex items-center gap-2 mb-3">
          <Fuel className="w-4 h-4 text-muted-foreground" />
          <label className="text-sm text-muted-foreground">Tipo de combustible</label>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {fuelTypes.map((type) => (
            <button
              key={type}
              onClick={() => onFuelTypeChange(type)}
              className={`py-2.5 px-3 rounded-xl text-sm font-medium transition-all ${
                selectedFuelType === type
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="text-sm text-muted-foreground mb-3 block">Marca</label>
        <select
          value={selectedBrand}
          onChange={(e) => onBrandChange(e.target.value)}
          className="w-full h-11 px-4 rounded-xl bg-secondary text-secondary-foreground border-0 focus:outline-none focus:ring-2 focus:ring-primary/20"
        >
          <option value="Todas">Todas las marcas</option>
          {brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
