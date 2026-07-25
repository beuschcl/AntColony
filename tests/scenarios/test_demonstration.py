from ant_colony.domain import (
    Coordinate,
    SimulationTime,
    TerrainType,
)
from ant_colony.scenarios import create_demonstration_state


def test_demonstration_scenario_begins_at_step_zero() -> None:
    state = create_demonstration_state()

    assert state.time == SimulationTime(step=0)


def test_demonstration_scenario_has_expected_dimensions() -> None:
    state = create_demonstration_state()

    assert state.world.dimensions.width == 5
    assert state.world.dimensions.height == 3


def test_demonstration_scenario_contains_varied_terrain() -> None:
    state = create_demonstration_state()

    terrain_types = {
        state.world.terrain_at(coordinate)
        for coordinate in state.world.iter_coordinates()
    }

    assert terrain_types == {
        TerrainType.SOIL,
        TerrainType.MUD,
        TerrainType.ROCK,
        TerrainType.WATER,
    }


def test_demonstration_scenario_is_deterministic() -> None:
    first_state = create_demonstration_state()
    second_state = create_demonstration_state()

    assert first_state == second_state


def test_demonstration_scenario_places_mud_explicitly() -> None:
    state = create_demonstration_state()

    assert state.world.terrain_at(Coordinate(1, 1)) is TerrainType.MUD
    assert state.world.terrain_at(Coordinate(2, 1)) is TerrainType.MUD
    assert state.world.terrain_at(Coordinate(2, 2)) is TerrainType.MUD