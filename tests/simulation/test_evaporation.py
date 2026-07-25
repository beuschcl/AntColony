"""Tests for moisture evaporation behavior."""

import pytest

from ant_colony.domain import (
    Coordinate,
    MoistureMap,
    ResourceDeposit,
    ResourceType,
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)
from ant_colony.simulation import advance_world, run_steps


def make_state(
    tiles: tuple[TerrainType, ...],
    values: tuple[int, ...],
    resource_deposits: tuple[ResourceDeposit, ...] = (),
    step: int = 0,
) -> WorldState:
    dimensions = WorldDimensions(width=len(tiles), height=1)
    terrain = TerrainMap(dimensions=dimensions, tiles=tiles)
    moisture = MoistureMap(dimensions=dimensions, values=values)
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
        resource_deposits=resource_deposits,
    )
    return WorldState(world=world, time=SimulationTime(step=step))


# ---------------------------------------------------------------------------
# Basic evaporation per step
# ---------------------------------------------------------------------------


def test_non_water_cell_loses_exactly_evaporation_rate_per_step() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    next_state = advance_world(state, evaporation_rate=3)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 47


def test_evaporation_applies_to_all_non_water_terrain_types() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL, TerrainType.MUD, TerrainType.ROCK),
        values=(40, 60, 80),
    )

    next_state = advance_world(state, evaporation_rate=5)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 35
    assert next_state.world.moisture_at(Coordinate(1, 0)) == 55
    assert next_state.world.moisture_at(Coordinate(2, 0)) == 75


# ---------------------------------------------------------------------------
# Clamping at zero
# ---------------------------------------------------------------------------


def test_moisture_is_clamped_at_zero() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(2,),
    )

    next_state = advance_world(state, evaporation_rate=10)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 0


def test_moisture_at_zero_stays_at_zero() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(0,),
    )

    next_state = advance_world(state, evaporation_rate=5)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 0


# ---------------------------------------------------------------------------
# Water terrain
# ---------------------------------------------------------------------------


def test_water_coordinate_has_moisture_100_after_step() -> None:
    state = make_state(
        tiles=(TerrainType.WATER,),
        values=(100,),
    )

    next_state = advance_world(state, evaporation_rate=10)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 100


def test_water_does_not_evaporate_regardless_of_rate() -> None:
    state = make_state(
        tiles=(TerrainType.WATER,),
        values=(100,),
    )

    next_state = advance_world(state, evaporation_rate=100)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 100


def test_water_and_non_water_cells_update_independently() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL, TerrainType.WATER),
        values=(40, 100),
    )

    next_state = advance_world(state, evaporation_rate=7)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 33
    assert next_state.world.moisture_at(Coordinate(1, 0)) == 100


# ---------------------------------------------------------------------------
# Rate of zero
# ---------------------------------------------------------------------------


def test_rate_of_zero_leaves_non_water_moisture_unchanged() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL, TerrainType.MUD),
        values=(30, 70),
    )

    next_state = advance_world(state, evaporation_rate=0)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 30
    assert next_state.world.moisture_at(Coordinate(1, 0)) == 70


# ---------------------------------------------------------------------------
# Multiple steps
# ---------------------------------------------------------------------------


def test_multiple_steps_apply_evaporation_once_per_step() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(20,),
    )

    final_state = run_steps(state, steps=4, evaporation_rate=3)

    assert final_state.world.moisture_at(Coordinate(0, 0)) == 8


def test_multiple_steps_clamp_correctly() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(5,),
    )

    final_state = run_steps(state, steps=3, evaporation_rate=3)

    assert final_state.world.moisture_at(Coordinate(0, 0)) == 0


def test_water_stays_100_across_multiple_steps() -> None:
    state = make_state(
        tiles=(TerrainType.WATER,),
        values=(100,),
    )

    final_state = run_steps(state, steps=10, evaporation_rate=5)

    assert final_state.world.moisture_at(Coordinate(0, 0)) == 100


# ---------------------------------------------------------------------------
# Terrain is preserved
# ---------------------------------------------------------------------------


def test_terrain_is_unchanged_after_evaporation() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL, TerrainType.WATER),
        values=(50, 100),
    )

    next_state = advance_world(state, evaporation_rate=1)

    assert next_state.world.terrain.tiles == state.world.terrain.tiles


def test_terrain_object_identity_is_preserved() -> None:
    state = make_state(
        tiles=(TerrainType.MUD, TerrainType.ROCK),
        values=(60, 80),
    )

    next_state = advance_world(state, evaporation_rate=2)

    assert next_state.world.terrain is state.world.terrain


