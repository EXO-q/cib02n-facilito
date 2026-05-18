# MICROSERVICIO - GRIFOS

# Imagen base: Python 3.12 en Alpine
FROM python:3.12-slim

# Evita que Python genere archivos .pyc (bytecode compilado)
# y que bufferee la salida — los logs aparecen en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Se copia solo 'requirements.txt' (optimización de caché de Docker)
# Si el código cambia pero las dependencias no, Docker reutiliza esta capa
COPY requirements.txt .

# Se instalan dependencias sin guardar caché de pip (reduce tamaño de imagen)
RUN pip install --no-cache-dir -r requirements.txt

# Se copia el resto del código
COPY . .

# Puerto que expone este servicio
EXPOSE 8001

# Comando para arrancar el servidor (usando uvicorn para FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
