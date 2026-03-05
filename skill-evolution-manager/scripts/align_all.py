#!/usr/bin/env python3
"""Align all skills that have evolution.json by stitching them into SKILL.md."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2


def default_skills_root() -> Path:
    # Prefer repo root (script lives in <repo>/skill-evolution-manager/scripts)
    candidate = Path(__file__).resolve().parents[2]
    if (candidate / "README.md").exists() and (candidate / "skill-evolution-manager").exists():
        return candidate
    return Path.cwd()


def align_all(skills_root: Path) -> dict[str, Any]:
    if not skills_root.exists() or not skills_root.is_dir():
        raise FileNotFoundError(f"skills root not found: {skills_root}")

    stitch_script = Path(__file__).resolve().parent / "smart_stitch.py"
    aligned: list[str] = []
    failed: list[dict[str, str]] = []

    for item in sorted(skills_root.iterdir()):
        if not item.is_dir():
            continue
        if not (item / "SKILL.md").exists():
            continue
        if not (item / "evolution.json").exists():
            continue

        proc = subprocess.run(
            [sys.executable, str(stitch_script), str(item), "--json"],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            aligned.append(item.name)
        else:
            failed.append({"skill": item.name, "stderr": proc.stderr.strip()})

    return {
        "status": "ok" if not failed else "partial",
        "skills_root": str(skills_root.resolve()),
        "aligned_count": len(aligned),
        "aligned": aligned,
        "failed_count": len(failed),
        "failed": failed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stitch evolution.json into all skills under a root directory")
    parser.add_argument(
        "skills_root",
        nargs="?",
        default=str(default_skills_root()),
        help="Root directory containing skill folders (default: inferred repository root)",
    )
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
        result = align_all(Path(args.skills_root))
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Finished. Aligned {result['aligned_count']} skills under {result['skills_root']}.")
        if result["failed_count"]:
            print(f"Failures: {result['failed_count']}")
            for entry in result["failed"]:
                print(f"- {entry['skill']}: {entry['stderr']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
