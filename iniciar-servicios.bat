@echo off
cd /d "%~dp0"
echo Directorio: %CD%
echo.
echo Levantando microservicios de Facilito UNI con el entorno virtual...
echo.

set PYTHON_EXEC="%~dp0.venv\Scripts\python.exe"

start "ms-grifos (8001)" cmd /k "cd /d "%~dp0ms-grifos" && %PYTHON_EXEC% -m uvicorn main:app --port 8001 --reload"
timeout /t 2 /nobreak > nul

start "ms-precios (8002)" cmd /k "cd /d "%~dp0ms-precios" && %PYTHON_EXEC% -m uvicorn main:app --port 8002 --reload"
timeout /t 2 /nobreak > nul

start "ms-ubicacion (8003)" cmd /k "cd /d "%~dp0ms-ubicacion" && %PYTHON_EXEC% -m uvicorn main:app --port 8003 --reload"
timeout /t 2 /nobreak > nul

echo.
echo Servicios levantados:
echo   ms-grifos    -^> http://localhost:8001/docs
echo   ms-precios   -^> http://localhost:8002/docs
echo   ms-ubicacion -^> http://localhost:8003/docs
echo.
pause
