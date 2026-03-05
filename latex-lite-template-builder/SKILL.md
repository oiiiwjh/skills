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
