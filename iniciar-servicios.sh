#!/bin/bash
echo "Levantando microservicios de Facilito UNI con entorno virtual..."

# Detección simple para Windows/Linux
if [ -f "../.venv/Scripts/python.exe" ]; then
    PYTHON_EXEC="../.venv/Scripts/python.exe"
else
    PYTHON_EXEC="../.venv/bin/python"
fi

cd ms-grifos && $PYTHON_EXEC -m uvicorn main:app --port 8001 --reload &
cd ../ms-precios && $PYTHON_EXEC -m uvicorn main:app --port 8002 --reload &
cd ../ms-ubicacion && $PYTHON_EXEC -m uvicorn main:app --port 8003 --reload &

echo ""
echo "Servicios levantados:"
echo "  ms-grifos    -> http://localhost:8001/docs"
echo "  ms-precios   -> http://localhost:8002/docs"
echo "  ms-ubicacion -> http://localhost:8003/docs"
echo ""
echo "Ctrl+C para detener todos"
wait
