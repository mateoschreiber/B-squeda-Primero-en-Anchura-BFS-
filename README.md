# Búsqueda Primero en Anchura (BFS)

Práctica básica de búsqueda no informada en Python aplicada a una Junta de Saneamiento.

## Problema

Una rotura comienza en el tanque `S1`. Se necesita determinar en qué orden se propaga la alerta por los puntos conectados de la red de agua potable.

```text
S1 Tanque
├── S2 Bomba
│   ├── S4 Válvula Central
│   │   └── S7 Puesto de Salud
│   └── S5 Ramal Sur
└── S3 Ramal Norte
    └── S6 Escuela Rural
```

## Qué es BFS

BFS (*Breadth-First Search*) es una búsqueda no informada: no usa costos ni estimaciones para elegir un camino. Recorre primero todos los puntos cercanos al origen y después avanza al siguiente nivel.

Su flujo es:

```text
Agregar el origen a la cola
          ↓
Sacar el primer punto
          ↓
Visitar sus vecinos no recorridos
          ↓
Agregar esos vecinos al final de la cola
          ↓
Repetir hasta vaciar la cola
```

La cola es FIFO: el primer elemento que entra es el primero que sale.

## Propagación de la alerta

```text
Nivel 0: S1
Nivel 1: S2, S3
Nivel 2: S4, S5, S6
Nivel 3: S7
```

Por lo tanto, el orden BFS es:

```text
S1 → S2 → S3 → S4 → S5 → S6 → S7
```

## Cómo está implementado

Todo está en `bfs.py`:

1. `RED` representa cada punto y sus conexiones mediante un diccionario.
2. `deque` funciona como la cola FIFO.
3. `visitados` evita recorrer un punto más de una vez.
4. El ciclo `while` procesa la red nivel por nivel.
5. La función `bfs` imprime cada etapa y devuelve el orden completo.

Marcar un vecino como visitado antes de encolarlo evita duplicados cuando existen conexiones de ida y vuelta.

## Ejecución

Requiere Python 3.10 o superior y no utiliza paquetes externos.

```powershell
python bfs.py
```

Salida esperada:

```text
PROPAGACIÓN DE UNA ALERTA DE ROTURA

Nivel 0: S1 - Tanque
Nivel 1: S2 - Bomba | S3 - Ramal Norte
Nivel 2: S4 - Valvula Central | S5 - Ramal Sur | S6 - Escuela Rural
Nivel 3: S7 - Puesto de Salud

Orden BFS:
S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7
```

## Complejidad

- Tiempo: `O(V + E)`; se visitan todos los puntos y conexiones.
- Memoria: `O(V)`; se guardan la cola y los puntos visitados.

`V` es la cantidad de puntos y `E` la cantidad de conexiones.

## Limitación

La práctica muestra conectividad. No calcula distancia física, presión, caudal ni tiempo real de propagación.
