import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'facilito.db')

GRIFOS = [
    {"id": "uni-1", "nombre": "Repsol San Cristóbal [DB]", "marca": "Repsol", "distrito": "Rímac", "direccion": "Av. 9 de Octubre 508", "lat": -12.03908, "lng": -77.016024, "rating": 4.4, "servicios": ["Tienda", "Baño", "24 horas"]},
    {"id": "uni-2", "nombre": "Repsol Tarapacá [DB]", "marca": "Repsol", "distrito": "Rímac", "direccion": "Av. Coronel Samuel Alcázar 801", "lat": -12.026932, "lng": -77.033602, "rating": 4.2, "servicios": ["Tienda", "Baño"]},
    {"id": "uni-3", "nombre": "Petroperú Rímac [DB]", "marca": "Petroperú", "distrito": "Rímac", "direccion": "Calle Sérvulo Gutiérrez 25", "lat": -12.036595, "lng": -77.037224, "rating": 4.1, "servicios": ["Tienda", "Diésel", "Baño"]},
    {"id": "uni-4", "nombre": "Repsol Pegaso [DB]", "marca": "Repsol", "distrito": "Independencia", "direccion": "Av. Túpac Amaru s/n, Urb. Mesa Redonda", "lat": -12.0056, "lng": -77.0589, "rating": 4.5, "servicios": ["Tienda", "CMR Puntos", "LATAM Pass"]},
    {"id": "uni-5", "nombre": "Repsol Super Repsol [DB]", "marca": "Repsol", "distrito": "Independencia", "direccion": "Av. Alfredo Mendiola 2000", "lat": -12.0102, "lng": -77.0597, "rating": 4.3, "servicios": ["Tienda", "Baño", "24 horas"]},
    {"id": "uni-6", "nombre": "Repsol Comas [DB]", "marca": "Repsol", "distrito": "Independencia", "direccion": "Av. Gerardo Unger 3689, Urb. Panamericana Norte", "lat": -11.9979, "lng": -77.0596, "rating": 4.0, "servicios": ["Tienda", "Baño"]},
    {"id": "uni-7", "nombre": "GESA Grifo Espinoza [DB]", "marca": "GESA", "distrito": "Independencia", "direccion": "Av. Tomás Valle", "lat": -12.0077, "lng": -77.0619, "rating": 3.9, "servicios": ["Tienda", "Aire", "Agua"]},
    {"id": "uni-8", "nombre": "Repsol Los Milagros [DB]", "marca": "Repsol", "distrito": "San Martín de Porres", "direccion": "Av. Túpac Amaru 1453", "lat": -12.0124, "lng": -77.0528, "rating": 4.2, "servicios": ["Tienda", "Baño", "Lavado"]},
    {"id": "uni-9", "nombre": "Estación UNI Norte [DB]", "marca": "Demo UNI", "distrito": "Independencia", "direccion": "Zona norte Av. Túpac Amaru (referencia demo)", "lat": -12.0152, "lng": -77.0549, "rating": 4.6, "servicios": ["Demo", "Tienda", "Baño"]},
    {"id": "uni-10", "nombre": "Estación UNI Sur [DB]", "marca": "Demo UNI", "distrito": "Rímac", "direccion": "Zona sur Av. Túpac Amaru (referencia demo)", "lat": -12.0248, "lng": -77.0472, "rating": 4.4, "servicios": ["Demo", "Aire", "Agua"]},
    # Miraflores
    {"id": "mfl-1", "nombre": "Repsol Miraflores Larco [DB]", "marca": "Repsol", "distrito": "Miraflores", "direccion": "Av. Larco 1150", "lat": -12.1211, "lng": -77.0285, "rating": 4.6, "servicios": ["Tienda", "Baño", "24 horas", "CMR Puntos"]},
    {"id": "mfl-2", "nombre": "Petroperú Miraflores [DB]", "marca": "Petroperú", "distrito": "Miraflores", "direccion": "Av. Benavides 598", "lat": -12.1280, "lng": -77.0220, "rating": 4.3, "servicios": ["Tienda", "Diésel", "Baño"]},
    {"id": "mfl-3", "nombre": "GESA Óvalo Miraflores [DB]", "marca": "GESA", "distrito": "Miraflores", "direccion": "Av. José Pardo 698", "lat": -12.1180, "lng": -77.0310, "rating": 4.1, "servicios": ["Tienda", "Aire", "Agua"]},
    # San Isidro
    {"id": "si-1", "nombre": "Repsol San Isidro Centro [DB]", "marca": "Repsol", "distrito": "San Isidro", "direccion": "Av. Javier Prado Este 380", "lat": -12.0942, "lng": -77.0333, "rating": 4.5, "servicios": ["Tienda", "Baño", "24 horas"]},
    {"id": "si-2", "nombre": "Primax San Isidro [DB]", "marca": "Primax", "distrito": "San Isidro", "direccion": "Calle Las Orquídeas 675", "lat": -12.0980, "lng": -77.0365, "rating": 4.4, "servicios": ["Tienda", "CMR Puntos", "Baño"]},
    # San Borja
    {"id": "sb-1", "nombre": "Repsol San Borja [DB]", "marca": "Repsol", "distrito": "San Borja", "direccion": "Av. San Borja Norte 820", "lat": -12.1020, "lng": -77.0020, "rating": 4.3, "servicios": ["Tienda", "Baño", "Lavado"]},
    {"id": "sb-2", "nombre": "Petroperú San Borja Sur [DB]", "marca": "Petroperú", "distrito": "San Borja", "direccion": "Av. Aviación 2450", "lat": -12.1080, "lng": -77.0000, "rating": 4.0, "servicios": ["Tienda", "Diésel"]},
    # Surco
    {"id": "sur-1", "nombre": "Repsol Surco Primavera [DB]", "marca": "Repsol", "distrito": "Surco", "direccion": "Av. Primavera 1250", "lat": -12.1210, "lng": -76.9930, "rating": 4.5, "servicios": ["Tienda", "24 horas", "Baño", "CMR Puntos"]},
    {"id": "sur-2", "nombre": "Primax Surco Caminos del Inca [DB]", "marca": "Primax", "distrito": "Surco", "direccion": "Av. Caminos del Inca 790", "lat": -12.1340, "lng": -76.9870, "rating": 4.2, "servicios": ["Tienda", "Baño"]},
    {"id": "sur-3", "nombre": "GESA Surco Monterrico [DB]", "marca": "GESA", "distrito": "Surco", "direccion": "Av. La Encalada 1550", "lat": -12.1050, "lng": -76.9750, "rating": 3.9, "servicios": ["Aire", "Agua", "Tienda"]},
    # La Molina
    {"id": "lm-1", "nombre": "Repsol La Molina [DB]", "marca": "Repsol", "distrito": "La Molina", "direccion": "Av. La Molina 1250", "lat": -12.0780, "lng": -76.9420, "rating": 4.4, "servicios": ["Tienda", "24 horas", "Baño"]},
    {"id": "lm-2", "nombre": "Primax La Molina Rinconada [DB]", "marca": "Primax", "distrito": "La Molina", "direccion": "Av. Raúl Ferrero 1080", "lat": -12.0850, "lng": -76.9380, "rating": 4.3, "servicios": ["Tienda", "Baño", "Lavado"]},
    # Ate
    {"id": "ate-1", "nombre": "Repsol Ate Vitarte [DB]", "marca": "Repsol", "distrito": "Ate", "direccion": "Carretera Central Km 4.5", "lat": -12.0450, "lng": -76.9700, "rating": 4.1, "servicios": ["Tienda", "Diésel", "24 horas"]},
    {"id": "ate-2", "nombre": "Petroperú Ate Santa Clara [DB]", "marca": "Petroperú", "distrito": "Ate", "direccion": "Av. Separadora Industrial 1800", "lat": -12.0380, "lng": -76.9550, "rating": 3.8, "servicios": ["Diésel", "Tienda"]},
    # Los Olivos
    {"id": "lo-1", "nombre": "Repsol Los Olivos Universitaria [DB]", "marca": "Repsol", "distrito": "Los Olivos", "direccion": "Av. Universitaria Norte 2800", "lat": -11.9950, "lng": -77.0680, "rating": 4.3, "servicios": ["Tienda", "Baño", "CMR Puntos"]},
    {"id": "lo-2", "nombre": "GESA Los Olivos Naranjal [DB]", "marca": "GESA", "distrito": "Los Olivos", "direccion": "Av. Naranjal 850", "lat": -11.9880, "lng": -77.0720, "rating": 4.0, "servicios": ["Tienda", "Aire"]},
    # San Miguel
    {"id": "sm-1", "nombre": "Repsol San Miguel La Marina [DB]", "marca": "Repsol", "distrito": "San Miguel", "direccion": "Av. La Marina 2850", "lat": -12.0780, "lng": -77.0870, "rating": 4.4, "servicios": ["Tienda", "24 horas", "Baño"]},
    {"id": "sm-2", "nombre": "Primax San Miguel [DB]", "marca": "Primax", "distrito": "San Miguel", "direccion": "Av. Universitaria 1550", "lat": -12.0820, "lng": -77.0910, "rating": 4.2, "servicios": ["Tienda", "Baño", "Lavado"]},
    # Cercado de Lima
    {"id": "cl-1", "nombre": "Repsol Brasil [DB]", "marca": "Repsol", "distrito": "Cercado de Lima", "direccion": "Av. Brasil 1650", "lat": -12.0650, "lng": -77.0530, "rating": 4.1, "servicios": ["Tienda", "Baño"]},
    {"id": "cl-2", "nombre": "Petroperú Abancay [DB]", "marca": "Petroperú", "distrito": "Cercado de Lima", "direccion": "Av. Abancay 750", "lat": -12.0530, "lng": -77.0270, "rating": 3.9, "servicios": ["Tienda", "Diésel"]},
    # Jesús María
    {"id": "jm-1", "nombre": "Repsol Jesús María [DB]", "marca": "Repsol", "distrito": "Jesús María", "direccion": "Av. Faustino Sánchez Carrión 850", "lat": -12.0720, "lng": -77.0470, "rating": 4.3, "servicios": ["Tienda", "Baño", "24 horas"]},
    # Lince
    {"id": "lin-1", "nombre": "Primax Lince [DB]", "marca": "Primax", "distrito": "Lince", "direccion": "Av. Arequipa 2750", "lat": -12.0840, "lng": -77.0360, "rating": 4.2, "servicios": ["Tienda", "CMR Puntos"]},
    # Barranco
    {"id": "bar-1", "nombre": "Repsol Barranco [DB]", "marca": "Repsol", "distrito": "Barranco", "direccion": "Av. Grau 780", "lat": -12.1480, "lng": -77.0220, "rating": 4.4, "servicios": ["Tienda", "Baño"]},
    # Chorrillos
    {"id": "cho-1", "nombre": "Repsol Chorrillos [DB]", "marca": "Repsol", "distrito": "Chorrillos", "direccion": "Av. Huaylas 1050", "lat": -12.1690, "lng": -77.0200, "rating": 4.1, "servicios": ["Tienda", "Baño", "24 horas"]},
    {"id": "cho-2", "nombre": "Petroperú Villa [DB]", "marca": "Petroperú", "distrito": "Chorrillos", "direccion": "Av. Defensores del Morro 980", "lat": -12.1820, "lng": -77.0150, "rating": 3.8, "servicios": ["Diésel", "Tienda"]},
    # Villa El Salvador
    {"id": "ves-1", "nombre": "Repsol Villa El Salvador [DB]", "marca": "Repsol", "distrito": "Villa El Salvador", "direccion": "Av. Pastor Sevilla 850", "lat": -12.2180, "lng": -76.9390, "rating": 4.2, "servicios": ["Tienda", "Baño", "Diésel"]},
    # Callao
    {"id": "cal-1", "nombre": "Repsol Callao Saenz Peña [DB]", "marca": "Repsol", "distrito": "Callao", "direccion": "Av. Sáenz Peña 550", "lat": -12.0560, "lng": -77.1180, "rating": 4.0, "servicios": ["Tienda", "Baño", "24 horas"]},
    {"id": "cal-2", "nombre": "GESA Callao Venezuela [DB]", "marca": "GESA", "distrito": "Callao", "direccion": "Av. Venezuela 3850", "lat": -12.0490, "lng": -77.1050, "rating": 3.9, "servicios": ["Diésel", "Aire", "Agua"]},
]

