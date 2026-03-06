#!/usr/bin/env python3
"""Inspect git repository status with optional JSON output."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from typing import Any

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2


def run_git_command(args: list[str], cwd: str | None = None) -> tuple[int, str, str]:
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


def check_git_repo(cwd: str) -> bool:
    code, _, _ = run_git_command(["rev-parse", "--is-inside-work-tree"], cwd)
    return code == 0


def get_remote_urls(cwd: str) -> list[dict[str, str]]:
    code, stdout, _ = run_git_command(["remote", "-v"], cwd)
    if code != 0:
        return []

    remotes: list[dict[str, str]] = []
    for line in stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            remotes.append({"name": parts[0], "url": parts[1], "type": parts[2]})
    return remotes


def get_current_branch(cwd: str) -> str | None:
    code, stdout, _ = run_git_command(["branch", "--show-current"], cwd)
    return stdout if code == 0 else None


def get_status_summary(cwd: str) -> list[dict[str, str]]:
    code, stdout, _ = run_git_command(["status", "--porcelain"], cwd)
    if code != 0:
        return []

    changes: list[dict[str, str]] = []
    for line in stdout.splitlines():
        if not line:
            continue
        changes.append({"status": line[:2].strip(), "file": line[3:]})
    return changes


def get_commit_history(cwd: str, limit: int) -> list[dict[str, str]]:
    code, stdout, _ = run_git_command(["log", "--oneline", f"-{limit}"], cwd)
    if code != 0:
        return []

    commits: list[dict[str, str]] = []
    for line in stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            commits.append({"hash": parts[0], "message": parts[1]})
    return commits


def collect_status(cwd: str, history_limit: int) -> dict[str, Any]:
    if not os.path.exists(cwd):
        raise FileNotFoundError(f"directory not found: {cwd}")

    if not check_git_repo(cwd):
        raise RuntimeError("not a git repository")

    return {
        "status": "ok",
        "cwd": os.path.abspath(cwd),
        "branch": get_current_branch(cwd),
        "remotes": get_remote_urls(cwd),
        "changes": get_status_summary(cwd),
        "recent_commits": get_commit_history(cwd, history_limit),
    }


def print_human(result: dict[str, Any]) -> None:
    print(f"检查目录: {result['cwd']}")
    print("✅ 是Git仓库")

    remotes = result["remotes"]
    if remotes:
        print("\n📡 远程仓库:")
        for remote in remotes:
            print(f"  {remote['name']}: {remote['url']} ({remote['type']})")
    else:
        print("\n⚠️  没有配置远程仓库")

    if result.get("branch"):
        print(f"\n🌿 当前分支: {result['branch']}")

    changes = result["changes"]
    if changes:
        print(f"\n📝 未提交的更改 ({len(changes)}个):")
        for change in changes:
            print(f"  {change['status'] or '??'} {change['file']}")
    else:
        print("\n✅ 工作区干净，没有未提交的更改")

    commits = result["recent_commits"]
    if commits:
        print(f"\n📜 最近提交 ({len(commits)}个):")
        for commit in commits:
            print(f"  {commit['hash'][:8]} {commit['message']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check git repository status")
    parser.add_argument("path", nargs="?", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--history-limit", type=int, default=5, help="Number of recent commits to include")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON output")
    return parser


def main() -> int:
    parser = build_parser()
    try:
        args = parser.parse_args()
    except SystemExit as exc:
        code = int(str(exc) or 0)
        return EXIT_USAGE if code != 0 else EXIT_OK

    try:
        result = collect_status(args.path, args.history_limit)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"❌ {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print_human(result)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