# ---------------------------------------------------------------------------
# Immutability of preceding state
# ---------------------------------------------------------------------------


def test_preceding_state_moisture_is_unchanged_after_advance() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )
    original_values = state.world.moisture.values

    advance_world(state, evaporation_rate=5)

    assert state.world.moisture.values == original_values


def test_preceding_world_is_unchanged_after_advance() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )
    original_world = state.world

    advance_world(state, evaporation_rate=5)

    assert state.world is original_world


# ---------------------------------------------------------------------------
# Invalid evaporation rates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "evaporation_rate",
    [
        -1,
        -100,
    ],
)
def test_negative_evaporation_rate_is_rejected(
    evaporation_rate: object,
) -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        advance_world(state, evaporation_rate=evaporation_rate)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "evaporation_rate",
    [
        True,
        False,
    ],
)
def test_boolean_evaporation_rate_is_rejected(
    evaporation_rate: object,
) -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        advance_world(state, evaporation_rate=evaporation_rate)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "evaporation_rate",
    [
        1.0,
        "1",
        None,
        1.5,
    ],
)
def test_non_integer_evaporation_rate_is_rejected(
    evaporation_rate: object,
) -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        advance_world(state, evaporation_rate=evaporation_rate)  # type: ignore[arg-type]


def test_run_steps_rejects_negative_evaporation_rate() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        run_steps(state, steps=0, evaporation_rate=-1)


def test_run_steps_rejects_boolean_evaporation_rate() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        run_steps(state, steps=0, evaporation_rate=True)  # type: ignore[arg-type]


def test_run_steps_rejects_non_integer_evaporation_rate() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(50,),
    )

    with pytest.raises(
        ValueError,
        match="evaporation_rate must be a non-negative integer",
    ):
        run_steps(state, steps=0, evaporation_rate=1.0)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_evaporation_result_is_deterministic() -> None:
    state = make_state(
        tiles=(TerrainType.SOIL, TerrainType.WATER, TerrainType.MUD),
        values=(40, 100, 60),
    )

    first_result = advance_world(state, evaporation_rate=4)
    second_result = advance_world(state, evaporation_rate=4)

    assert first_result.world.moisture.values == second_result.world.moisture.values


def test_processing_order_does_not_affect_result() -> None:
    """All values are computed from the same starting state atomically."""
    dimensions = WorldDimensions(width=3, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.SOIL, TerrainType.SOIL),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(10, 20, 30),
    )
    world = World(dimensions=dimensions, terrain=terrain, moisture=moisture)
    state = WorldState(world=world)

    next_state = advance_world(state, evaporation_rate=2)

    assert next_state.world.moisture_at(Coordinate(0, 0)) == 8
    assert next_state.world.moisture_at(Coordinate(1, 0)) == 18
    assert next_state.world.moisture_at(Coordinate(2, 0)) == 28


def test_resource_deposits_are_preserved_after_one_evaporation_step() -> None:
    resource_deposits = (
        ResourceDeposit(
            coordinate=Coordinate(0, 0),
            resource_type=ResourceType.FOOD,
            quantity=25,
        ),
    )
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(40,),
        resource_deposits=resource_deposits,
    )

    next_state = advance_world(state, evaporation_rate=4)

    assert next_state.world.resource_deposits is resource_deposits
    assert next_state.world.resource_quantity_at(Coordinate(0, 0), ResourceType.FOOD) == 25


def test_resource_deposits_remain_unchanged_over_multiple_steps() -> None:
    resource_deposits = (
        ResourceDeposit(
            coordinate=Coordinate(0, 0),
            resource_type=ResourceType.FOOD,
            quantity=25,
        ),
    )
    initial_state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(40,),
        resource_deposits=resource_deposits,
    )

    final_state = run_steps(initial_state, steps=3, evaporation_rate=2)

    assert final_state.world.resource_deposits is resource_deposits
    assert final_state.world.resource_quantity_at(Coordinate(0, 0), ResourceType.FOOD) == 25


def test_previous_world_and_state_resource_deposits_remain_unchanged() -> None:
    resource_deposits = (
        ResourceDeposit(
            coordinate=Coordinate(0, 0),
            resource_type=ResourceType.FOOD,
            quantity=25,
        ),
    )
    state = make_state(
        tiles=(TerrainType.SOIL,),
        values=(40,),
        resource_deposits=resource_deposits,
    )

    advance_world(state, evaporation_rate=1)

    assert state.world.resource_deposits is resource_deposits
    assert state.world.resource_quantity_at(Coordinate(0, 0), ResourceType.FOOD) == 25
