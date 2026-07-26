# Terroir Simulator Agent Instructions

## Required reading

Before proposing or making changes, read:

1. `.github/copilot-instructions.md`
2. `docs/world-v0.1.md`
3. Relevant source files and tests

These documents define the engineering rules and current domain scope.

## Current objective

Build World v0.1: a deterministic, observable environment that runs without
ants or colonies.

Do not introduce ants, colonies, ant behavior, or ant-specific infrastructure
unless explicitly requested.

## Working agreement

- Work in small, reviewable implementation slices.
- Explain the intended change before editing.
- Do not invent missing domain behavior.
- Ask before making decisions that affect simulation rules or public contracts.
- Prefer the smallest design that satisfies demonstrated requirements.
- Preserve separation between domain state, simulation rules, orchestration,
  rendering, persistence, and user interfaces.
- Keep the simulation independent of UI and storage frameworks.
- Add focused tests for every behavioral change.
- Run relevant tests before declaring work complete.
- Do not modify unrelated files.
- Do not commit or push unless explicitly requested.

## Determinism

- Supply randomness explicitly.
- Never use module-level randomness for simulation behavior.
- Do not rely on incidental collection ordering.
- Define stable processing and tie-breaking rules.
- Given identical initial state, configuration, seed, commands, and step count,
  the observable result must be identical.

## Completion report

After making changes, report:

- Files changed
- Behavior added or modified
- Tests executed and their results
- Architectural or determinism implications
- Anything intentionally deferred