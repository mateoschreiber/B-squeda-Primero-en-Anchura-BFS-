# Arquitectura explicada de forma simple

## Qué hace cada parte

| Parte | Qué hace | Por qué está separada |
| --- | --- | --- |
| `data/red_sensores.json` | Guarda los puntos y sus conexiones. | Cambiar la red no exige cambiar Python. |
| `network.py` | Lee y revisa que los datos sean coherentes. | Evita ejecutar el algoritmo con una red mal escrita. |
| `bfs.py` | Recorre la red y calcula niveles y rutas. | El algoritmo se puede probar sin usar la consola. |
| `scenarios.py` | Crea variantes temporales como S8, S9 o una conexión interrumpida. | Permite experimentar sin modificar el JSON original. |
| `cli.py` | Recibe opciones y muestra un reporte. | La presentación no se mezcla con la lógica. |

## Flujo del programa

```text
JSON de la red → validación → BFS desde el origen → reporte en consola
```

Cuando se usa `--escenario`, el flujo es:

```text
JSON original → copia en memoria → cambio controlado → BFS → mismo reporte
```

Los ayudantes privados sólo copian la red, la reconstruyen y ejecutan BFS. Cada función pública muestra directamente el cambio que realiza y devuelve `ResultadoEscenario` con la red, el resultado y la ruta.

La red es un grafo no dirigido y no ponderado: si S1 conecta con S2, S2 también conecta con S1, y todos los enlaces cuentan igual. BFS usa una cola FIFO, una lista de visitados, niveles y predecesores. Marcar un punto antes de añadirlo a la cola evita visitas repetidas en redes con ciclos.

Todo el código de ejecución usa la biblioteca estándar: `argparse`, `collections`, `dataclasses`, `json` y `pathlib`. El recorrido tarda O(V + E). La ruta minimiza enlaces, no distancia física, tiempo hidráulico ni prioridad operativa.
