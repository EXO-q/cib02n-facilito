# MICROSERVICIO — UBICACION

# Imagen base de Python 3.12 en su versión 'slim' (Alpine)
FROM python:3.12-slim

# PYTHONDONTWRITEBYTECODE=1 — Evita que Python genere archivos .pyc (ahorra espacio en el contenedor)
# PYTHONUNBUFFERED=1 — Muestra los logs en tiempo real (sin guardarlos en buffer)
# PORT=8003 — Variable de entorno que indica el puerto expuesto por el microservicio
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8003

# Directorio de trabajo
WORKDIR /app

# Copia de la lista de dependencias al contenedor
# (Para aprovechar el caché de Docker)
COPY requirements.txt .

# Instalación de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia del resto de archivos
COPY . .

# Exposición del puerto
EXPOSE ${PORT}

# Arranque del servidor (usando uvicorn para FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
