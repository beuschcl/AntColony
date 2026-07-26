# World v0.1

## Purpose

World v0.1 establishes a deterministic, observable environment before ants or
colonies are introduced.

The world must be capable of running independently so we can observe how terrain,
environmental conditions, plants, fruit, seeds, and fungus change over time.

This version establishes the environmental foundation that future entities will
inspect and interact with.

## Primary goal

Given the same:

- Initial scenario
- Configuration
- Random seed
- Sequence of commands
- Number of simulation steps

the world must produce the same observable state and event history.

## Development philosophy

World v0.1 should be:

- Simple enough to understand and observe
- Deterministic enough to reproduce
- Modular enough to extend when demonstrated behavior requires it
- Independent of any particular renderer or user interface
- Useful without ants
- Built through small, runnable vertical slices

Future-proofing means preserving clear boundaries and explicit contracts. It does
not mean implementing speculative behavior in advance.

## Included concepts

World v0.1 may contain:

- A bounded two-dimensional world
- Addressable cells and coordinates
- Terrain
- Environmental conditions
- Plants and plant lifecycle states
- Fruit production and decay
- Simple seed deposits and germination
- Fungus growth and dormancy
- Simulation time
- Deterministic random behavior
- Observable state and events
- Scenario creation
- Save, load, and replay support

Each concept will be introduced only when its implementation slice begins.

## Explicitly excluded

World v0.1 does not include:

- Ants
- Colonies
- Ant behavior
- Ant inventories
- Agent pathfinding
- Combat
- Breeding or genetics
- Individual seed identity
- Seed batches or cohorts
- Seed provenance
- Seed viability or decay
- Mixed seed types within one deposit
- Automatic seed overflow
- Multiplayer
- Distributed simulation
- Behavior added only for hypothetical future requirements

## World structure

The world is logically composed of cells addressed by coordinates.

A cell may expose environmental and ecological state without requiring all state
to be stored in one large cell object.

The precise storage representation is an implementation decision, provided that:

- Domain behavior does not depend on rendering.
- Coordinate and world boundaries are explicit.
- State ownership is unambiguous.
- Iteration order does not determine simulation outcomes.
- Future entities can inspect the world through stable domain contracts.

## Simulation time

The world advances through explicit simulation steps.

Time does not advance because a screen redraws or because real time passes. A user
interface may request a step, pause execution, or display the current state, but
it does not own simulation time.

Each completed step produces a new, observable world state.

## Update semantics

Systems may read from a stable state at the beginning of an update stage and
propose changes that are resolved together.

This prevents earlier iteration from receiving an unintended advantage merely
because it was processed first.

When order is intentionally meaningful:

- The order must be explicitly defined.
- The order must be deterministic.
- Tests must demonstrate the intended behavior.

The exact stage sequence will be documented as systems are introduced.

## Randomness

All simulation randomness must come from a random source owned or supplied by the
simulation.

Simulation code must not depend on:

- Module-level random state
- Wall-clock time
- Object memory addresses
- Set or dictionary iteration order
- Renderer timing
- Platform-specific ordering

Random behavior must be reproducible from the scenario and simulation seed.

## Plants

Plants are environmental entities with explicit lifecycle state.

The shared code-facing lifecycle vocabulary is:

- `dormant`
- `emerging`
- `vegetative`
- `flowering`
- `fruiting`
- `senescent`
- `dead`

Species may use only the stages that apply to them. Species-specific posture,
stress, transition order, thresholds, and timing are separate concerns and
remain deferred until their implementation slices define the required rules.

World v0.1 may eventually support:

- Establishment
- Growth
- Maturity
- Fruit production
- Decline or death

The exact lifecycle rules, thresholds, and timing will be introduced through
separate implementation slices. They are not implied merely by appearing in this
scope document.

## Fruit

Fruit is a plant-produced resource.

World v0.1 may allow fruit to:

- Appear on or near its producing plant
- Accumulate subject to local capacity
- Decay when its lifetime expires

Exact production, placement, capacity, and decay rules remain deferred until the
fruit implementation slice.

## Seeds

Seeds use a deliberately simplified aggregate model.

A seed deposit contains only:

```text
plant_type_id
quantity
germination_progress
```

## Rules:

- One cell may contain at most one seed type.
- Seeds are represented as whole units.
- Seeds in one deposit share one germination state.
- A plant produces seeds of its own plant type.
- Adding seeds to a matching deposit increases its quantity up to capacity.
- Seeds that do not fit are not automatically moved to nearby cells.
- A deposit cannot contain mixed plant types.
- Seeds do not decay in World v0.1.
- Seeds have no individual identity, age, viability, provenance, batch, or cohort.
- Suitable conditions allow germination progress to increase.
- Unsuitable conditions pause germination progress.
- When progress reaches its threshold, one seed may become one sprout if the plant
layer has space.
- Disturbing a deposit through collection resets its germination progress.

Ant collection and inventory behavior are not part of World v0.1. Those rules
describe the future interaction contract without introducing ants now.

## Fungus

Fungus is an environmental organism independent of ant agriculture.

World v0.1 may eventually support:

- Growth under suitable conditions
- Dormancy under unsuitable conditions
- Decline when required conditions remain absent

Exact fungus behavior remains deferred until its implementation slice.

## Observation

The environment must be inspectable without requiring direct access to private
implementation details.

Observation should eventually make it possible to examine:

- Current simulation time
- Cell state
- Environmental conditions
- Plants and lifecycle state
- Resource quantities
- Recent domain events
- Deterministic replay results

The first observer may be textual. A graphical renderer is not required to prove
the domain model.

## Architectural boundaries

The project separates these responsibilities:

- Domain state and value objects
- Simulation rules
- Step orchestration
- Scenario construction
- Observation and rendering
- Persistence and replay

Dependencies must point toward the domain model. Domain code must not import UI,
rendering, IDE, or storage-framework concerns.

## Completion criteria

World v0.1 is complete when:

- A scenario can create a deterministic environment.
- The environment can advance without ants.
- Included environmental systems interact through explicit contracts.
- The evolving world can be inspected.
- State can be saved and restored.
- A run can be replayed deterministically.
- Automated tests protect domain rules and determinism.
- The simulation can run long enough to expose ecological behavior for observation.
- The architecture provides clear interaction points for future ants.


## Deferred decisions

A behavior described as possible or eventual in this document is not permission
to invent its detailed rules.

## Each implementation slice must define:

Required behavior
- Invariants
- Configuration
- Update stage
- Conflict resolution
- Observable events
- Acceptance tests
- Explicit exclusions

If a rule is missing, implementation pauses until the rule is decided.
