"""Interfaz de consola de la demostración."""
import argparse
from pathlib import Path
from .bfs import breadth_first_search, reconstruct_path
from .network import DEFAULT_NETWORK_PATH, NetworkConfigurationError, load_network
from .scenarios import ESCENARIOS


def _mostrar_reporte(red, origen, destino, resultado, ruta):
    print(f"Alerta: {red.alert}")
    print(f"Origen: {origen} - {red.nodes[origen].name}")
    # Se agrupan los puntos por nivel para mostrar cómo se expande la alerta.
    for nivel in range(max(resultado.levels.values()) + 1):
        puntos = [nodo for nodo in resultado.visit_order if resultado.levels[nodo] == nivel]
        nombres = ", ".join(f"{nodo} - {red.nodes[nodo].name}" for nodo in puntos)
        print(f"Nivel {nivel}: {nombres}")
    print(f"Ruta a {destino}: {' -> '.join(ruta) if ruta else 'no disponible'}")
    no_alcanzables = ", ".join(resultado.unreachable) or "ninguno"
    print(f"No alcanzables: {no_alcanzables}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulación BFS de una red de saneamiento.")
    parser.add_argument("--red", type=Path, help="Archivo JSON de la red.")
    parser.add_argument("--origen", help="Identificador del origen.")
    parser.add_argument("--destino", help="Identificador del destino.")
    parser.add_argument("--escenario", choices=ESCENARIOS, help="Escenario didáctico predefinido.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.escenario and any(value is not None for value in (args.red, args.origen, args.destino)):
        print("Error: --escenario no se puede combinar con --red, --origen ni --destino.")
        return 2
    try:
        if args.escenario:
            escenario = ESCENARIOS[args.escenario]()
            red, origen, destino = escenario.red, escenario.origen, escenario.destino
            resultado, ruta = escenario.resultado, escenario.ruta
        else:
            red = load_network(args.red or DEFAULT_NETWORK_PATH)
            origen, destino = args.origen or "S1", args.destino or "S7"
            if destino not in red.nodes:
                raise ValueError(f"El destino '{destino}' no existe en la red.")
            resultado = breadth_first_search(red, origen)
            ruta = reconstruct_path(resultado, destino)
    except (OSError, NetworkConfigurationError, ValueError) as error:
        print(f"Error: {error}")
        return 2

    if args.escenario:
        print(f"Escenario: {escenario.nombre}")
        print(f"Explicación: {escenario.explicacion}")
    _mostrar_reporte(red, origen, destino, resultado, ruta)
    return 0
