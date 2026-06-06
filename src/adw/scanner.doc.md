# scanner.py

- What: Core AST-based metrics engine (complexity, length, dead code, duplicates).
- Touches: `cli.py` (calls `scan_repo`), `reporter.py` (consumes `FileMetrics`).
- Heuristic: dead-code detection is crude — only checks same-file references and imports.
- Duplicate detection: exact string matches of 3+ lines via MD5 hashing.
