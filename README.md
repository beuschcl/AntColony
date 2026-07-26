# Ant Colony

[![Test Suite](https://github.com/beuschcl/AntColony/actions/workflows/tests.yml/badge.svg)](https://github.com/beuschcl/AntColony/actions/workflows/tests.yml)

A deterministic simulation of a living environment that ants will eventually
observe, navigate, and interact with.

Development begins with World v0.1: terrain, environmental conditions, plants,
and resources without ant behavior.

## Development quality checks

Run these commands locally before opening a pull request:

- `python -m ruff format --check .`
- `python -m ruff check .`
- `python -m pytest`

To apply formatting locally:

- `python -m ruff format .`