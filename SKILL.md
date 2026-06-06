# ADW Skill

## Usage

```bash
adw scan <path> [--output report.json]
```

## Output Format

```json
{
  "summary": {
    "files_scanned": 42,
    "total_score": 7,
    "overall_heat": "yellow",
    "exit_code": 1
  },
  "files": [
    {
      "path": "src/foo.py",
      "lines": 120,
      "score": 2,
      "heat": "yellow",
      "functions": [...],
      "duplicates": [[1, 15]],
      "dead_symbols": ["unused_helper"]
    }
  ]
}
```

## Integration

Use in CI:

```yaml
- run: adw scan . || true
  id: adw
- if: steps.adw.outputs.exit_code == '1'
  run: echo "Debt detected!"
```
