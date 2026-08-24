"""Interfaz de consola de la demostración."""
from __future__ import annotations

import argparse
from pathlib import Path
from .bfs import breadth_first_search, reconstruct_path
from .network import NetworkConfigurationError, load_network

DEFAULT_NETWORK = Path(__file__).resolve().parents[2] / "data" / "red_sensores.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulación BFS de una red de saneamiento.")
    parser.add_argument("--red", type=Path, default=DEFAULT_NETWORK, help="Archivo JSON de la red.")
    parser.add_argument("--origen", default="S1", help="Identificador del origen.")
    parser.add_argument("--destino", default="S7", help="Identificador del destino.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        network = load_network(args.red)
        if args.destino not in network.nodes:
            raise ValueError(f"El destino '{args.destino}' no existe en la red.")
        result = breadth_first_search(network, args.origen)
    except (OSError, NetworkConfigurationError, ValueError) as error:
        print(f"Error: {error}")
        return 2
    print(f"Alerta: {network.alert}")
    print(f"Origen: {args.origen} - {network.nodes[args.origen].name}")
    # Se agrupan los puntos por nivel para mostrar cómo se expande la alerta.
    for level in range(max(result.levels.values()) + 1):
        sensors = [node for node in result.visit_order if result.levels[node] == level]
        print(f"Nivel {level}: {', '.join(f'{node} - {network.nodes[node].name}' for node in sensors)}")
    path = reconstruct_path(result, args.destino)
    print(f"Ruta a {args.destino}: {' -> '.join(path) if path else 'no disponible'}")
    print(f"No alcanzables: {', '.join(result.unreachable) if result.unreachable else 'ninguno'}")
    return 0
