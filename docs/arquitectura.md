# Arquitectura explicada de forma simple

## Qué hace cada parte

| Parte | Qué hace | Por qué está separada |
| --- | --- | --- |
| `data/red_sensores.json` | Guarda los puntos y sus conexiones. | Cambiar la red no exige cambiar Python. |
| `network.py` | Lee y revisa que los datos sean coherentes. | Evita ejecutar el algoritmo con una red mal escrita. |
| `bfs.py` | Recorre la red y calcula niveles y rutas. | El algoritmo se puede probar sin usar la consola. |
| `cli.py` | Recibe opciones y muestra un reporte. | La presentación no se mezcla con la lógica. |

## Flujo del programa

```text
JSON de la red → validación → BFS desde el origen → reporte en consola
```

La red es un grafo no dirigido y no ponderado: si S1 conecta con S2, S2 también conecta con S1, y todos los enlaces cuentan igual. BFS usa una cola FIFO, una lista de visitados, niveles y predecesores. Marcar un punto antes de añadirlo a la cola evita visitas repetidas en redes con ciclos.

El recorrido tarda O(V + E): depende de la cantidad de puntos (V) y conexiones (E). La ruta minimiza enlaces, no distancia física, tiempo hidráulico ni prioridad operativa. Es una simulación académica, no un sistema de control real.
