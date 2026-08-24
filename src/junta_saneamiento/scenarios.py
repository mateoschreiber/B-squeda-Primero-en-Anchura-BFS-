"""Escenarios didácticos construidos sin modificar la red original."""
from dataclasses import dataclass

from .bfs import BFSResult, breadth_first_search, reconstruct_path
from .network import DEFAULT_NETWORK_PATH, Network, Node, load_network


@dataclass(frozen=True)
class ResultadoEscenario:
    """Datos completos de una simulación, listos para explorar desde Python."""

    nombre: str
    explicacion: str
    red: Network
    origen: str
    destino: str
    resultado: BFSResult
    ruta: list[str] | None


def _copiar_red(red):
    """Devuelve copias modificables; la red original queda intacta."""
    return dict(red.nodes), {node_id: list(vecinos) for node_id, vecinos in red.neighbors.items()}


def _crear_red(red, nodos, vecinos):
    vecinos = {node_id: tuple(lista) for node_id, lista in vecinos.items()}
    return Network(red.alert, nodos, vecinos)


def _ejecutar(
    nombre: str,
    explicacion: str,
    red: Network,
    origen: str = "S1",
    destino: str = "S7",
) -> ResultadoEscenario:
    resultado = breadth_first_search(red, origen)
    return ResultadoEscenario(
        nombre, explicacion, red, origen, destino, resultado, reconstruct_path(resultado, destino)
    )


def simular_rotura_en_tanque() -> ResultadoEscenario:
    """Propaga desde el tanque S1 hasta la toma S7 en la red original."""
    red = load_network(DEFAULT_NETWORK_PATH)
    return _ejecutar(
        "Rotura en tanque",
        "La alerta comienza en S1 y recorre la red original hasta S7.",
        red,
    )


def simular_rotura_en_toma_s8() -> ResultadoEscenario:
    """Añade S8 conectado a S5 y propaga su alerta hasta S7."""
    red = load_network(DEFAULT_NETWORK_PATH)
    nodos, vecinos = _copiar_red(red)
    nodos["S8"] = Node("S8", "Toma comunitaria 8", "Origen de la alerta")
    # Una conexión no dirigida se guarda en ambos sentidos.
    vecinos["S8"] = ["S5"]
    vecinos["S5"].append("S8")
    red = _crear_red(red, nodos, vecinos)
    return _ejecutar(
        "Rotura en toma S8",
        "Se añade S8 junto a S5 y la alerta viaja desde esa nueva toma hasta S7.",
        red,
        origen="S8",
    )


def simular_toma_aislada() -> ResultadoEscenario:
    """Añade S9 sin conexiones para mostrar un punto no alcanzable."""
    red = load_network(DEFAULT_NETWORK_PATH)
    nodos, vecinos = _copiar_red(red)
    nodos["S9"] = Node("S9", "Toma aislada 9", "Toma sin conexión")
    vecinos["S9"] = []
    red = _crear_red(red, nodos, vecinos)
    return _ejecutar(
        "Toma aislada",
        "S9 se añade sin conexiones; por eso una alerta iniciada en S1 no puede alcanzarla.",
        red,
        destino="S9",
    )


def simular_conexion_interrumpida() -> ResultadoEscenario:
    """Retira S2-S4 para mostrar la parte de la red que queda separada."""
    red = load_network(DEFAULT_NETWORK_PATH)
    nodos, vecinos = _copiar_red(red)
    # También se retira en ambos sentidos porque la red es no dirigida.
    vecinos["S2"].remove("S4")
    vecinos["S4"].remove("S2")
    red = _crear_red(red, nodos, vecinos)
    return _ejecutar(
        "Conexión interrumpida",
        "Al retirar S2-S4, los puntos S4 y S7 dejan de ser alcanzables desde S1.",
        red,
    )


def simular_origen_inexistente() -> ResultadoEscenario:
    """Intenta iniciar en S99 y deja que BFS produzca su error didáctico."""
    red = load_network(DEFAULT_NETWORK_PATH)
    return _ejecutar(
        "Origen inexistente",
        "S99 no está declarado; BFS rechaza el origen con un mensaje comprensible.",
        red,
        origen="S99",
    )


ESCENARIOS = {
    "rotura-tanque": simular_rotura_en_tanque,
    "rotura-toma-s8": simular_rotura_en_toma_s8,
    "toma-aislada": simular_toma_aislada,
    "conexion-interrumpida": simular_conexion_interrumpida,
    "origen-inexistente": simular_origen_inexistente,
}
