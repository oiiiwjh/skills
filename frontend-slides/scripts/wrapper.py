#!/usr/bin/env python3
"""Install/update upstream frontend-slides skill into agent skill directories."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

UPSTREAM_URL = "https://github.com/zarazhangrui/frontend-slides.git"
SKILL_NAME = "frontend-slides"
TRACKED_HASH = "384d1a07ba1fd59ff626b141caa65f51a44ccc73"
TRACKED_VERSION = "v2.0.0"

AGENT_DIRS = {
    "codex": Path("~/.codex/skills").expanduser(),
    "claude": Path("~/.claude/skills").expanduser(),
    "opencode": Path("~/.agents/skills").expanduser(),
}

INCLUDE_FILES = [
    "SKILL.md",
    "STYLE_PRESETS.md",
    "viewport-base.css",
    "html-template.md",
    "animation-patterns.md",
    "scripts/extract-pptx.py",
]


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"failed: {' '.join(cmd)}")


def clone_tracked_repo(dst_repo: Path) -> None:
    run(["git", "init", str(dst_repo)])
    run(["git", "-C", str(dst_repo), "remote", "add", "origin", UPSTREAM_URL])
    run(["git", "-C", str(dst_repo), "fetch", "--depth", "1", "origin", TRACKED_HASH])
    run(["git", "-C", str(dst_repo), "checkout", "--detach", "FETCH_HEAD"])
def copy_selected_files(src_repo: Path, dst_skill: Path, force: bool) -> None:
    if dst_skill.exists():
        if not force:
            raise FileExistsError(f"{dst_skill} already exists (use --force to overwrite)")
        shutil.rmtree(dst_skill)

    (dst_skill / "scripts").mkdir(parents=True, exist_ok=True)
    for rel in INCLUDE_FILES:
        src = src_repo / rel
        if not src.exists():
            continue
        dst = dst_skill / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def install_or_update(target_dir: Path, force: bool) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    dst_skill = target_dir / SKILL_NAME
    with tempfile.TemporaryDirectory(prefix="frontend-slides-src-") as tmp:
        repo_dir = Path(tmp) / "repo"
        clone_tracked_repo(repo_dir)
        copy_selected_files(repo_dir, dst_skill, force=force)
    return dst_skill


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage frontend-slides skill installation")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_target_flags(cmd: argparse.ArgumentParser) -> None:
        cmd.add_argument("--agent", choices=sorted(AGENT_DIRS.keys()), default="codex")
        cmd.add_argument("--target-dir", help="Override target skill root directory")
        cmd.add_argument("--force", action="store_true", help="Overwrite existing skill directory")

    add_target_flags(sub.add_parser("install", help="Install frontend-slides to a target agent directory"))
    add_target_flags(sub.add_parser("update", help="Update frontend-slides in a target agent directory"))
    sub.add_parser("info", help="Show upstream metadata")
    return parser.parse_args()


def resolve_target_dir(agent: str, target_dir: str | None) -> Path:
    if target_dir:
        return Path(target_dir).expanduser().resolve()
    return AGENT_DIRS[agent]


def main() -> int:
    args = parse_args()
    if args.command == "info":
        print(f"skill={SKILL_NAME}")
        print(f"url={UPSTREAM_URL}")
        print(f"tracked_hash={TRACKED_HASH}")
        print(f"tracked_version={TRACKED_VERSION}")
        return 0

    target_root = resolve_target_dir(args.agent, args.target_dir)
    is_update = args.command == "update"
    force = True if is_update else bool(args.force)

    try:
        installed_at = install_or_update(target_root, force=force)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1

    action = "updated" if is_update else "installed"
    print(f"{action}: {installed_at}")
    print(f"source: {UPSTREAM_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
