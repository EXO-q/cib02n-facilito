import { Search, MapPin } from "lucide-react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function SearchBar({ value, onChange, placeholder = "Buscar por distrito o dirección..." }: SearchBarProps) {
  return (
    <div className="relative w-full">
      <div className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground">
        <Search className="w-5 h-5" />
      </div>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full h-14 pl-12 pr-12 rounded-2xl bg-white border border-border shadow-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
      />
      <div className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground">
        <MapPin className="w-5 h-5" />
      </div>
    </div>
  );
}
