# SIN-Code-ADW-Tool — Architectural Debt Watchdogs — AST-based debt scanner emitting a green/yellow/red heat map (cyclomatic complexity, oversized files/functions, dead code, exact duplicates).

<!--
  Docs: this file follows the SIN-Code AGENTS.md standard
  (see OpenSIN-Code/SIN-Code AGENTS.md section "Ecosystem map" and
  issue #40). sin-brain discovers rules via the section headers below;
  sin-context-bridge queries this file via the "## Architecture" anchor.
  Generated: 2026-06-13; standard version: v1 (chore/issue-40).
-->

## Architecture

Single-pass AST scan with four detectors, heat-map scoring, and a stable JSON report (consumed by downstream dashboards). Exit-code contract: `0`=all green, `1`=any yellow/red. Main entry point: `src/adw/cli.py` (Typer, 2 subcommands: `scan`, `version`). Heat-map thresholds (`0`/`1-3`/`4+`) are part of the public contract.

## Services

| Service | Port | Purpose |
| ------- | ---- | ------- |
| CLI     | N/A  | `adw <subcommand>` — scan, version |

## Quick-Start

```bash
pip install -e .
adw --help
adw scan .
```

## Key Endpoints / Commands

- `adw scan` — scan repo for architectural debt (exit 1 on yellow/red)
- `adw version` — print tool version

## CoDocs

- All Python source files in `src/adw/` MUST have a `.doc.md` companion.
- Run `sin codocs check` to validate. Output MUST be `OK: 3 files` to pass.
- CoDocs companion for THIS file: none (AGENTS.md is itself a doc).

## Testing

```bash
pytest tests/ -v
pytest tests/test_agents_md.py -v
```

Expected: 12 tests pass (11 existing + 1 from issue #40).

## Integration

- **sin-code HubTool:** `sin code adw scan` — called by `sin code debt` and `sin code full`.
- **MCP server:** `adw` exposes MCP via the `sin-code serve` adapter; the
  tool prefix in MCP namespace is `adw__*` (e.g. `adw__scan`).
- **Cross-repo:** called by `sin code debt` and the `sin code full` pipeline.

---

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **SIN-Code-ADW-Tool** (139 symbols, 201 relationships, 6 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/SIN-Code-ADW-Tool/context` | Codebase overview, check index freshness |
| `gitnexus://repo/SIN-Code-ADW-Tool/clusters` | All functional areas |
| `gitnexus://repo/SIN-Code-ADW-Tool/processes` | All execution flows |
| `gitnexus://repo/SIN-Code-ADW-Tool/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
