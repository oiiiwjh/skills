# Static Analysis Limitations

This skill uses Python AST parsing and does not execute the target repository.

## What It Resolves Well

- top-level functions in a module
- class methods defined in the same file
- calls through `self.method()` or `cls.method()` when the method exists in the same class
- direct imports such as `from pkg.mod import func`
- module-qualified calls such as `pkg.mod.func()` when the import can be tracked statically

## Common Blind Spots

- dynamic dispatch through variables whose runtime type is unknown
- `getattr`, `setattr`, reflection, plugin registries
- decorators that replace or wrap functions
- monkey patching after import
- star imports
- conditional imports with environment-specific behavior
- nested functions and closures as first-class graph nodes in the current version
- instance variables whose concrete class cannot be inferred statically

## Guidance

- Start with a full graph to see what resolves cleanly.
- If a specific area matters, rerun with `--entry` to reduce noise.
- Use the JSON output to inspect `unresolved_calls` when edges appear to be missing.
