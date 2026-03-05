#!/usr/bin/env python3
"""Stitch evolution.json into SKILL.md under a dedicated section."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2
SECTION_TITLE = "## User-Learned Best Practices & Constraints"


def build_evolution_block(data: dict[str, Any]) -> str:
    lines: list[str] = [
        "",
        "",
        SECTION_TITLE,
        "",
        "> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.",
    ]

    if data.get("preferences"):
        lines.append("")
        lines.append("### User Preferences")
        lines.extend(f"- {item}" for item in data["preferences"])

    if data.get("fixes"):
        lines.append("")
        lines.append("### Known Fixes & Workarounds")
        lines.extend(f"- {item}" for item in data["fixes"])

    if data.get("custom_prompts"):
        lines.append("")
        lines.append("### Custom Instruction Injection")
        lines.append("")
        lines.append(str(data["custom_prompts"]))

    return "\n".join(lines).rstrip() + "\n"


def stitch_skill(skill_dir: str) -> dict[str, Any]:
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    evolution_json_path = os.path.join(skill_dir, "evolution.json")

    if not os.path.isdir(skill_dir):
        raise FileNotFoundError(f"skill directory not found: {skill_dir}")
    if not os.path.exists(skill_md_path):
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    if not os.path.exists(evolution_json_path):
        return {
            "status": "skipped",
            "reason": "no evolution.json",
            "skill_dir": os.path.abspath(skill_dir),
        }

    try:
        with open(evolution_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        raise ValueError(f"failed to parse evolution.json: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("evolution.json must contain a JSON object")

    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    evolution_block = build_evolution_block(data)
    pattern = re.compile(r"\n+## User-Learned Best Practices & Constraints.*$", re.DOTALL)

    if pattern.search(content):
        new_content = pattern.sub(evolution_block, content)
        action = "updated"
    else:
        new_content = content.rstrip() + evolution_block
        action = "appended"

    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {
        "status": "ok",
        "action": action,
        "skill_dir": os.path.abspath(skill_dir),
        "skill_md": os.path.abspath(skill_md_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stitch evolution.json content into SKILL.md")
    parser.add_argument("skill_dir", help="Path to target skill directory")
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
        result = stitch_skill(args.skill_dir)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if result["status"] == "skipped":
            print(f"Skipped {args.skill_dir}: no evolution.json")
        else:
            print(f"Successfully stitched evolution data into {result['skill_md']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
