# Conectividad en Juntas de Saneamiento con BFS

## Objetivo

Este proyecto demuestra cómo una alerta puede recorrer una red hipotética de una Junta de Saneamiento usando búsqueda en anchura (BFS) en Python.

## Problema representado

Una posible rotura de cañería comienza en un punto de la red. El programa indica en qué orden se alcanza cada punto, a cuántas conexiones está del origen, la ruta más corta en cantidad de enlaces y los puntos aislados.

## Topología S1-S7

`S1 Tanque` conecta con `S2 Bomba` y `S3 Ramal Norte`; `S2` con `S4 Válvula Central` y `S5 Ramal Sur`; `S3` con `S6 Escuela Rural`; `S4` con `S7 Puesto de Salud`.

## Cómo funciona BFS

BFS visita primero los puntos más cercanos al origen. Usa una cola FIFO: el primer punto que entra es el primero que sale.

```text
S1 → S2, S3 → S4, S5, S6 → S7
     nivel 1    nivel 2     nivel 3
```

Por eso, en una red sin pesos, la primera ruta encontrada tiene la menor cantidad de conexiones. No representa distancia física, presión, caudal ni una decisión operativa real.

## Requisitos

Python 3.11 o superior. La aplicación usa únicamente la biblioteca estándar de Python: no requiere frameworks ni paquetes externos en tiempo de ejecución.

## Instalación

```powershell
python -m pip install -e .
```

Consulta la guía completa para principiantes: [docs/guia_paso_a_paso.md](docs/guia_paso_a_paso.md).

## Ejecución

```powershell
python -m junta_saneamiento
python -m junta_saneamiento --origen S1 --destino S7
python -m junta_saneamiento --red data/red_sensores.json --origen S3 --destino S7
```

## Escenarios didácticos

Los escenarios crean variantes temporales en memoria. El archivo `data/red_sensores.json` no cambia.

```powershell
python -m junta_saneamiento --escenario rotura-tanque
python -m junta_saneamiento --escenario rotura-toma-s8
python -m junta_saneamiento --escenario toma-aislada
python -m junta_saneamiento --escenario conexion-interrumpida
python -m junta_saneamiento --escenario origen-inexistente
```

También pueden llamarse directamente desde Python:

```python
from junta_saneamiento import simular_rotura_en_toma_s8

escenario = simular_rotura_en_toma_s8()
print(escenario.resultado.visit_order)
print(escenario.ruta)
```

En este ejemplo la ruta es `S8 -> S5 -> S2 -> S4 -> S7`. Una “toma rota” sólo indica dónde se inicia la alerta simulada; el programa no detecta daños reales.

## Ejemplo de salida

```text
Alerta: Posible rotura de cañería
Origen: S1 - Tanque
Nivel 0: S1 - Tanque
Nivel 1: S2 - Bomba, S3 - Ramal Norte
Nivel 2: S4 - Válvula Central, S5 - Ramal Sur, S6 - Escuela Rural
Nivel 3: S7 - Puesto de Salud
Ruta a S7: S1 -> S2 -> S4 -> S7
No alcanzables: ninguno
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

BFS usa `collections.deque`, marca un nodo antes de encolarlo, funciona en O(V + E) y devuelve rutas con la menor cantidad de conexiones. Las 13 pruebas verifican el algoritmo, la carga de datos, los cinco escenarios y la consola.

## Diseño mínimo

- `network.py`: lee y valida el JSON.
- `bfs.py`: contiene el algoritmo y reconstruye rutas.
- `scenarios.py`: copia la red y aplica cambios temporales visibles.
- `cli.py`: recibe argumentos y presenta el resultado.

No hay clases, capas, dependencias ni abstracciones adicionales fuera de las necesarias para esas cuatro tareas.

## Materiales de exposición

- [Plan de ejecución actualizado](docs/entrega/Plan_Ejecucion_BFS_Junta_Saneamiento_Corregido.pdf)
- [Presentación BFS de 5 minutos](docs/entrega/Presentacion_BFS_Junta_Saneamiento_5min.pptx)

## Estructura del repositorio

`data/` contiene la topología JSON; `src/junta_saneamiento/` contiene la carga, BFS, escenarios y CLI; `tests/` contiene las pruebas; y `docs/` explica arquitectura y casos manuales.

## Limitaciones

No integra dispositivos ni datos reales. No calcula presión, caudal, distancia ni tiempo hidráulico. Una ruta BFS minimiza conexiones, no una decisión técnica u operativa.
