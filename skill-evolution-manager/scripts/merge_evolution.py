#!/usr/bin/env python3
"""Merge new evolution entries into evolution.json for one skill."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from typing import Any

EXIT_OK = 0
EXIT_RUNTIME = 1
EXIT_USAGE = 2


def merge_evolution(skill_dir: str, new_data_json_str: str) -> dict[str, Any]:
    evolution_json_path = os.path.join(skill_dir, "evolution.json")

    if not os.path.isdir(skill_dir):
        raise FileNotFoundError(f"skill directory not found: {skill_dir}")

    if os.path.exists(evolution_json_path):
        try:
            with open(evolution_json_path, "r", encoding="utf-8") as f:
                current_data: dict[str, Any] = json.load(f)
        except Exception as exc:
            raise ValueError(f"failed to parse existing evolution.json: {exc}") from exc
    else:
        current_data = {}

    try:
        new_data = json.loads(new_data_json_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid new data JSON: {exc}") from exc

    if not isinstance(new_data, dict):
        raise ValueError("new data JSON must be an object")

    current_data["last_updated"] = dt.datetime.now(dt.timezone.utc).isoformat()

    for list_key in ["preferences", "fixes", "contexts"]:
        if list_key not in new_data:
            continue

        incoming = new_data[list_key]
        if not isinstance(incoming, list):
            raise ValueError(f"field '{list_key}' must be a list")

        existing = current_data.get(list_key, [])
        if not isinstance(existing, list):
            existing = []

        for item in incoming:
            if item not in existing:
                existing.append(item)
        current_data[list_key] = existing

    if "custom_prompts" in new_data:
        current_data["custom_prompts"] = new_data["custom_prompts"]

    if "last_evolved_hash" in new_data:
        current_data["last_evolved_hash"] = new_data["last_evolved_hash"]

    with open(evolution_json_path, "w", encoding="utf-8") as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    return {
        "skill_dir": os.path.abspath(skill_dir),
        "evolution_json": os.path.abspath(evolution_json_path),
        "status": "ok",
        "merged_keys": sorted(list(new_data.keys())),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge evolution data into a skill's evolution.json")
    parser.add_argument("skill_dir", help="Path to target skill directory")
    parser.add_argument("json_string", help="JSON object string with evolution data")
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
        result = merge_evolution(args.skill_dir, args.json_string)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Successfully merged evolution data for {os.path.basename(args.skill_dir)}")
        print(f"Updated: {result['evolution_json']}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
