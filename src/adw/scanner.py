"""Core scanning engine for ADW metrics.

Docs: scanner.doc.md
"""
import ast
import hashlib
from pathlib import Path
from typing import Dict, List, NamedTuple, Set, Tuple


class FunctionMetrics(NamedTuple):
    """Metrics for a single function or method."""
    name: str
    lines: int
    complexity: int
    dead: bool


class FileMetrics(NamedTuple):
    """Metrics for a single file."""
    path: str
    lines: int
    functions: List[FunctionMetrics]
    duplicates: List[List[int]]  # line-number groups that are duplicated
    dead_symbols: List[str]
    score: int


# ── Complexity ──────────────────────────────────────

COMPLEXITY_NODES = (
    ast.If, ast.For, ast.While, ast.ExceptHandler,
    ast.BoolOp, ast.With, ast.Assert, ast.ListComp,
    ast.SetComp, ast.DictComp, ast.GeneratorExp,
)


def _count_complexity(node: ast.AST) -> int:
    """Recursively count complexity-increasing nodes."""
    total = 0
    for child in ast.walk(node):
        if isinstance(child, COMPLEXITY_NODES):
            total += 1
        elif isinstance(child, ast.Try):
            # Each except handler is already counted above, but Try itself adds 1
            total += 1
    return total


# ── Length ──────────────────────────────────────────

def _body_length(node: ast.FunctionDef | ast.ClassDef | ast.AsyncFunctionDef) -> int:
    """Return the number of lines the body spans."""
    if not node.body:
        return 0
    first = node.body[0].lineno
    last = node.body[-1].end_lineno or node.body[-1].lineno
    return last - first + 1


# ── Duplicate detection ─────────────────────────────

def _find_duplicates(source: str, min_lines: int = 3) -> List[List[int]]:
    """Find exact duplicate chunks of >= min_lines lines."""
    lines = source.splitlines()
    chunks: Dict[str, List[int]] = {}
    for i in range(len(lines) - min_lines + 1):
        chunk = "\n".join(lines[i : i + min_lines])
        h = hashlib.md5(chunk.encode()).hexdigest()
        chunks.setdefault(h, []).append(i)
    duplicates = []
    for occurrences in chunks.values():
        if len(occurrences) > 1:
            # Store line numbers (1-indexed)
            duplicates.append([o + 1 for o in occurrences])
    return duplicates


# ── Dead-code detection ─────────────────────────────

def _find_dead_code(
    tree: ast.AST, defined: Dict[str, ast.AST], imported_names: Set[str]
) -> List[str]:
    """Crude dead-code heuristic: defined but never referenced in file."""
    referenced: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                referenced.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                referenced.add(node.func.attr)
        elif isinstance(node, ast.Name):
            referenced.add(node.id)
    dead = []
    for name, node in defined.items():
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if name not in referenced and name not in imported_names:
                dead.append(name)
    return dead


# ── Public API ────────────────────────────────────

def scan_file(path: Path) -> FileMetrics:
    """Scan a single Python file and return metrics."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    total_lines = len(source.splitlines())
    functions: List[FunctionMetrics] = []
    defined: Dict[str, ast.AST] = {}
    imported_names: Set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defined[node.name] = node
            functions.append(
                FunctionMetrics(
                    name=node.name,
                    lines=_body_length(node),
                    complexity=_count_complexity(node),
                    dead=False,
                )
            )
        elif isinstance(node, ast.ClassDef):
            defined[node.name] = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)

    dead = _find_dead_code(tree, defined, imported_names)
    duplicates = _find_duplicates(source, min_lines=3)

    # Mark dead functions
    functions = [
        f._replace(dead=f.name in dead) for f in functions
    ]

    # Score: complexity > 10 → +1, function > 50 lines → +1, dead code → +1, duplicates → +1 per 2 groups
    score = 0
    for f in functions:
        if f.complexity > 10:
            score += 1
        if f.lines > 50:
            score += 1
        if f.dead:
            score += 1
    score += len(dead)
    score += len(duplicates) // 2
    if total_lines > 300:
        score += 1

    return FileMetrics(
        path=str(path),
        lines=total_lines,
        functions=functions,
        duplicates=duplicates,
        dead_symbols=dead,
        score=score,
    )


def scan_repo(repo_path: Path) -> List[FileMetrics]:
    """Scan all Python files under *repo_path*."""
    results = []
    for py_file in repo_path.rglob("*.py"):
        # Skip common virtualenv / cache paths
        if any(part.startswith(".") for part in py_file.parts):
            continue
        if "venv" in py_file.parts or "__pycache__" in py_file.parts:
            continue
        try:
            results.append(scan_file(py_file))
        except SyntaxError:
            continue
    return results
