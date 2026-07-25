from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import (
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)


def make_world() -> World:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.MUD),
    )
    return World(dimensions=dimensions, terrain=terrain)


def test_world_state_preserves_its_world() -> None:
    world = make_world()

    state = WorldState(world=world)

    assert state.world is world


def test_world_state_begins_at_step_zero_by_default() -> None:
    state = WorldState(world=make_world())

    assert state.time == SimulationTime(step=0)


def test_world_state_accepts_an_explicit_time() -> None:
    time = SimulationTime(step=12)

    state = WorldState(world=make_world(), time=time)

    assert state.time is time


def test_world_state_rejects_invalid_world() -> None:
    with pytest.raises(TypeError, match="world must be World"):
        WorldState(world=None)  # type: ignore[arg-type]


def test_world_state_rejects_invalid_time() -> None:
    with pytest.raises(TypeError, match="time must be SimulationTime"):
        WorldState(
            world=make_world(),
            time=0,  # type: ignore[arg-type]
        )


def test_world_state_is_immutable() -> None:
    state = WorldState(world=make_world())

    with pytest.raises(FrozenInstanceError):
        state.time = SimulationTime(step=1)  # type: ignore[misc]


def test_creating_world_state_does_not_advance_time() -> None:
    time = SimulationTime(step=3)

    state = WorldState(world=make_world(), time=time)

    assert state.time.step == 3
    assert time.step == 3