# Diseño de optimización BFS

## Objetivo

Reducir el código al mínimo razonable sin alterar el comportamiento exigido por la demostración: cargar una red desde JSON, recorrerla con BFS, mostrar niveles, reconstruir la ruta con menos conexiones, identificar nodos no alcanzables y ejecutar cinco escenarios didácticos desde la consola.

## Restricciones

- Usar Python 3.11 o superior y únicamente su biblioteca estándar.
- Conservar `data/red_sensores.json` como red base editable.
- Conservar las opciones `--red`, `--origen`, `--destino` y `--escenario`.
- Conservar los cinco escenarios y sus resultados observables.
- No conservar la API pública anterior de funciones de escenario.
- Documentar todas las funciones con docstrings y comentar solamente decisiones cuya intención no sea evidente.
- Explicar el proyecto completo en `README.md`.

## Arquitectura

La implementación tendrá dos módulos funcionales. `core.py` contendrá la carga y validación del JSON, las modificaciones temporales de escenarios, BFS y reconstrucción de rutas. `cli.py` contendrá el análisis de argumentos y el formato del reporte. `__main__.py` seguirá siendo el punto de entrada de `python -m junta_saneamiento`.

Se eliminarán `network.py`, `bfs.py` y `scenarios.py`, junto con las dataclasses y exportaciones que solo sostenían la API anterior. La red se representará con diccionarios y listas, suficientes para este enunciado y más compactos que los modelos actuales.

## Flujo de datos

1. La consola selecciona el JSON base y los valores predeterminados `S1` y `S7`.
2. La carga valida nodos, conexiones, orden de vecinos y texto de alerta.
3. Si hay un escenario, se modifica una copia en memoria de la red.
4. BFS devuelve orden de visita, niveles, predecesores y nodos no alcanzables.
5. La ruta se reconstruye desde el destino siguiendo predecesores.
6. La consola muestra el mismo reporte didáctico y devuelve código `0` o `2`.

## Errores

El programa rechazará JSON ilegible o incoherente, origen o destino inexistentes y combinaciones incompatibles con `--escenario`. Todos estos casos producirán un mensaje iniciado por `Error:` y código de salida `2`.

## Pruebas

Las pruebas usarán `unittest` y código real, sin mocks. Cubrirán la red válida, datos inválidos, BFS desde distintos orígenes, ciclos, nodos aislados, reconstrucción de rutas, cinco escenarios, equivalencia de resultados observables en la consola y opciones incompatibles.

## Documentación

El README será la referencia única para principiantes: objetivo, estructura, datos, algoritmo BFS, comandos, escenarios, salida, pruebas, complejidad y limitaciones. La documentación secundaria podrá permanecer como material complementario, pero no será necesaria para comprender o ejecutar el proyecto.
