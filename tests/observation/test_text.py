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
        "040 050 060\n"
        "food:\n"
        "000 000 000\n"
        "000 000 000"
    )


def test_render_world_displays_moisture_in_row_major_order() -> None:
    state = make_state(step=3)

    snapshot = render_world(state)

    lines = snapshot.split("\n")
    moisture_start = lines.index("moisture:") + 1
    food_index = lines.index("food:")
    moisture_lines = lines[moisture_start:food_index]
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

    lines = snapshot.split("\n")
    moisture_start = lines.index("moisture:") + 1
    food_index = lines.index("food:")
    moisture_line = lines[moisture_start:food_index][0]
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


def _make_food_world(deposits: tuple[ResourceDeposit, ...]) -> WorldState:
    """Return a minimal 3x1 world with the given resource deposits."""

    dimensions = WorldDimensions(width=3, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.SOIL, TerrainType.SOIL),
    )
    moisture = MoistureMap(dimensions=dimensions, values=(0, 0, 0))
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
        resource_deposits=deposits,
    )
    return WorldState(world=world, time=SimulationTime(step=0))


def _food_lines(snapshot: str) -> list[str]:
    """Return the food grid rows from a rendered snapshot."""

    lines = snapshot.split("\n")
    food_start = lines.index("food:") + 1
    return lines[food_start:]


def test_render_world_displays_food_section_after_moisture() -> None:
    state = make_state(step=0)

    snapshot = render_world(state)

    lines = snapshot.split("\n")
    moisture_index = lines.index("moisture:")
    food_index = lines.index("food:")
    assert food_index > moisture_index


def test_render_world_renders_absent_food_as_000() -> None:
    state = _make_food_world(deposits=())

    snapshot = render_world(state)

    assert _food_lines(snapshot) == ["000 000 000"]


def test_render_world_formats_food_values_as_three_digits() -> None:
    deposits = (
        ResourceDeposit(
            coordinate=Coordinate(x=0, y=0),
            resource_type=ResourceType.FOOD,
            quantity=5,
        ),
        ResourceDeposit(
            coordinate=Coordinate(x=1, y=0),
            resource_type=ResourceType.FOOD,
            quantity=99,
        ),
        ResourceDeposit(
            coordinate=Coordinate(x=2, y=0),
            resource_type=ResourceType.FOOD,
            quantity=100,
        ),
    )
    state = _make_food_world(deposits=deposits)

    snapshot = render_world(state)

    assert _food_lines(snapshot) == ["005 099 100"]


def test_render_world_displays_food_in_row_major_order() -> None:
    dimensions = WorldDimensions(width=3, height=2)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.SOIL,
        ),
    )
    moisture = MoistureMap(dimensions=dimensions, values=(0, 0, 0, 0, 0, 0))
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
        resource_deposits=(
            ResourceDeposit(
                coordinate=Coordinate(x=0, y=0),
                resource_type=ResourceType.FOOD,
                quantity=1,
            ),
            ResourceDeposit(
                coordinate=Coordinate(x=2, y=1),
                resource_type=ResourceType.FOOD,
                quantity=2,
            ),
        ),
    )
    state = WorldState(world=world, time=SimulationTime(step=0))

    snapshot = render_world(state)

    assert _food_lines(snapshot) == ["001 000 000", "000 000 002"]


def test_render_world_food_is_static_across_steps() -> None:
    from ant_colony.simulation import run_steps

    state_before = make_state(step=0)
    state_after = run_steps(state_before, steps=3, evaporation_rate=1)

    snapshot_before = render_world(state_before)
    snapshot_after = render_world(state_after)

    food_before = _food_lines(snapshot_before)
    food_after = _food_lines(snapshot_after)
    assert food_before == food_after