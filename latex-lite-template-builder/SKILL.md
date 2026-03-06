---
name: latex-lite-template-builder
description: Build reusable lite LaTeX paper templates from a source template directory. Use when users ask to migrate an existing LaTeX paper style into a compact reusable skeleton, including script-based generation and optional Overleaf bundle output.
---

# Latex Lite Template Builder

Use this skill when users ask to:
- migrate a LaTeX template into a reusable short version,
- create a lightweight paper skeleton from an existing source repo,
- keep or neutralize branding assets while preserving style.

## Workflow

1. Resolve repository root containing `tools/make_lite_template.sh`.
2. Detect desired profile (`2602`, `2603`, or `auto`) from user request.
3. Run the wrapper script in `scripts/run_make_lite.sh`.
4. Return output path and follow-up instructions (edit `main.tex`, `sec/*.tex`, `main.bib`).

## Command

```bash
scripts/run_make_lite.sh \
  --source <source_dir> \
  --profile <2602|2603|auto> \
  --output <output_dir> \
  [--neutral-branding] \
  [--with-overleaf-bundle] \
  [--force] [--dry-run]
```

## Notes

- Default is keep-branding mode.
- Output should be a new directory, not in-place rewrite.
- If detection fails, retry with explicit `--profile`.
- Supported profile details are in `references/profiles.md`.

## Overview

This skill is used when its `description` in frontmatter matches the user request. Prefer existing scripts under `scripts/` over ad-hoc rewrites.

## Examples

```bash
# Run from repository root
python <skill-name>/scripts/<script>.py --help
```

## References

- `scripts/`: executable helpers for deterministic steps
- `references/`: additional docs loaded on demand
- `assets/`: templates or static files used by the skill

## Trigger Conditions

- User explicitly names this skill
- User intent clearly matches this skill description
- The task needs this skill's scripts/resources

## Applicable Scope

- Requests covered by this skill's frontmatter `description`
- Tasks that benefit from the bundled workflow and scripts

## Out of Scope

- Requests that conflict with repository safety rules
- Tasks unrelated to this skill's declared purpose
- Destructive changes without explicit user permission
