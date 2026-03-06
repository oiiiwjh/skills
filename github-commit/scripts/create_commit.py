#!/usr/bin/env python3
"""Stage changes, create a commit, and optionally push."""

from __future__ import annotations

import argparse
import json
import os
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


def validate_commit_message(message: str) -> tuple[bool, str]:
    text = message.strip()
    if not text:
        return False, "commit message is required"
    if len(text) < 10:
        return False, "commit message must be at least 10 characters"
    if len(text) > 200:
        return False, "commit message must be <= 200 characters"
    return True, ""


def get_changes(cwd: str) -> list[dict[str, str]]:
    code, stdout, stderr = run_git_command(["status", "--porcelain"], cwd)
    if code != 0:
        raise RuntimeError(stderr or "failed to get status")
    out: list[dict[str, str]] = []
    for line in stdout.splitlines():
        if line:
            out.append({"status": line[:2].strip(), "file": line[3:]})
    return out


def ensure_repo(cwd: str) -> None:
    code, _, stderr = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd)
    if code != 0:
        raise RuntimeError(stderr or "not a git repository")


def current_branch(cwd: str) -> str:
    code, stdout, stderr = run_git_command(["branch", "--show-current"], cwd)
    if code != 0 or not stdout:
        raise RuntimeError(stderr or "failed to resolve current branch")
    return stdout


def create_commit(cwd: str, message: str, push: bool, remote: str) -> dict[str, Any]:
    ensure_repo(cwd)
    changes = get_changes(cwd)
    if not changes:
        return {"status": "noop", "message": "no changes to commit", "cwd": os.path.abspath(cwd)}

    code, _, stderr = run_git_command(["add", "-A"], cwd)
    if code != 0:
        raise RuntimeError(stderr or "failed to stage changes")

    code, stdout, stderr = run_git_command(["commit", "-m", message], cwd)
    if code != 0:
        raise RuntimeError(stderr or "failed to create commit")

    branch = current_branch(cwd)
    push_result = "skipped"
    push_error = ""
    if push:
        p_code, p_out, p_err = run_git_command(["push", remote, branch], cwd)
        if p_code != 0:
            push_result = "failed"
            push_error = p_err or p_out
        else:
            push_result = "ok"

    return {
        "status": "ok",
        "cwd": os.path.abspath(cwd),
        "branch": branch,
        "changes_count": len(changes),
        "commit_output": stdout,
        "push": push_result,
        "push_error": push_error,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a commit from current changes")
    parser.add_argument("path", help="Repository path")
    parser.add_argument("message", help="Commit message")
    parser.add_argument("--push", action="store_true", help="Push after commit")
    parser.add_argument("--remote", default="origin", help="Remote name when --push is used")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON output")
    return parser


def main() -> int:
    parser = build_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exc:
        code = int(str(exc) or 0)
        return EXIT_USAGE if code != 0 else EXIT_OK

    if not os.path.isdir(args.path):
        print(f"Error: directory not found: {args.path}", file=sys.stderr)
        return EXIT_RUNTIME

    valid, reason = validate_commit_message(args.message)
    if not valid:
        print(f"Error: {reason}", file=sys.stderr)
        return EXIT_USAGE

    try:
        result = create_commit(args.path, args.message, args.push, args.remote)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if result["status"] == "noop":
            print("No changes detected, skipping commit.")
        else:
            print(f"Commit created on branch {result['branch']}.")
            if args.push:
                if result["push"] == "ok":
                    print("Push succeeded.")
                elif result["push"] == "failed":
                    print(f"Push failed: {result['push_error']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
