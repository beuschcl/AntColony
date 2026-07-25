import pytest

from ant_colony.domain import (
    MoistureMap,
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)
from ant_colony.simulation import advance_world


def make_state(step: int = 0) -> WorldState:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.MUD),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(25, 75),
    )
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
    )

    return WorldState(
        world=world,
        time=SimulationTime(step=step),
    )


def test_advance_world_advances_time_exactly_once() -> None:
    current_state = make_state(step=3)

    next_state = advance_world(current_state)

    assert next_state.time == SimulationTime(step=4)


def test_advance_world_returns_a_new_state() -> None:
    current_state = make_state()

    next_state = advance_world(current_state)

    assert next_state is not current_state


def test_advance_world_preserves_the_terrain() -> None:
    current_state = make_state()

    next_state = advance_world(current_state)

    assert next_state.world.terrain is current_state.world.terrain


def test_advance_world_does_not_modify_the_current_state() -> None:
    current_state = make_state(step=3)

    advance_world(current_state)

    assert current_state.time == SimulationTime(step=3)


def test_each_explicit_advance_completes_one_step() -> None:
    state_at_zero = make_state()

    state_at_one = advance_world(state_at_zero)
    state_at_two = advance_world(state_at_one)

    assert state_at_zero.time == SimulationTime(step=0)
    assert state_at_one.time == SimulationTime(step=1)
    assert state_at_two.time == SimulationTime(step=2)


def test_advance_world_rejects_invalid_state() -> None:
    with pytest.raises(TypeError, match="state must be WorldState"):
        advance_world(None)  # type: ignore[arg-type]