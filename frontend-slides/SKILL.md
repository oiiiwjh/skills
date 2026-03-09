---
name: frontend-slides
description: Install and maintain the upstream Frontend Slides skill from GitHub so agents can create high-quality HTML slide decks and convert PPTX content.
metadata:
  github_url: https://github.com/zarazhangrui/frontend-slides.git
  github_hash: 384d1a07ba1fd59ff626b141caa65f51a44ccc73
  version: v2.0.0
  created_at: 2026-03-06T03:00:18Z
  entry_point: scripts/wrapper.py
  dependencies:
    - git
    - python3
    - python-pptx (optional for PPTX conversion)
---

# Frontend Slides Wrapper Skill

This wrapper manages the upstream skill repository: [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides).

## Overview

Use this skill when you need to:
- Install Frontend Slides into an agent skill directory.
- Update an existing installation to the latest upstream commit.
- Keep one canonical source of truth with tracked hash/version metadata.

The upstream Frontend Slides skill focuses on:
- Animation-rich single-file HTML presentations.
- Visual style discovery for non-designers.
- PPTX to web-slide conversion (with optional `python-pptx`).

## Workflow

1. Run `scripts/wrapper.py info` to inspect tracked source metadata.
1. Install to a target agent:
```bash
python scripts/wrapper.py install --agent codex
```
1. Update an existing local copy:
```bash
python scripts/wrapper.py update --agent codex
```
1. Optional custom destination:
```bash
python scripts/wrapper.py install --target-dir /abs/path/to/skills
```

## Examples

Install for Claude Code:
```bash
python scripts/wrapper.py install --agent claude
```

Force reinstall:
```bash
python scripts/wrapper.py install --agent codex --force
```

## References

- `references/upstream-notes.md`
- Upstream repo: https://github.com/zarazhangrui/frontend-slides
