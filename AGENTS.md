# SIN-Code-ADW-Tool — Agent-Engineering Hints

## What it does (1 sentence)
Architectural Debt Watchdogs — lightweight CLI scanner that detects cyclomatic complexity, oversized functions/files, dead code, and exact-match duplicate chunks in Python codebases; emits a JSON report with a green/yellow/red heat map.

## Stack
- Language: Python
- Version: 0.1.0
- Test count: 11 tests
- CLI: `adw` with 2 subcommands (`scan`, `version`)

## When to use
- CI gate to fail builds when architectural debt crosses a threshold (`adw scan` exits 1 on yellow/red).
- One-shot debt audit on a legacy or unfamiliar Python repo (output is structured JSON, easy to consume).
- Tracking debt trend over time by piping `adw scan -o report.json` into a time-series store.

## Boundaries
- Do NOT change the heat-map thresholds (`0` green, `1-3` yellow, `4+` red) without bumping the major version — CI configs depend on them.
- Do NOT change the JSON report shape — downstream dashboards parse it.
- Always keep the exit-code contract: `0` = all green, `1` = any yellow/red.
- Always run via `adw.cli:main` — never call scanner functions directly from external tools (use the JSON output).

## Key files
- `src/adw/scanner.py` — AST-based debt detectors (complexity, length, dead-code, duplicates).
- `src/adw/reporter.py` — heat-map scoring + JSON report assembly.
- `src/adw/cli.py` — Typer CLI (`scan`, `version`).
- `tests/test_scanner.py` — 11 tests covering per-detector behavior + integration (`test_scan_repo_finds_files`, `test_json_report_structure`, `test_heat_levels`).
- `tests/fixtures/` — sample Python files with known debt patterns.

## Verification
- `pytest tests/ -v` — all 11 tests pass.
- `adw version` — prints version.
- `adw scan .` — smoke test on this repo; should exit cleanly and print JSON.
