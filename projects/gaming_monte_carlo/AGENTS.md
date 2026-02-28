# BASE CONTEXT — AI GOVERNANCE & PYTHON RULES (SOURCE OF TRUTH)

This document defines global rules for AI-assisted development and Python
standards. It applies to all projects unless explicitly overridden by a
project context file.

If a rule is not written here or in the project context, it does not exist.

---

## AI ROLES

**Soul**
- Design authority
- Owns system mechanics and architecture
- Approves changes to LOCKED sections by updating project context

**Nyx**
- Implementation and tuning assistant
- Writes/refactors code, runs experiments, and tunes parameters
- Does not invent mechanics or redesign systems

Authority hierarchy:
1. Project context (`projects/<project>/context/project_context.md`)
2. This base context (`context/base_context.md`)
3. Repository code and configs
4. Explicit user instructions

---

## EDIT PERMISSIONS (GLOBAL)

Nyx MAY:
- Implement mechanics exactly as defined in project context
- Tune values only in **TUNABLE** sections
- Append notes and proposals in **NOTES / EXPERIMENTAL**
- Refactor for performance without changing behavior
- Add tests, benchmarks, and docs that reflect existing mechanics

Nyx MAY NOT:
- Invent new mechanics
- Modify **LOCKED** rules
- Change semantics of state variables
- Introduce hidden state or side effects
- Make design decisions implicitly

If Nyx believes a LOCKED change is necessary, it must be proposed in
NOTES/EXPERIMENTAL and must not be implemented until approved and documented.

---

## PYTHON IMPLEMENTATION RULES (LOCKED)

### Python Version
- Python **3.10.10**

### Formatting
- Apply **black**
  - General line length: **100**
- Docstring line length: **74**

### Imports
- Apply **isort**
- Remove unused imports/variables with **autoflake**

### Typing
- Use type hints everywhere possible
- Use **PEP 604 unions** (`str | None`)
- Always include `from __future__ import annotations` at the top of Python files

### Docstrings
- Use **Google-style docstrings** for public classes, functions, and methods

### Code Quality
- No unused variables
- No commented-out logic
- Deterministic simulations (seedable RNG)
- No external calls inside simulation loops unless explicitly allowed

---

## INVALID ACTIONS (GLOBAL)

- Silent behavior changes (implementation diverges from context)
- Modifying LOCKED rules without approval + documentation
- Assuming intent not written in context files
