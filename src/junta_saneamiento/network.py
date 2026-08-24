"""Carga y validación de la topología de la red."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class NetworkConfigurationError(ValueError):
    """La topología no cumple el formato esperado."""


@dataclass(frozen=True)
class Node:
    id: str
    name: str
    role: str


@dataclass(frozen=True)
class Network:
    alert: str
    nodes: dict[str, Node]
    neighbors: dict[str, tuple[str, ...]]


def load_network(path: str | Path) -> Network:
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except (OSError, json.JSONDecodeError) as error:
        raise NetworkConfigurationError(f"No se pudo leer la red: {error}") from error
    if not isinstance(raw, dict):
        raise NetworkConfigurationError("La raíz del JSON debe ser un objeto.")
    entries, connections, order = raw.get("nodes"), raw.get("connections"), raw.get("neighbor_order")
    if not isinstance(entries, list) or not isinstance(connections, list) or not isinstance(order, dict):
        raise NetworkConfigurationError("Se requieren 'nodes', 'connections' y 'neighbor_order' válidos.")
    nodes: dict[str, Node] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) and entry[key] for key in ("id", "name", "role")):
            raise NetworkConfigurationError("Cada nodo debe tener id, name y role no vacíos.")
        node = Node(entry["id"], entry["name"], entry["role"])
        if node.id in nodes:
            raise NetworkConfigurationError(f"El identificador '{node.id}' está duplicado.")
        nodes[node.id] = node
    expected = {node_id: set() for node_id in nodes}
    for connection in connections:
        if not isinstance(connection, list) or len(connection) != 2 or not all(isinstance(value, str) for value in connection):
            raise NetworkConfigurationError("Cada conexión debe ser una lista de dos identificadores.")
        left, right = connection
        if left not in nodes or right not in nodes:
            raise NetworkConfigurationError(f"La conexión '{left}' - '{right}' usa un nodo no declarado.")
        if left == right or right in expected[left]:
            raise NetworkConfigurationError(f"La conexión '{left}' - '{right}' es inválida o duplicada.")
        expected[left].add(right)
        expected[right].add(left)
    # Cada nodo debe declarar todos sus vecinos y en el orden que desea mostrar BFS.
    if set(order) != set(nodes):
        raise NetworkConfigurationError("neighbor_order debe definir exactamente todos los nodos.")
    neighbors: dict[str, tuple[str, ...]] = {}
    for node_id, values in order.items():
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise NetworkConfigurationError(f"El orden de vecinos de '{node_id}' no es válido.")
        if len(values) != len(set(values)) or set(values) != expected[node_id]:
            raise NetworkConfigurationError(f"El orden de vecinos de '{node_id}' no coincide con sus conexiones.")
        neighbors[node_id] = tuple(values)
    alert = raw.get("alert", "Alerta sin descripción")
    if not isinstance(alert, str) or not alert:
        raise NetworkConfigurationError("'alert' debe ser un texto no vacío.")
    return Network(alert, nodes, neighbors)
