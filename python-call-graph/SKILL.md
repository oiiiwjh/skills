---
name: python-call-graph
description: Generate a static function and method call graph for a Python repository. Use this skill when the user wants a Python call graph, function dependency map, Mermaid call diagram, or static call-chain analysis from a local repo.
---

# Python Call Graph

## Overview

Use this skill to analyze a Python repository with AST-only static analysis and produce function or method call relationships without executing the target code.

Default behavior is:
- scan the whole repository first
- generate both Mermaid and JSON outputs
- narrow to a specific entrypoint only when the user needs a focused subgraph

## When To Use

Trigger this skill when the user asks for:
- a Python function call graph
- a Mermaid call diagram
- a function dependency map
- a static call-chain view for a repository
- a repository-level function or method relationship graph

Do not use this skill for:
- runtime tracing
- non-Python repositories
- exact dynamic dispatch resolution
- closure or nested-function structure analysis as the primary goal

## Workflow

1. Confirm the target is a Python repository or contains meaningful `.py` sources.
2. Run a full-repo scan to understand the overall structure.
3. If the graph is too large, rerun with `--entry` and optionally `--max-depth`.
4. Prefer Mermaid output for human review and JSON output for downstream tooling or filtering.
5. If results look incomplete, check the known static-analysis limitations in [references/limitations.md](./references/limitations.md).

## Commands

Full repository scan:

```bash
python /Users/jah/.agents/skills/python-call-graph/scripts/generate_call_graph.py /path/to/repo
```

Write both Mermaid and JSON outputs to files:

```bash
python /Users/jah/.agents/skills/python-call-graph/scripts/generate_call_graph.py /path/to/repo --format both --output /tmp/repo-call-graph
```

Focus on one entrypoint:

```bash
python /Users/jah/.agents/skills/python-call-graph/scripts/generate_call_graph.py /path/to/repo --entry package.module::main --max-depth 3
```

Include test files and add extra ignore globs:

```bash
python /Users/jah/.agents/skills/python-call-graph/scripts/generate_call_graph.py /path/to/repo --include-tests --ignore 'examples/*' --ignore 'legacy/*.py'
```

## Output Contract

The script produces:
- Mermaid graph output for inspection in Markdown viewers
- JSON output with nodes, edges, entrypoints, unresolved calls, and scan statistics

Qualified symbols use these forms:
- `package.module::function`
- `package.module::Class.method`

When `--format both` is used:
- without `--output`, both outputs are printed to stdout, Mermaid first and JSON second
- with `--output`, the script writes `<base>.mmd` and `<base>.json`

## Constraints

This skill performs static AST analysis only. It prefers stable, explainable results over aggressive inference.

Expect partial or missing resolution for:
- dynamic dispatch
- `getattr` and reflection
- decorator rewrites
- runtime imports
- monkey patching
- complex alias chains across modules

See [references/limitations.md](./references/limitations.md) for the detailed blind spots.
