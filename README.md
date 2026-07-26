# Terroir Simulator

[![Test Suite](https://github.com/beuschcl/terroir-simulator/actions/workflows/tests.yml/badge.svg)](https://github.com/beuschcl/terroir-simulator/actions/workflows/tests.yml)

A cozy, observable ecosystem simulation where the character of the world
emerges from its environment.

A deterministic simulation of a living environment that ants will eventually
observe, navigate, and interact with.

Development begins with World v0.1: terrain, environmental conditions, plants,
and resources without ant behavior.

## Development quality checks

Run these commands locally before opening a pull request:

- `python -m ruff format --check .`
- `python -m ruff check .`
- `python -m mypy`
- `python -m pytest`
- `python -m terroir_simulator`

To apply formatting locally:

- `python -m ruff format .`

## Running the demonstrations

- Text demonstration: `python -m terroir_simulator`
- Interactive graphical observer: `python -m terroir_simulator.graphical_demo`

### Graphical observer controls

- `Space` advances one simulation step.
- `P` toggles play and pause.
- `R` restores the original demonstration state and pauses playback.
- `M` toggles the moisture overlay.
- Left click selects a world tile for inspection.
- `Up` / `Down` scroll the inspector panel when needed.
- `Esc` closes the window.