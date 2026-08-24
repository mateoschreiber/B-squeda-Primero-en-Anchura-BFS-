"""Demostración básica de BFS en una red de saneamiento."""

from collections import deque


# Cada punto indica con cuáles puntos está conectado directamente.
RED = {
    "S1 - Tanque": ["S2 - Bomba", "S3 - Ramal Norte"],
    "S2 - Bomba": ["S1 - Tanque", "S4 - Valvula Central", "S5 - Ramal Sur"],
    "S3 - Ramal Norte": ["S1 - Tanque", "S6 - Escuela Rural"],
    "S4 - Valvula Central": ["S2 - Bomba", "S7 - Puesto de Salud"],
    "S5 - Ramal Sur": ["S2 - Bomba"],
    "S6 - Escuela Rural": ["S3 - Ramal Norte"],
    "S7 - Puesto de Salud": ["S4 - Valvula Central"],
}


def bfs(red, inicio):
    """Recorre la red por niveles y devuelve el orden de propagación."""
    cola, visitados, orden, nivel = deque([inicio]), {inicio}, [], 0

    while cola:
        etapa = []
        # Los elementos actualmente en la cola pertenecen al mismo nivel.
        for _ in range(len(cola)):
            punto = cola.popleft()
            etapa.append(punto)
            orden.append(punto)

            for vecino in red[punto]:
                if vecino not in visitados:
                    # Se marca al encolar para no repetir puntos en redes con ciclos.
                    visitados.add(vecino)
                    cola.append(vecino)

        print(f"Nivel {nivel}: {' | '.join(etapa)}")
        nivel += 1

    return orden


print("PROPAGACION DE UNA ALERTA DE ROTURA\n")
resultado = bfs(RED, "S1 - Tanque")
print("\nOrden BFS:")
print(" -> ".join(punto.split(" - ")[0] for punto in resultado))
