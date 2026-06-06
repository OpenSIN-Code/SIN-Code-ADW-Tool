"""Test suite for ADW scanner and reporter.

Docs: test_scanner.doc.md
"""
import json
from pathlib import Path

import pytest

from adw.scanner import scan_file, scan_repo, _count_complexity, _find_duplicates, _find_dead_code
from adw.reporter import generate_report, _heat

FIXTURES = Path(__file__).parent / "fixtures"


class TestComplexity:
    """Cyclomatic complexity counting."""

    def test_simple_function(self):
        """A function with no branches has complexity 0."""
        import ast
        code = "def f():\n    return 1\n"
        tree = ast.parse(code)
        func = tree.body[0]
        assert _count_complexity(func) == 0

    def test_nested_ifs(self):
        """Nested if/elif/else and loops increase complexity."""
        import ast
        code = """
def f(x):
    if x > 0:
        if x > 10:
            for i in range(3):
                while i < 5:
                    i += 1
"""
        tree = ast.parse(code)
        func = tree.body[0]
        assert _count_complexity(func) >= 4


class TestLength:
    """Function and file length metrics."""

    def test_long_function_detected(self):
        """A function with >50 lines should be flagged."""
        result = scan_file(FIXTURES / "complex.py")
        long_funcs = [f for f in result.functions if f.lines > 50]
        assert len(long_funcs) >= 1
        assert long_funcs[0].name == "long_function"

    def test_file_lines(self):
        """File line count should be reasonable."""
        result = scan_file(FIXTURES / "complex.py")
        assert result.lines > 0


class TestDeadCode:
    """Dead code detection heuristics."""

    def test_unused_function(self):
        """An unreferenced function is flagged dead."""
        result = scan_file(FIXTURES / "complex.py")
        assert "unused_function" in result.dead_symbols

    def test_unused_class(self):
        """An unreferenced class is flagged dead."""
        result = scan_file(FIXTURES / "complex.py")
        assert "UnusedClass" in result.dead_symbols


class TestDuplicates:
    """Duplicate code detection."""

    def test_duplicate_blocks_found(self):
        """Exact 3-line duplicates should be detected."""
        result = scan_file(FIXTURES / "duplicate.py")
        assert len(result.duplicates) > 0

    def test_duplicate_groups(self):
        """Each duplicate group should have at least 2 occurrences."""
        result = scan_file(FIXTURES / "duplicate.py")
        for group in result.duplicates:
            assert len(group) >= 2


class TestIntegration:
    """End-to-end integration tests."""

    def test_scan_repo_finds_files(self):
        """scan_repo should discover both fixture files."""
        results = scan_repo(FIXTURES)
        paths = [r.path for r in results]
        assert any("complex.py" in p for p in paths)
        assert any("duplicate.py" in p for p in paths)

    def test_json_report_structure(self):
        """Report should contain summary and files array."""
        results = scan_repo(FIXTURES)
        report = generate_report(results)
        assert "summary" in report
        assert "files" in report
        assert isinstance(report["files"], list)

    def test_heat_levels(self):
        """Heat mapping: 0=green, 1-3=yellow, 4+=red."""
        assert _heat(0).value == "green"
        assert _heat(1).value == "yellow"
        assert _heat(3).value == "yellow"
        assert _heat(4).value == "red"
