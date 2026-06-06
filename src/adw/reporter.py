"""JSON reporting and heat-map scoring for ADW.

Docs: reporter.doc.md
"""
import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any

from adw.scanner import FileMetrics, FunctionMetrics


class Heat(str, Enum):
    """Heat-map level."""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


def _heat(score: int) -> Heat:
    """Map numeric score to heat level."""
    if score == 0:
        return Heat.GREEN
    elif score <= 3:
        return Heat.YELLOW
    return Heat.RED


def _function_to_dict(f: FunctionMetrics) -> Dict[str, Any]:
    return {
        "name": f.name,
        "lines": f.lines,
        "complexity": f.complexity,
        "dead": f.dead,
    }


def _file_to_dict(m: FileMetrics) -> Dict[str, Any]:
    return {
        "path": m.path,
        "lines": m.lines,
        "score": m.score,
        "heat": _heat(m.score).value,
        "functions": [_function_to_dict(f) for f in m.functions],
        "duplicates": m.duplicates,
        "dead_symbols": m.dead_symbols,
    }


def generate_report(results: List[FileMetrics]) -> Dict[str, Any]:
    """Build the JSON report structure."""
    total_score = sum(r.score for r in results)
    files = [_file_to_dict(r) for r in results]
    any_yellow_red = any(r.score > 0 for r in results)
    return {
        "summary": {
            "files_scanned": len(results),
            "total_score": total_score,
            "overall_heat": _heat(total_score).value,
            "exit_code": 1 if any_yellow_red else 0,
        },
        "files": files,
    }


def write_report(results: List[FileMetrics], out_path: Path | None = None) -> str:
    """Serialize report to JSON string or file."""
    report = generate_report(results)
    json_str = json.dumps(report, indent=2)
    if out_path:
        out_path.write_text(json_str, encoding="utf-8")
    return json_str
