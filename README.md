# ADW — Architectural Debt Watchdogs

A lightweight CLI scanner that detects architectural debt in Python codebases:

- Cyclomatic complexity
- Function / file length
- Dead code (crude heuristic)
- Duplicate code (exact-match chunks)

## SOTA Status

- Tests: **11 passing** (`pytest tests/ -q`, ~0.2s)
- CI: ![ci](https://img.shields.io/badge/ci-pending-lightgrey) (placeholder — wire up GitHub Actions)
- Maturity tier: **1 / 3** (MVP — v0.1.0)
- Last commit: 2026-06-06

## Quick Start

```bash
pip install -e .
adw scan .
```

## CLI

```bash
adw scan <repo_path>          # JSON report to stdout
adw scan <repo_path> -o report.json
```

Exit code: `0` = all green, `1` = any yellow/red (for CI gates).

## Heat Map

| Score | Heat     |
|-------|----------|
| 0     | green    |
| 1-3   | yellow   |
| 4+    | red      |

## GitHub

https://github.com/OpenSIN-Code/SIN-Code-ADW-Tool

## Integration

This tool is exposed in the unified `sin code` hub:

```bash
sin code adw scan .            # alias of: adw scan .
```

See `AGENTS.md` for boundaries, key files, and verification steps.

