"""Find duplicate, conflicting, and stale instructions in long context files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Sequence


CONFLICT_PAIRS = [("always", "never"), ("must", "do not"), ("required", "optional")]
STALE_PATTERNS = [r"\bdeprecated\b", r"\bold\b", r"\blegacy\b", r"\bTODO\b"]


def normalize(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip().lower())


def analyze_context(path: str) -> Dict[str, List[str] | int]:
    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()
    lines = [(number, line.strip()) for number, line in enumerate(raw_lines, start=1) if line.strip()]
    seen = {}
    duplicates = []
    conflicts = []
    stale = []
    findings = []
    first_seen_line = {}
    for line_number, line in lines:
        key = normalize(line)
        seen[key] = seen.get(key, 0) + 1
        first_seen_line.setdefault(key, line_number)
        if seen[key] == 2:
            duplicates.append(line)
            findings.append(
                {
                    "kind": "duplicate",
                    "line": line_number,
                    "first_line": first_seen_line[key],
                    "text": line,
                }
            )
        lower = line.lower()
        for left, right in CONFLICT_PAIRS:
            if left in lower and right in lower:
                conflicts.append(line)
                findings.append({"kind": "conflict", "line": line_number, "text": line, "pair": [left, right]})
        if any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in STALE_PATTERNS):
            stale.append(line)
            findings.append({"kind": "stale", "line": line_number, "text": line})
    return {
        "line_count": len(lines),
        "duplicates": duplicates,
        "conflicts": conflicts,
        "stale": stale,
        "findings": findings,
    }


def format_text(result: Dict[str, List[str] | int]) -> str:
    lines = [f"Lines: {result['line_count']}"]
    for key in ["duplicates", "conflicts", "stale"]:
        values = result[key]
        lines.extend(["", f"{key.title()}:"])
        lines.extend(f"- {item}" for item in values) if values else lines.append("- none")
    if result["findings"]:
        lines.extend(["", "Findings:"])
        for finding in result["findings"]:
            location = f"line {finding['line']}"
            if finding["kind"] == "duplicate":
                location += f" (first seen line {finding['first_line']})"
            lines.append(f"- {finding['kind']} at {location}: {finding['text']}")
    return "\n".join(lines)


def run(input_path: str, output_format: str = "text") -> str:
    result = analyze_context(input_path)
    if output_format == "json":
        return json.dumps(result, indent=2, sort_keys=True)
    return format_text(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find duplicate, conflicting, and stale instructions in long context files.")
    parser.add_argument("input", help="Markdown or text context file")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