PRECIOS = {
    "uni-1":  {"regular": 15.90, "premium": 21.10, "diesel": 14.85},
    "uni-2":  {"regular": 14.80, "premium": 19.70, "diesel": 15.30},
    "uni-3":  {"regular": 15.45, "premium": 20.20, "diesel": 13.90},
    "uni-4":  {"regular": 15.20, "premium": 18.30, "diesel": 14.60},
    "uni-5":  {"regular": 17.40, "premium": 19.10, "diesel": 14.95},
    "uni-6":  {"regular": 16.80, "premium": 20.90, "diesel": 15.70},
    "uni-7":  {"regular": 16.10, "premium": 19.40, "diesel": 16.20},
    "uni-8":  {"regular": 15.65, "premium": 20.50, "diesel": 14.40},
    "uni-9":  {"regular": 16.35, "premium": 18.95, "diesel": 15.05},
    "uni-10": {"regular": 15.05, "premium": 20.05, "diesel": 14.10},
    "mfl-1":  {"regular": 17.20, "premium": 22.50, "diesel": 16.80},
    "mfl-2":  {"regular": 16.90, "premium": 21.80, "diesel": 16.20},
    "mfl-3":  {"regular": 16.50, "premium": 21.20, "diesel": 15.90},
    "si-1":   {"regular": 17.40, "premium": 22.80, "diesel": 16.90},
    "si-2":   {"regular": 17.10, "premium": 22.40, "diesel": 16.60},
    "sb-1":   {"regular": 16.30, "premium": 21.00, "diesel": 15.70},
    "sb-2":   {"regular": 15.80, "premium": 20.40, "diesel": 15.10},
    "sur-1":  {"regular": 16.70, "premium": 21.60, "diesel": 16.00},
    "sur-2":  {"regular": 16.40, "premium": 21.10, "diesel": 15.60},
    "sur-3":  {"regular": 15.95, "premium": 20.60, "diesel": 15.20},
    "lm-1":   {"regular": 16.20, "premium": 21.30, "diesel": 15.50},
    "lm-2":   {"regular": 15.90, "premium": 20.90, "diesel": 15.20},
    "ate-1":  {"regular": 15.30, "premium": 19.80, "diesel": 14.50},
    "ate-2":  {"regular": 14.90, "premium": 19.20, "diesel": 14.10},
    "lo-1":   {"regular": 15.50, "premium": 20.10, "diesel": 14.70},
    "lo-2":   {"regular": 15.10, "premium": 19.60, "diesel": 14.30},
    "sm-1":   {"regular": 16.00, "premium": 20.80, "diesel": 15.30},
    "sm-2":   {"regular": 15.75, "premium": 20.50, "diesel": 15.00},
    "cl-1":   {"regular": 15.40, "premium": 19.90, "diesel": 14.60},
    "cl-2":   {"regular": 14.70, "premium": 19.10, "diesel": 14.00},
    "jm-1":   {"regular": 16.10, "premium": 20.70, "diesel": 15.40},
    "lin-1":  {"regular": 15.85, "premium": 20.30, "diesel": 15.10},
    "bar-1":  {"regular": 16.60, "premium": 21.40, "diesel": 15.80},
    "cho-1":  {"regular": 15.60, "premium": 20.20, "diesel": 14.80},
    "cho-2":  {"regular": 15.00, "premium": 19.50, "diesel": 14.20},
    "ves-1":  {"regular": 14.80, "premium": 19.30, "diesel": 13.90},
    "cal-1":  {"regular": 15.20, "premium": 19.70, "diesel": 14.40},
    "cal-2":  {"regular": 14.60, "premium": 19.00, "diesel": 13.80},
}

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Base de datos anterior eliminada: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE estaciones (
        id TEXT PRIMARY KEY,
        nombre TEXT,
        marca TEXT,
        distrito TEXT,
        direccion TEXT,
        lat REAL,
        lng REAL,
        rating REAL,
        servicios TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE precios (
        grifo_id TEXT PRIMARY KEY,
        regular REAL,
        premium REAL,
        diesel REAL,
        FOREIGN KEY(grifo_id) REFERENCES estaciones(id)
    )
    ''')

    for g in GRIFOS:
        cursor.execute('''
        INSERT INTO estaciones (id, nombre, marca, distrito, direccion, lat, lng, rating, servicios)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (g["id"], g["nombre"], g["marca"], g["distrito"], g["direccion"], g["lat"], g["lng"], g["rating"], json.dumps(g["servicios"])))

    for gid, p in PRECIOS.items():
        cursor.execute('''
        INSERT INTO precios (grifo_id, regular, premium, diesel)
        VALUES (?, ?, ?, ?)
        ''', (gid, p["regular"], p["premium"], p["diesel"]))

    conn.commit()
    conn.close()
    print("Base de datos facilito.db creada y poblada exitosamente.")

if __name__ == "__main__":
    init_db()
