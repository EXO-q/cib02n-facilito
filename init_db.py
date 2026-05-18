from pathlib import Path
import sqlite3
import json

# Directorios importantes
W_DIR = Path(__file__).parent
JSON_DIR = W_DIR / "datos-prueba"

# Archivos importantes
GRIFOS_JSON = JSON_DIR / "grifos.json"
PRECIOS_JSON  = JSON_DIR / "precios.json"

def init_db(db: Path) -> None:
    # Sobreescritura de los datos
    db.unlink(missing_ok=True)
    
    # Carga de datos desde archivos JSON
    with GRIFOS_JSON.open(mode='r', encoding='utf-8') as f:
        grifos_data = json.load(f)
    
    with PRECIOS_JSON.open(mode='r', encoding='utf-8') as f:
        precios_data = json.load(f)
    
    # Creación de la base de datos
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    cur.execute('''
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
    
    cur.execute('''
        CREATE TABLE precios (
            grifo_id TEXT PRIMARY KEY,
            regular REAL,
            premium REAL,
            diesel REAL,
            FOREIGN KEY(grifo_id) REFERENCES estaciones(id)
        )
    ''')
    
    for g in grifos_data:
        cur.execute('INSERT INTO estaciones VALUES (?,?,?,?,?,?,?,?,?)',
                    (g['id'], g['nombre'], g['marca'], g['distrito'],
                     g['direccion'], g['lat'], g['lng'], g['rating'],
                     json.dumps(g['servicios'])))
    
    for gid, p in precios_data.items():
        cur.execute('INSERT INTO precios VALUES (?,?,?,?)',
                    (gid, p['regular'], p['premium'], p['diesel']))
    
    conn.commit()
    conn.close()

    print("Base de datos creada y poblada exitosamente.")
    print("Ruta:", db.absolute())

if __name__ == '__main__':
    SUFFIX: str = "app/facilito.db"
    ms_grifos_db = W_DIR / f"ms-grifos/{SUFFIX}"
    ms_precios_db = W_DIR / f"ms-precios/{SUFFIX}"
    ms_ubicacion_db = W_DIR / f"ms-ubicacion/{SUFFIX}"

    init_db(ms_grifos_db)
    init_db(ms_precios_db)
    init_db(ms_ubicacion_db)
