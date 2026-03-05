#!/usr/bin/env python3
"""Add or update a git remote with validation and optional JSON output."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2


def run_git_command(args: list[str], cwd: str) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as exc:
        return EXIT_RUNTIME, "", str(exc)


def validate_github_url(url: str) -> tuple[bool, str]:
    if not url:
        return False, "URL cannot be empty"
    patterns = [
        r"^https://github\.com/[\w\-.]+/[\w\-.]+(\.git)?$",
        r"^git@github\.com:[\w\-.]+/[\w\-.]+(\.git)?$",
    ]
    for pattern in patterns:
        if re.match(pattern, url):
            return True, ""
    return False, "invalid GitHub URL format"


def get_remote_map(cwd: str) -> dict[str, str]:
    code, stdout, _ = run_git_command(["remote", "-v"], cwd)
    if code != 0:
        return {}
    remotes: dict[str, str] = {}
    for line in stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] not in remotes:
            remotes[parts[0]] = parts[1]
    return remotes


def ensure_git_repo(cwd: str) -> None:
    code, _, stderr = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd)
    if code != 0:
        raise RuntimeError(stderr or "not a git repository")


def upsert_remote(cwd: str, remote_name: str, remote_url: str) -> dict[str, Any]:
    ensure_git_repo(cwd)
    remotes = get_remote_map(cwd)

    if remote_name in remotes:
        code, _, stderr = run_git_command(["remote", "set-url", remote_name, remote_url], cwd)
        action = "updated"
        old_url = remotes[remote_name]
    else:
        code, _, stderr = run_git_command(["remote", "add", remote_name, remote_url], cwd)
        action = "added"
        old_url = None

    if code != 0:
        raise RuntimeError(stderr or "failed to update remote")

    test_code, _, test_err = run_git_command(["ls-remote", remote_name], cwd)
    return {
        "status": "ok",
        "action": action,
        "cwd": os.path.abspath(cwd),
        "remote": remote_name,
        "old_url": old_url,
        "new_url": remote_url,
        "connection_test": "ok" if test_code == 0 else "failed",
        "connection_error": test_err if test_code != 0 else "",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add or update a git remote")
    parser.add_argument("path", help="Repository path")
    parser.add_argument("remote", help="Remote name, e.g. origin")
    parser.add_argument("url", help="GitHub SSH/HTTPS remote URL")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON output")
    return parser


def main() -> int:
    parser = build_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exc:
        code = int(str(exc) or 0)
        return EXIT_USAGE if code != 0 else EXIT_OK

    if not os.path.exists(args.path):
        print(f"Error: directory not found: {args.path}", file=sys.stderr)
        return EXIT_RUNTIME

    valid, reason = validate_github_url(args.url)
    if not valid:
        print(f"Error: {reason}", file=sys.stderr)
        return EXIT_USAGE

    try:
        result = upsert_remote(args.path, args.remote, args.url)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Remote '{result['remote']}' {result['action']}: {result['new_url']}")
        if result["connection_test"] == "ok":
            print("Remote connection test passed.")
        else:
            print(f"Remote connection test failed: {result['connection_error']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
