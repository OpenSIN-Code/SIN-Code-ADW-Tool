# ADW — Architectural Debt Watchdogs

A lightweight CLI scanner that detects architectural debt in Python codebases:

- Cyclomatic complexity
- Function / file length
- Dead code (crude heuristic)
- Duplicate code (exact-match chunks)

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
