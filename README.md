# Context Window Doctor

Find context rot in long coding-agent instruction files.

## Why

Long coding-agent contexts accumulate repeated, stale, and contradictory instructions that lower reliability.

This is a baseline HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/context-window-doctor.git
cd context-window-doctor
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m context_window_doctor examples/context.md
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m context_window_doctor examples/context.md
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m context_window_doctor examples/context.md --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m context_window_doctor --help`
- Main demo: `PYTHONPATH=src python3 -m context_window_doctor examples/context.md`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- Duplicate instruction detection
- Simple conflict pattern detection
- Stale wording detection
- Line-numbered findings
- Text and JSON output

## API

The public Python surface is intentionally small:

```python
from context_window_doctor.cli import analyze_context
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It gives prompt and agent teams a quick hygiene pass for overloaded context files.

## Used With

- Run before `repo-to-ai-brief` when long context files include stale or contradictory instructions.
- Pair with `prompt-drift-watch` when duplicated context hides risky instruction changes.
- Keep this as the context-rot detector inside a larger coding-agent maintenance workflow.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
