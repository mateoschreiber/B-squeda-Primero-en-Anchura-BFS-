import unittest

from junta_saneamiento.bfs import breadth_first_search, reconstruct_path
from junta_saneamiento.network import Network, Node, load_network


class BFSTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.network = load_network("data/red_sensores.json")

    def test_main_scenario(self):
        result = breadth_first_search(self.network, "S1")
        self.assertEqual(result.visit_order, ["S1", "S2", "S3", "S4", "S5", "S6", "S7"])
        self.assertEqual(result.levels, {"S1": 0, "S2": 1, "S3": 1, "S4": 2, "S5": 2, "S6": 2, "S7": 3})
        self.assertEqual(reconstruct_path(result, "S7"), ["S1", "S2", "S4", "S7"])

    def test_cycle_and_other_origin(self):
        result = breadth_first_search(self.network, "S3")
        self.assertEqual(result.levels["S3"], 0)
        cycle = Network("test", {"A": Node("A", "A", ""), "B": Node("B", "B", ""), "C": Node("C", "C", "")}, {"A": ("B", "C"), "B": ("A", "C"), "C": ("A", "B")})
        result = breadth_first_search(cycle, "A")
        self.assertEqual(result.visit_order, ["A", "B", "C"])
        self.assertEqual(len(result.visit_order), len(set(result.visit_order)))

    def test_isolated_node_and_invalid_origin(self):
        isolated = Network("test", {"A": Node("A", "A", ""), "B": Node("B", "B", "")}, {"A": (), "B": ()})
        result = breadth_first_search(isolated, "A")
        self.assertEqual(result.unreachable, ["B"])
        self.assertIsNone(reconstruct_path(result, "B"))
        with self.assertRaisesRegex(ValueError, "no existe"):
            breadth_first_search(self.network, "X")
