---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

# Explain Code

## Overview

Use this skill when the user wants to understand code rather than change it. The explanation should make unfamiliar code feel concrete, visual, and easy to follow.

Every explanation must include:
- an everyday analogy first
- an ASCII diagram
- a step-by-step walkthrough of what the code does
- one gotcha, misconception, or easy-to-miss detail

Keep the tone conversational. For complex topics, use more than one analogy if that makes the explanation clearer.

## Workflow

1. Identify the code unit to explain: function, class, module, request flow, state machine, or subsystem.
2. Scan for the real entrypoints, inputs, outputs, side effects, and dependencies before explaining.
3. Start with an analogy that matches the code's role.
4. Draw a compact ASCII diagram that shows control flow, data flow, or object relationships.
5. Walk through execution in the order a reader would mentally simulate it.
6. Call out one gotcha:
   - hidden mutation
   - async ordering
   - shared state
   - caching behavior
   - error handling edge cases
   - framework lifecycle behavior
7. End with a short recap only if it adds clarity.

## Explanation Template

Use this structure by default:

~~~markdown
Analogy:
[plain-language comparison]

Diagram:
~~~text
[ASCII diagram]
~~~

Walkthrough:
1. ...
2. ...
3. ...

Gotcha:
[common mistake or misconception]
~~~

Adjust the headings if the user asks for a different format, but keep all four elements.

## Diagram Guidelines

- Prefer simple ASCII over dense notation.
- Show direction with arrows.
- Label important state transitions and decision points.
- Keep diagrams narrow enough to read in a normal terminal.
- If the system has multiple layers, use one overview diagram and then one focused diagram for the tricky part.

Example patterns:

```text
Request -> Router -> Handler -> Service -> DB
                     |
                     v
                  Response
```

```text
input
  |
  v
parse -> validate -> transform -> save
                     |
                     v
                  return id
```

## Analogy Guidelines

- Choose everyday systems: mailrooms, kitchens, assembly lines, librarians, traffic control, checklists.
- Match the analogy to the actual mechanics of the code.
- Do not stretch the analogy past its useful boundary.
- If the analogy breaks down, say where it stops being accurate.

## Gotcha Guidance

Always include at least one concrete gotcha. Good gotchas are specific and testable:
- "This mutates the original list in place."
- "The callback runs later, so `result` is still unset here."
- "This cache key ignores locale, so different languages can collide."
- "The constructor looks cheap, but it opens a network connection."

Avoid vague warnings like "performance may be affected" unless you name the exact reason.

## Examples

Use this skill for prompts like:
- "How does this function work?"
- "Explain this class to a junior engineer."
- "Walk me through this request flow."
- "Why does this React component re-render?"
- "Can you teach me this codebase?"

## References

There are no bundled scripts or references for this skill. Read the target code directly and explain only what is relevant to the user's question.
