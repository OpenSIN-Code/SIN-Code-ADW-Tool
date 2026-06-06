# reporter.py

- What: JSON serialization and heat-map scoring.
- Touches: `cli.py` (calls `write_report`), `scanner.py` (consumes `FileMetrics`).
- Score thresholds: 0=green, 1-3=yellow, 4+=red.
- Exit code logic: 1 if any file has score > 0.
