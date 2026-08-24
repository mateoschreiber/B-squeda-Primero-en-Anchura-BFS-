# Guía paso a paso para principiantes

Estos pasos usan Windows y PowerShell. Ejecuta los comandos desde la carpeta del repositorio.

## 1. Obtener y abrir el proyecto

Si el repositorio ya está en tu equipo, ábrelo en PowerShell:

```powershell
cd "C:\ruta\al\bfs-junta-saneamiento"
```

Si está publicado en GitHub, primero clónalo y entra a la carpeta:

```powershell
git clone URL_DEL_REPOSITORIO
cd bfs-junta-saneamiento
```

Debes ver archivos como `README.md`, `pyproject.toml`, `data` y `src`.

## 2. Comprobar Python

```powershell
python --version
```

Debes obtener Python 3.11 o una versión superior. Si el comando no funciona, instala Python y vuelve a abrir PowerShell.

## 3. Instalar el proyecto localmente

```powershell
python -m pip install -e .
```

La opción `-e` permite ejecutar el proyecto mientras lo estudias o modificas. No se instalan bibliotecas externas.

## 4. Ejecutar la demostración

```powershell
python -m junta_saneamiento
```

Debes observar que S1 es el origen, S2 y S3 aparecen en el nivel 1, y la ruta a S7 es `S1 -> S2 -> S4 -> S7`.

## 5. Probar otros puntos

```powershell
python -m junta_saneamiento --origen S3 --destino S7
```

Ahora S3 debe aparecer en el nivel 0. Puedes cambiar los identificadores por S1 a S7. Si escribes uno inexistente, el programa muestra un error claro y termina con código 2.

## 6. Ejecutar las pruebas

```powershell
python -m unittest discover -s tests -v
```

Debes ver `OK`. Esto confirma que la ruta principal, ciclos, nodos aislados y configuraciones inválidas funcionan como se espera.

## 7. Entender dónde modificar cada cosa

- Para cambiar los puntos o conexiones, edita `data/red_sensores.json`.
- Para estudiar el recorrido BFS, lee `src/junta_saneamiento/bfs.py`.
- Para cambiar las opciones o la salida, revisa `src/junta_saneamiento/cli.py`.

Después de cambiar el JSON, ejecuta otra vez las pruebas para comprobar que la red sigue siendo válida.

## 8. Preparar un commit

```powershell
git status
git add README.md docs data src tests pyproject.toml .gitignore
git commit -m "docs: mejorar guía didáctica de BFS"
```

Antes del commit, `git status` no debe mostrar `__pycache__`, entornos virtuales ni carpetas `.egg-info` para subir.
