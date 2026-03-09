#!/usr/bin/env python3
"""Generate a static call graph for a Python repository."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import deque
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any


DEFAULT_SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
}

DEFAULT_TEST_DIR_NAMES = {"tests", "test"}


@dataclass(frozen=True)
class Symbol:
    qualified_name: str
    dotted_name: str
    module_name: str
    file_path: str
    line: int
    kind: str
    class_name: str | None = None


@dataclass
class CallableContext:
    symbol: Symbol
    imports: dict[str, str]
    body: list[ast.stmt]
    module_name: str
    class_name: str | None = None


@dataclass
class AnalysisResult:
    symbols: dict[str, Symbol] = field(default_factory=dict)
    dotted_index: dict[str, str] = field(default_factory=dict)
    module_functions: dict[str, dict[str, str]] = field(default_factory=dict)
    module_classes: dict[str, set[str]] = field(default_factory=dict)
    class_methods: dict[tuple[str, str], dict[str, str]] = field(default_factory=dict)
    edges: set[tuple[str, str]] = field(default_factory=set)
    unresolved_calls: list[dict[str, Any]] = field(default_factory=list)
    parsed_files: int = 0
    skipped_files: int = 0
    parse_errors: list[dict[str, str]] = field(default_factory=list)


class CallCollector(ast.NodeVisitor):
    """Collect call expressions while skipping nested callable definitions."""

    def __init__(self) -> None:
        self.calls: list[tuple[ast.AST, int]] = []

    def visit_Call(self, node: ast.Call) -> None:
        self.calls.append((node.func, node.lineno))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_Lambda(self, node: ast.Lambda) -> None:
        return

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a static Mermaid and/or JSON call graph for a Python repository."
    )
    parser.add_argument("repo_path", help="Path to the target Python repository")
    parser.add_argument("--entry", help="Qualified symbol to use as the graph entrypoint")
    parser.add_argument(
        "--format",
        choices=("mermaid", "json", "both"),
        default="both",
        help="Output format",
    )
    parser.add_argument(
        "--output",
        help="Output file path. With --format both, acts as the output basename.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        help="Maximum traversal depth from --entry. Only applies with --entry.",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test directories and files in the scan",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="GLOB",
        help="Additional glob pattern to ignore. Can be passed multiple times.",
    )
    return parser.parse_args()


def is_test_path(path: Path) -> bool:
    path_parts = set(path.parts)
    if path_parts.intersection(DEFAULT_TEST_DIR_NAMES):
        return True
    name = path.name
    return name.startswith("test_") or name.endswith("_test.py")


def should_skip_dir(path: Path, repo_root: Path, include_tests: bool, ignore_globs: list[str]) -> bool:
    rel_dir = path.relative_to(repo_root).as_posix()
    if path.name in DEFAULT_SKIP_DIRS:
        return True
    if not include_tests and (path.name in DEFAULT_TEST_DIR_NAMES or fnmatch(rel_dir, "tests/*")):
        return True
    return any(fnmatch(rel_dir, pattern) for pattern in ignore_globs)


def should_skip_file(path: Path, repo_root: Path, include_tests: bool, ignore_globs: list[str]) -> bool:
    rel_file = path.relative_to(repo_root).as_posix()
    if any(fnmatch(rel_file, pattern) for pattern in ignore_globs):
        return True
    if not include_tests and is_test_path(path.relative_to(repo_root)):
        return True
    return False


def module_name_for_path(repo_root: Path, file_path: Path) -> str:
    rel_path = file_path.relative_to(repo_root)
    parts = list(rel_path.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def import_prefix(module_name: str, level: int) -> str:
    if level <= 0:
        return ""
    parts = module_name.split(".")
    if level > len(parts):
        return ""
    return ".".join(parts[:-level])


def resolve_import_module(module_name: str, node: ast.ImportFrom) -> str:
    base_module = node.module or ""
    if node.level <= 0:
        return base_module
    prefix = import_prefix(module_name, node.level)
    if base_module:
        return ".".join(part for part in (prefix, base_module) if part)
    return prefix


def dotted_to_qualified(dotted_name: str) -> str:
    parts = dotted_name.split(".")
    if len(parts) < 2:
        return dotted_name
    if len(parts) >= 3 and parts[-2][:1].isupper():
        module_part = ".".join(parts[:-2])
        name_part = ".".join(parts[-2:])
    else:
        module_part = ".".join(parts[:-1])
        name_part = parts[-1]
    return f"{module_part}::{name_part}" if module_part else dotted_name


def collect_imports(module_name: str, tree: ast.AST) -> dict[str, str]:
    imports: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                alias_name = alias.asname or alias.name.split(".")[0]
                imports[alias_name] = alias.name
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                continue
            base_module = resolve_import_module(module_name, node)
            for alias in node.names:
                alias_name = alias.asname or alias.name
                if base_module:
                    imports[alias_name] = f"{base_module}.{alias.name}"
                else:
                    imports[alias_name] = alias.name
    return imports


def register_symbol(result: AnalysisResult, symbol: Symbol) -> None:
    result.symbols[symbol.qualified_name] = symbol
    result.dotted_index[symbol.dotted_name] = symbol.qualified_name
    if symbol.class_name:
        key = (symbol.module_name, symbol.class_name)
        result.class_methods.setdefault(key, {})[symbol.qualified_name.split(".")[-1]] = symbol.qualified_name
        result.module_classes.setdefault(symbol.module_name, set()).add(symbol.class_name)
    else:
        result.module_functions.setdefault(symbol.module_name, {})[
            symbol.qualified_name.split("::", 1)[1]
        ] = symbol.qualified_name


def analyze_repository(
    repo_root: Path, include_tests: bool, ignore_globs: list[str]
) -> tuple[AnalysisResult, list[CallableContext]]:
    result = AnalysisResult()
    contexts: list[CallableContext] = []

    for file_path in sorted(repo_root.rglob("*.py")):
        if should_skip_file(file_path, repo_root, include_tests, ignore_globs):
            result.skipped_files += 1
            continue
        relative_parents = file_path.relative_to(repo_root).parents
        if any(
            should_skip_dir(repo_root / parent, repo_root, include_tests, ignore_globs)
            for parent in relative_parents
            if str(parent) != "."
        ):
            result.skipped_files += 1
            continue

        module_name = module_name_for_path(repo_root, file_path)
        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(file_path))
            result.parsed_files += 1
        except Exception as exc:
            result.parse_errors.append({"file": str(file_path), "error": str(exc)})
            continue

        imports = collect_imports(module_name, tree)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualified_name = f"{module_name}::{node.name}"
                symbol = Symbol(
                    qualified_name=qualified_name,
                    dotted_name=f"{module_name}.{node.name}",
                    module_name=module_name,
                    file_path=str(file_path),
                    line=node.lineno,
                    kind="function",
                )
                register_symbol(result, symbol)
                contexts.append(
                    CallableContext(
                        symbol=symbol,
                        imports=imports,
                        body=node.body,
                        module_name=module_name,
                    )
                )
            elif isinstance(node, ast.ClassDef):
                result.module_classes.setdefault(module_name, set()).add(node.name)
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        qualified_name = f"{module_name}::{node.name}.{child.name}"
                        symbol = Symbol(
                            qualified_name=qualified_name,
                            dotted_name=f"{module_name}.{node.name}.{child.name}",
                            module_name=module_name,
                            file_path=str(file_path),
                            line=child.lineno,
                            kind="method",
                            class_name=node.name,
                        )
                        register_symbol(result, symbol)
                        contexts.append(
                            CallableContext(
                                symbol=symbol,
                                imports=imports,
                                body=child.body,
                                module_name=module_name,
                                class_name=node.name,
                            )
                        )

    return result, contexts


def attribute_to_parts(node: ast.AST) -> list[str] | None:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        base = attribute_to_parts(node.value)
        if base is None:
            return None
        return base + [node.attr]
    return None


def resolve_name(name: str, context: CallableContext, result: AnalysisResult) -> str | None:
    if context.class_name:
        class_methods = result.class_methods.get((context.module_name, context.class_name), {})
        if name in class_methods:
            return class_methods[name]
    module_functions = result.module_functions.get(context.module_name, {})
    if name in module_functions:
        return module_functions[name]
    imported = context.imports.get(name)
    if imported:
        return resolve_dotted_target(imported.split("."), context, result, {})
    return None


def resolve_dotted_target(
    parts: list[str],
    context: CallableContext,
    result: AnalysisResult,
    local_types: dict[str, tuple[str, str]],
) -> str | None:
    if not parts:
        return None
    if parts[0] in {"self", "cls"} and context.class_name:
        class_methods = result.class_methods.get((context.module_name, context.class_name), {})
        if len(parts) == 2 and parts[1] in class_methods:
            return class_methods[parts[1]]
        return None
    if parts[0] in local_types and len(parts) == 2:
        module_name, class_name = local_types[parts[0]]
        class_methods = result.class_methods.get((module_name, class_name), {})
        if parts[1] in class_methods:
            return class_methods[parts[1]]
        return None

    if len(parts) == 2 and context.class_name and parts[0] == context.class_name:
        dotted_name = f"{context.module_name}.{parts[0]}.{parts[1]}"
        return result.dotted_index.get(dotted_name)

    expanded_parts = parts
    alias_target = context.imports.get(parts[0])
    if alias_target:
        expanded_parts = alias_target.split(".") + parts[1:]

    dotted_name = ".".join(expanded_parts)
    if dotted_name in result.dotted_index:
        return result.dotted_index[dotted_name]

    if len(expanded_parts) == 2:
        same_module_dotted = f"{context.module_name}.{expanded_parts[0]}.{expanded_parts[1]}"
        if same_module_dotted in result.dotted_index:
            return result.dotted_index[same_module_dotted]

    return None


def resolve_class_target(
    parts: list[str], context: CallableContext, result: AnalysisResult
) -> tuple[str, str] | None:
    if not parts:
        return None

    if len(parts) == 1:
        if parts[0] in result.module_classes.get(context.module_name, set()):
            return context.module_name, parts[0]
        imported = context.imports.get(parts[0])
        if imported:
            return resolve_class_target(imported.split("."), context, result)
        return None

    alias_target = context.imports.get(parts[0])
    expanded_parts = alias_target.split(".") + parts[1:] if alias_target else parts
    module_name = ".".join(expanded_parts[:-1])
    class_name = expanded_parts[-1]
    if class_name in result.module_classes.get(module_name, set()):
        return module_name, class_name
    return None


def expr_to_text(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return ast.dump(node, include_attributes=False)


def infer_local_types(
    context: CallableContext, result: AnalysisResult
) -> dict[str, tuple[str, str]]:
    inferred: dict[str, tuple[str, str]] = {}
    for stmt in context.body:
        if not isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            continue
        value = stmt.value
        if not isinstance(value, ast.Call):
            continue
        if isinstance(value.func, ast.Name):
            class_target = resolve_class_target([value.func.id], context, result)
        else:
            parts = attribute_to_parts(value.func)
            class_target = resolve_class_target(parts or [], context, result)
        if class_target is None:
            continue

        targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
        for target in targets:
            if isinstance(target, ast.Name):
                inferred[target.id] = class_target
    return inferred


def collect_edges(result: AnalysisResult, contexts: list[CallableContext]) -> None:
    for context in contexts:
        local_types = infer_local_types(context, result)
        collector = CallCollector()
        for stmt in context.body:
            collector.visit(stmt)

        for call_expr, lineno in collector.calls:
            resolved_target: str | None = None
            if isinstance(call_expr, ast.Name):
                resolved_target = resolve_name(call_expr.id, context, result)
            else:
                parts = attribute_to_parts(call_expr)
                if parts is not None:
                    resolved_target = resolve_dotted_target(parts, context, result, local_types)

            if resolved_target:
                result.edges.add((context.symbol.qualified_name, resolved_target))
            else:
                result.unresolved_calls.append(
                    {
                        "caller": context.symbol.qualified_name,
                        "call": expr_to_text(call_expr),
                        "line": lineno,
                    }
                )


def filter_graph(
    result: AnalysisResult, entry: str | None, max_depth: int | None
) -> tuple[list[Symbol], list[tuple[str, str]], list[dict[str, Any]], list[str]]:
    if not entry:
        nodes = sorted(result.symbols.values(), key=lambda item: item.qualified_name)
        edges = sorted(result.edges)
        unresolved = sorted(result.unresolved_calls, key=lambda item: (item["caller"], item["line"], item["call"]))
        return nodes, edges, unresolved, []

    if entry not in result.symbols:
        raise ValueError(f"Entrypoint not found: {entry}")

    adjacency: dict[str, list[str]] = {}
    for source, target in result.edges:
        adjacency.setdefault(source, []).append(target)

    visited = {entry}
    queue: deque[tuple[str, int]] = deque([(entry, 0)])
    while queue:
        current, depth = queue.popleft()
        if max_depth is not None and depth >= max_depth:
            continue
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    nodes = [result.symbols[name] for name in sorted(visited)]
    edges = sorted((source, target) for source, target in result.edges if source in visited and target in visited)
    unresolved = sorted(
        (item for item in result.unresolved_calls if item["caller"] in visited),
        key=lambda item: (item["caller"], item["line"], item["call"]),
    )
    return nodes, edges, unresolved, [entry]


def mermaid_id(symbol_name: str) -> str:
    safe = []
    for char in symbol_name:
        safe.append(char if char.isalnum() else "_")
    identifier = "".join(safe).strip("_")
    return f"n_{identifier}" if identifier else "n_root"


def build_mermaid(nodes: list[Symbol], edges: list[tuple[str, str]]) -> str:
    lines = ["graph TD"]
    for symbol in nodes:
        lines.append(f'    {mermaid_id(symbol.qualified_name)}["{symbol.qualified_name}"]')
    for source, target in edges:
        lines.append(f"    {mermaid_id(source)} --> {mermaid_id(target)}")
    return "\n".join(lines)


def build_json_payload(
    nodes: list[Symbol],
    edges: list[tuple[str, str]],
    unresolved_calls: list[dict[str, Any]],
    result: AnalysisResult,
    entrypoints: list[str],
) -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": symbol.qualified_name,
                "dotted_name": symbol.dotted_name,
                "module": symbol.module_name,
                "kind": symbol.kind,
                "class_name": symbol.class_name,
                "file": symbol.file_path,
                "line": symbol.line,
            }
            for symbol in nodes
        ],
        "edges": [{"source": source, "target": target} for source, target in edges],
        "entrypoints": entrypoints,
        "unresolved_calls": unresolved_calls,
        "stats": {
            "parsed_files": result.parsed_files,
            "skipped_files": result.skipped_files,
            "parse_errors": len(result.parse_errors),
            "symbol_count": len(nodes),
            "edge_count": len(edges),
            "unresolved_call_count": len(unresolved_calls),
        },
        "parse_errors": result.parse_errors,
    }


def write_output(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def emit_outputs(args: argparse.Namespace, mermaid: str, json_text: str) -> None:
    if args.output:
        output_path = Path(args.output)
        if args.format == "mermaid":
            write_output(output_path, mermaid)
        elif args.format == "json":
            write_output(output_path, json_text)
        else:
            write_output(output_path.with_suffix(".mmd"), mermaid)
            write_output(output_path.with_suffix(".json"), json_text)
        return

    if args.format == "mermaid":
        print(mermaid)
    elif args.format == "json":
        print(json_text)
    else:
        print(mermaid)
        print()
        print(json_text)


def validate_args(args: argparse.Namespace) -> int | None:
    if args.max_depth is not None and args.max_depth < 0:
        print("error: --max-depth must be >= 0", file=sys.stderr)
        return 2
    if args.max_depth is not None and not args.entry:
        print("error: --max-depth requires --entry", file=sys.stderr)
        return 2
    return None


def main() -> int:
    args = parse_args()
    error_code = validate_args(args)
    if error_code is not None:
        return error_code

    repo_root = Path(args.repo_path).expanduser().resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print(f"error: repository path does not exist or is not a directory: {repo_root}", file=sys.stderr)
        return 2

    try:
        result, contexts = analyze_repository(repo_root, args.include_tests, args.ignore)
        collect_edges(result, contexts)
        nodes, edges, unresolved_calls, entrypoints = filter_graph(result, args.entry, args.max_depth)
        mermaid = build_mermaid(nodes, edges)
        payload = build_json_payload(nodes, edges, unresolved_calls, result, entrypoints)
        json_text = json.dumps(payload, indent=2, sort_keys=False)
        emit_outputs(args, mermaid, json_text)
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
