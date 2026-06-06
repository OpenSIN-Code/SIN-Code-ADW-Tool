"""Typer CLI for ADW.

Docs: cli.doc.md
"""
import sys
from pathlib import Path

import typer

from adw.scanner import scan_repo
from adw.reporter import write_report

app = typer.Typer(help="Architectural Debt Watchdogs — code quality scanner")


@app.command()
def scan(
    repo_path: Path = typer.Argument(..., help="Path to repository or file to scan"),
    output: Path | None = typer.Option(None, "--output", "-o", help="JSON output file (default: stdout)"),
) -> None:
    """Scan a codebase and report architectural debt metrics."""
    if repo_path.is_file():
        # Single file mode: wrap in list for uniform handling
        from adw.scanner import scan_file
        results = [scan_file(repo_path)]
    else:
        results = scan_repo(repo_path)

    json_str = write_report(results, out_path=output)
    if not output:
        typer.echo(json_str)

    exit_code = 1 if any(r.score > 0 for r in results) else 0
    raise typer.Exit(code=exit_code)


@app.command()
def version() -> None:
    """Show version."""
    from adw import __version__
    typer.echo(__version__)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
