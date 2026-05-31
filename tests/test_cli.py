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
        self.assertEqual(result["findings"][0]["line"], 2)

    def test_json_output_contains_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "context.md"
            path.write_text("Always never ask.\n", encoding="utf-8")
            payload = json.loads(run(str(path), "json"))
        self.assertEqual(payload["conflicts"], ["Always never ask."])

    def test_text_output_includes_line_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "context.md"
            path.write_text("Use tests.\nUse tests.\n", encoding="utf-8")

            output = run(str(path))

        self.assertIn("duplicate at line 2", output)


if __name__ == "__main__":
    unittest.main()
