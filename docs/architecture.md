# Terroir Simulator Architecture

## Purpose

This document defines the architectural boundaries for World v0.1.

The architecture exists to keep simulation behavior deterministic, observable, and
independent of presentation and storage technologies.

## Dependency direction

Dependencies point inward toward the domain:

```text
Interfaces and rendering
          ↓
Application orchestration
          ↓
Simulation rules
          ↓
Domain model
```
Persistence implements contracts defined by inner layers. The domain does not depend
on persistence, rendering, user interfaces, or frameworks.

## Architectural areas
### Domain

The domain contains the state and vocabulary of the simulated world.

Examples may eventually include:

- Coordinates
- World dimensions
- Terrain
- Environmental conditions
- Plants
- Fruit
- Seed deposits
- Fungus
- Simulation time
- Domain events

The domain:
- Defines invariants.
- Uses plain Python.
- Does not render output.
- Does not read files or databases.
- Does not know which interface controls the simulation.
- Does not use uncontrolled randomness.

### Simulation 

The simulation area contains rules that change domain state.

Examples may eventually include:

- Environmental updates
- Plant lifecycle rules
- Fruit production and decay
- Seed germination
- Fungus behavior
- Conflict resolution
- Deterministic update stages

Simulation rules:

- Receive required state and dependencies explicitly.
- Use explicitly supplied randomness.
- Define stable ordering and tie-breaking.
- Do not depend on rendering or persistence.
- Produce observable results or events.

### Application

The application area coordinates use cases.

Examples may eventually include:

- Create a scenario.
- Advance the world by one step.
- Run multiple steps.
- Inspect the current state.
- Save or load a world.
- Replay recorded commands.

The application layer controls sequencing but does not contain ecological rules.

### Interfaces

Interfaces translate between users or external systems and application operations.

Possible interfaces include:

- A command-line interface
- A textual observer
- A graphical renderer
- A future interactive application

Interfaces may display or request changes, but they do not own simulation time or
domain behavior.

### Persistence

Persistence stores and restores simulation information.

It may eventually support:

- World snapshots
- Scenario definitions
- Command histories
- Replay data

Serialization and storage formats must not become part of the core domain model.

## Initial package direction

The project will use a ```src``` layout:
```
src/
└── terroir_simulator/
    ├── domain/
    ├── simulation/
    ├── application/
    ├── interfaces/
    └── persistence/

tests/
├── domain/
├── simulation/
├── application/
├── interfaces/
└── persistence/
```

Directories will be introduced only when the first real responsibility belongs in
them. Empty architectural layers do not need placeholder implementation code.

## Cross-boundary rules
- Domain code must not import from outer architectural areas.
- Simulation rules may depend on domain types.
- Application code may coordinate domain and simulation behavior.
- Interfaces may call application operations.
- Persistence may implement contracts required by application workflows.
- Rendering must not change domain state directly.
- Framework-specific types must not leak into the domain.
- Circular dependencies are prohibited.
- Public contracts require tests and documentation.

## Determinism boundary

Determinism is a system-wide contract.

All code affecting simulation results must avoid:

- Uncontrolled randomness
- Wall-clock dependencies
- Incidental collection ordering
- Memory-address-based behavior
- Rendering or interface timing
- Platform-specific ordering

Given the same initial state, configuration, seed, commands, and step count, the
observable state and event history must be identical.

## Growth rule

New abstractions are introduced only when a concrete implementation slice requires
them.

Before adding a new architectural component, identify:

1. Its responsibility.
2. The contract it exposes.
3. The layer that owns it.
4. Its dependencies.
5. How its behavior will be tested.

Missing domain rules must be resolved before implementation.
