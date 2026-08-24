import io
import unittest
from contextlib import redirect_stdout

from junta_saneamiento import (
    ResultadoEscenario,
    simular_conexion_interrumpida,
    simular_origen_inexistente,
    simular_rotura_en_tanque,
    simular_rotura_en_toma_s8,
    simular_toma_aislada,
)
from junta_saneamiento.cli import main
from junta_saneamiento.network import DEFAULT_NETWORK_PATH, load_network


class ScenarioTests(unittest.TestCase):
    def test_rotura_en_tanque_usa_la_red_original(self):
        escenario = simular_rotura_en_tanque()
        self.assertIsInstance(escenario, ResultadoEscenario)
        self.assertEqual(list(escenario.red.nodes), ["S1", "S2", "S3", "S4", "S5", "S6", "S7"])
        self.assertEqual(escenario.ruta, ["S1", "S2", "S4", "S7"])

    def test_rotura_en_s8_agrega_conexion_bidireccional_sin_mutar_la_base(self):
        escenario = simular_rotura_en_toma_s8()
        self.assertIn("S5", escenario.red.neighbors["S8"])
        self.assertIn("S8", escenario.red.neighbors["S5"])
        self.assertEqual(escenario.ruta, ["S8", "S5", "S2", "S4", "S7"])
        self.assertNotIn("S8", load_network(DEFAULT_NETWORK_PATH).nodes)

    def test_toma_aislada_aparece_como_no_alcanzable(self):
        escenario = simular_toma_aislada()
        self.assertEqual(escenario.red.neighbors["S9"], ())
        self.assertIn("S9", escenario.resultado.unreachable)
        self.assertIsNone(escenario.ruta)

    def test_conexion_interrumpida_desconecta_s4_y_s7(self):
        escenario = simular_conexion_interrumpida()
        self.assertNotIn("S4", escenario.red.neighbors["S2"])
        self.assertNotIn("S2", escenario.red.neighbors["S4"])
        self.assertEqual(escenario.resultado.unreachable, ["S4", "S7"])
        self.assertIsNone(escenario.ruta)

    def test_origen_inexistente_conserva_el_error_didactico(self):
        with self.assertRaisesRegex(ValueError, "El origen 'S99' no existe"):
            simular_origen_inexistente()

    def test_cli_y_api_entregan_resultados_equivalentes(self):
        esperado = " -> ".join(simular_rotura_en_toma_s8().ruta or [])
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = main(["--escenario", "rotura-toma-s8"])
        self.assertEqual(codigo, 0)
        self.assertIn(f"Ruta a S7: {esperado}", salida.getvalue())

    def test_cli_rechaza_opciones_incompatibles(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            codigo = main(["--escenario", "rotura-tanque", "--origen", "S1"])
        self.assertEqual(codigo, 2)
        self.assertIn("no se puede combinar", salida.getvalue())
