#!/usr/bin/env python3
"""Shared local and CI command recipes for the leanvm-riscv workspace."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parent.parent

LINT_COMMANDS = {
    "sort": ["cargo", "+stable", "sort", "--workspace", "--grouped", "--check"],
    "toml": ["taplo", "fmt", "--check"],
    "deps": ["cargo", "machete", "--with-metadata"],
    "clippy": ["cargo", "+stable", "clippy", "--all-targets", "--", "-D", "warnings"],
    "docs": [
        "cargo",
        "+stable",
        "doc",
        "--no-deps",
        "--workspace",
        "--document-private-items",
    ],
    "fmt": ["cargo", "+nightly", "fmt", "--all", "--", "--check"],
}


def package_args(packages: Sequence[str]) -> list[str]:
    return [item for package in packages for item in ("-p", package)]


def lint_commands(check: str | None, packages: Sequence[str]) -> list[list[str]]:
    # Repository-wide checks ignore package selection.
    commands = dict(LINT_COMMANDS)
    if packages:
        scope = package_args(packages)
        commands["clippy"] = ["cargo", "+stable", "clippy", *scope, "--all-targets", "--", "-D", "warnings"]
        commands["docs"] = ["cargo", "+stable", "doc", "--no-deps", *scope, "--document-private-items"]
        commands["fmt"] = ["cargo", "+nightly", "fmt", *scope, "--", "--check"]
    if check:
        return [commands[check]]
    return list(commands.values())


def commands_for(args: argparse.Namespace) -> list[list[str]]:
    # `full` takes no package selection.
    selected = getattr(args, "package", None) or []
    listed = (getattr(args, "packages", None) or "").split(",")
    packages = sorted(set(selected) | {p for p in listed if p})
    scope = package_args(packages) or ["--workspace"]
    if args.command == "fast":
        return [["cargo", "check", *scope, "--all-targets"]]
    if args.command == "test":
        # A new workspace may have no tests yet.
        return [["cargo", "nextest", "run", *scope, "--no-tests", "warn"]]
    if args.command == "doctest":
        return [["cargo", "test", "--doc", *scope]]
    if args.command == "lint":
        return lint_commands(args.check, packages)
    # `full` runs every routine host check.
    return [
        ["cargo", "check", "--workspace", "--all-targets"],
        ["cargo", "nextest", "run", "--workspace", "--no-tests", "warn"],
        ["cargo", "test", "--doc", "--workspace"],
        *lint_commands(None, []),
    ]


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--dry-run", action="store_true", help="print commands without running them")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("fast", "test", "doctest", "lint", "full"):
        command = commands.add_parser(name)
        if name == "full":
            continue
        command.add_argument("--package", action="append", help="limit to one workspace package")
        command.add_argument("--packages", help="comma-separated workspace packages")
        if name == "lint":
            command.add_argument("--check", choices=sorted(LINT_COMMANDS))
    return root


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    for command in commands_for(args):
        print(f"$ {shlex.join(command)}", flush=True)
        if args.dry_run:
            continue
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
