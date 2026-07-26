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