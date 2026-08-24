import json
import tempfile
import unittest
from pathlib import Path

from junta_saneamiento.network import NetworkConfigurationError, load_network


class NetworkTests(unittest.TestCase):
    def write_json(self, payload):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "network.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_loads_valid_network(self):
        self.assertEqual(load_network("data/red_sensores.json").neighbors["S2"], ("S1", "S4", "S5"))

    def test_rejects_bad_references_and_order(self):
        unknown = {
            "nodes": [{"id": "A", "name": "A", "role": "test"}],
            "connections": [["A", "B"]],
            "neighbor_order": {"A": []},
        }
        with self.assertRaisesRegex(NetworkConfigurationError, "no declarado"):
            load_network(self.write_json(unknown))

        bad_order = {
            "nodes": [
                {"id": "A", "name": "A", "role": "test"},
                {"id": "B", "name": "B", "role": "test"},
            ],
            "connections": [["A", "B"]],
            "neighbor_order": {"A": [], "B": ["A"]},
        }
        with self.assertRaisesRegex(NetworkConfigurationError, "no coincide"):
            load_network(self.write_json(bad_order))

    def test_rejects_invalid_json(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / "invalid.json"
        path.write_text("{", encoding="utf-8")
        with self.assertRaises(NetworkConfigurationError):
            load_network(path)
