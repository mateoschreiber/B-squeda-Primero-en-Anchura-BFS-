"""Búsqueda en anchura independiente de la interfaz."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from .network import Network


@dataclass(frozen=True)
class BFSResult:
    visit_order: list[str]
    levels: dict[str, int]
    predecessors: dict[str, str | None]
    unreachable: list[str]


def breadth_first_search(network: Network, origin: str) -> BFSResult:
    if origin not in network.nodes:
        raise ValueError(f"El origen '{origin}' no existe en la red.")
    # La cola FIFO garantiza que se visiten primero los puntos más cercanos.
    queue: deque[str] = deque([origin])
    visited = {origin}
    order: list[str] = []
    levels = {origin: 0}
    predecessors: dict[str, str | None] = {origin: None}
    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in network.neighbors[current]:
            if neighbor not in visited:
                # Se marca antes de encolar para impedir visitas duplicadas en ciclos.
                visited.add(neighbor)
                # Todo vecino nuevo queda a una conexión más que el punto actual.
                levels[neighbor] = levels[current] + 1
                # Guardar de dónde vino permite reconstruir la ruta después.
                predecessors[neighbor] = current
                queue.append(neighbor)
    return BFSResult(order, levels, predecessors, [node for node in network.nodes if node not in visited])


def reconstruct_path(result: BFSResult, destination: str) -> list[str] | None:
    if destination not in result.predecessors:
        return None
    path: list[str] = []
    current: str | None = destination
    while current is not None:
        path.append(current)
        # Se avanza hacia el origen siguiendo los predecesores guardados por BFS.
        current = result.predecessors[current]
    return list(reversed(path))
