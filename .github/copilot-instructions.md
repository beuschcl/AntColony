# Ant Colony Copilot Instructions

## Project intent

Ant Colony is a deterministic simulation of a living environment that ants will
eventually observe, navigate, and interact with.

Development currently focuses only on World v0.1: the environment without ants.

## Working principles

- Implement the smallest solution that satisfies the current task.
- Do not invent domain behavior that has not been documented.
- Do not add ants or ant-specific logic until explicitly requested.
- Keep simulation behavior independent of rendering, input, and UI frameworks.
- Prefer clear, explicit Python over clever or highly condensed code.
- Prefer composition and small focused types over deep inheritance hierarchies.
- Do not add abstractions solely for hypothetical future requirements.
- Keep domain objects free of UI and persistence concerns.
- Use type hints for public functions, methods, and attributes.
- Use descriptive names rather than abbreviations.
- Explain any necessary deviation from these instructions before implementing it.

## Determinism

- All simulation randomness must come from an explicitly supplied random source.
- Never use module-level random state for simulation behavior.
- Never use collection iteration order as a simulation rule.
- Define deterministic tie-breaking wherever multiple outcomes are possible.
- Read stage behavior from a stable starting state and commit proposed changes
  together when simultaneous resolution is required.
- The same scenario, seed, configuration, and commands must produce the same result.

## Architecture boundaries

- Keep the domain model independent of PyCharm, graphical libraries, and storage.
- Separate world state, simulation rules, orchestration, rendering, and persistence.
- Domain rules belong in the simulation domain—not in rendering or interface code.
- Dependencies should point toward the domain model.
- Add extension points only when an actual requirement needs them.
- Preserve explicit boundaries between layers.

## World v0.1 scope

World v0.1 may include:

- World dimensions and cells
- Terrain
- Environmental conditions
- Plants
- Fruit
- Simple seed deposits
- Fungus
- Simulation time
- Deterministic updates
- Inspection and replay support

World v0.1 excludes:

- Ants
- Colonies
- Ant inventories
- Pathfinding for agents
- Individual seed identities
- Seed cohorts
- Seed provenance
- Seed viability or decay
- Automatic seed-deposit overflow
- Speculative multiplayer or distributed-simulation infrastructure

## Simplified seed rule

A seed deposit has only:

- `plant_type_id`
- `quantity`
- `germination_progress`

One cell may contain one seed type. Seeds have no individual identity, age,
provenance, viability, or cohort history in World v0.1.

## Testing

- Add or update focused tests for every behavioral change.
- Test externally observable behavior rather than private implementation details.
- Include determinism tests for behavior involving randomness or tie-breaking.
- Keep tests readable and arrange them around one behavior at a time.
- Run the relevant tests after every implementation change.
- Do not weaken or delete a test merely to make a change pass.

## Task workflow

Before editing:

1. Read the relevant repository documentation.
2. Inspect the affected code and tests.
3. Summarize the intended change.
4. Identify missing or conflicting requirements.
5. Stop and ask when a domain rule is genuinely ambiguous.

While editing:

1. Stay within the requested task.
2. Avoid unrelated cleanup or refactoring.
3. Keep changes small enough to review.
4. Update documentation when a public contract changes.

After editing:

1. Run the relevant tests.
2. Summarize every changed file.
3. Explain how determinism and architecture boundaries were preserved.
4. List anything intentionally deferred.