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
from ant_colony.observation import render_world


def make_state(step: int = 0) -> WorldState:
    dimensions = WorldDimensions(width=3, height=2)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.MUD,
            TerrainType.ROCK,
            TerrainType.WATER,
            TerrainType.MUD,
            TerrainType.SOIL,
        ),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(10, 20, 30, 40, 50, 60),
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


def test_render_world_displays_time_and_terrain() -> None:
    state = make_state(step=7)

    snapshot = render_world(state)

    assert snapshot == (
        "step=7\n"
        "terrain:\n"
        "SMR\n"
        "WMS\n"
        "moisture:\n"
        "010 020 030\n"
        "040 050 060"
    )


def test_render_world_displays_moisture_in_row_major_order() -> None:
    state = make_state(step=3)

    snapshot = render_world(state)

    moisture_lines = snapshot.split("\n")[snapshot.split("\n").index("moisture:") + 1:]
    assert moisture_lines == ["010 020 030", "040 050 060"]


def test_render_world_formats_moisture_values_as_three_digits() -> None:
    dimensions = WorldDimensions(width=4, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
        ),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(0, 5, 99, 100),
    )
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
    )
    state = WorldState(world=world, time=SimulationTime(step=0))

    snapshot = render_world(state)

    moisture_line = snapshot.split("\n")[-1]
    assert moisture_line == "000 005 099 100"


def test_render_world_is_deterministic() -> None:
    state = make_state(step=3)

    first_snapshot = render_world(state)
    second_snapshot = render_world(state)

    assert first_snapshot == second_snapshot


def test_render_world_does_not_modify_state() -> None:
    state = make_state(step=3)

    render_world(state)

    assert state.time == SimulationTime(step=3)
    assert state.world.terrain.tiles == (
        TerrainType.SOIL,
        TerrainType.MUD,
        TerrainType.ROCK,
        TerrainType.WATER,
        TerrainType.MUD,
        TerrainType.SOIL,
    )


def test_render_world_does_not_advance_time() -> None:
    state = make_state(step=3)

    snapshot = render_world(state)

    assert snapshot.startswith("step=3")
    assert state.time.step == 3


def test_render_world_rejects_invalid_state() -> None:
    with pytest.raises(TypeError, match="state must be WorldState"):
        render_world(None)  # type: ignore[arg-type]