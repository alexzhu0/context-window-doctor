import json
import tempfile
import unittest
from pathlib import Path

from context_window_doctor.cli import analyze_context, run


class ContextWindowDoctorTests(unittest.TestCase):
    def test_finds_duplicates_and_stale_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "context.md"
            path.write_text("Use tests.\nUse tests.\nTODO legacy note\n", encoding="utf-8")
            result = analyze_context(str(path))
        self.assertEqual(result["duplicates"], ["Use tests."])
        self.assertEqual(result["stale"], ["TODO legacy note"])

    def test_json_output_contains_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "context.md"
            path.write_text("Always never ask.\n", encoding="utf-8")
            payload = json.loads(run(str(path), "json"))
        self.assertEqual(payload["conflicts"], ["Always never ask."])


if __name__ == "__main__":
    unittest.main()
