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

La opción `-e` permite ejecutar el proyecto mientras lo estudias o modificas. La aplicación no instala bibliotecas externas: sólo usa módulos incluidos con Python.

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

Debes ver `Ran 13 tests` y `OK`. Esto confirma que la ruta principal, ciclos, nodos aislados, escenarios, consola y configuraciones inválidas funcionan como se espera.

## 7. Simular comportamientos sin editar el JSON

Ejecuta, por ejemplo:

```powershell
python -m junta_saneamiento --escenario rotura-toma-s8
```

Debes observar que aparece S8, que su nivel es 0 y que la ruta es `S8 -> S5 -> S2 -> S4 -> S7`. S8 sólo existe durante esa ejecución.

Los cinco escenarios disponibles son:

| Escenario | Qué debes observar |
| --- | --- |
| `rotura-tanque` | Usa la red original desde S1 hasta S7. |
| `rotura-toma-s8` | Añade S8 conectado a S5 en ambos sentidos. |
| `toma-aislada` | Añade S9 sin conexiones; aparece como no alcanzable. |
| `conexion-interrumpida` | Retira S2-S4; S4 y S7 quedan no alcanzables. |
| `origen-inexistente` | S99 produce un error claro y código de salida 2. |

No combines `--escenario` con `--red`, `--origen` ni `--destino`. Son dos formas diferentes de ejecutar el programa.

## 8. Llamar un escenario desde Python

Abre Python desde PowerShell:

```powershell
python
```

Luego escribe:

```python
from junta_saneamiento import simular_rotura_en_toma_s8
escenario = simular_rotura_en_toma_s8()
print(escenario.resultado.visit_order)
print(escenario.ruta)
exit()
```

Debes obtener el orden de visita y la misma ruta que muestra la consola. Puedes reemplazar la función por `simular_rotura_en_tanque`, `simular_toma_aislada` o `simular_conexion_interrumpida`. `simular_origen_inexistente` genera un `ValueError` de forma intencional.

## 9. Entender dónde modificar cada cosa

- Para cambiar los puntos o conexiones, edita `data/red_sensores.json`.
- Para estudiar el recorrido BFS, lee `src/junta_saneamiento/bfs.py`.
- Para estudiar variantes temporales, lee `src/junta_saneamiento/scenarios.py`.
- Para cambiar las opciones o la salida, revisa `src/junta_saneamiento/cli.py`.

El proyecto mantiene una responsabilidad por archivo y ayudantes pequeños para copiar, reconstruir y ejecutar escenarios. No necesitas aprender frameworks para entenderlo.

Después de cambiar el JSON, ejecuta otra vez las pruebas para comprobar que la red sigue siendo válida.

## 10. Preparar un commit

```powershell
git status
git add README.md docs data src tests pyproject.toml .gitignore
git commit -m "feat: añadir escenarios didácticos de BFS"
```

Antes del commit, `git status` no debe mostrar `__pycache__`, entornos virtuales ni carpetas `.egg-info` para subir.
