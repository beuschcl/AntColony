import pytest

from ant_colony.domain import (
    Coordinate,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
)


def make_world(width: int = 10, height: int = 6) -> World:
    dimensions = WorldDimensions(width=width, height=height)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL,) * (width * height),
    )
    return World(dimensions=dimensions, terrain=terrain)


def test_world_preserves_its_dimensions_and_terrain() -> None:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.WATER),
    )

    world = World(dimensions=dimensions, terrain=terrain)

    assert world.dimensions is dimensions
    assert world.terrain is terrain


def test_world_rejects_invalid_dimensions() -> None:
    dimensions = WorldDimensions(width=1, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL,),
    )

    with pytest.raises(TypeError, match="dimensions must be WorldDimensions"):
        World(dimensions=(1, 1), terrain=terrain)  # type: ignore[arg-type]


def test_world_rejects_invalid_terrain() -> None:
    dimensions = WorldDimensions(width=1, height=1)

    with pytest.raises(TypeError, match="terrain must be TerrainMap"):
        World(dimensions=dimensions, terrain=None)  # type: ignore[arg-type]


def test_world_rejects_terrain_with_different_dimensions() -> None:
    terrain = TerrainMap(
        dimensions=WorldDimensions(width=2, height=1),
        tiles=(TerrainType.SOIL, TerrainType.ROCK),
    )

    with pytest.raises(
        ValueError,
        match="terrain dimensions must match world dimensions",
    ):
        World(
            dimensions=WorldDimensions(width=1, height=2),
            terrain=terrain,
        )


@pytest.mark.parametrize(
    ("coordinate", "expected"),
    [
        (Coordinate(0, 0), True),
        (Coordinate(9, 5), True),
        (Coordinate(-1, 0), False),
        (Coordinate(10, 5), False),
    ],
)
def test_world_determines_whether_coordinate_is_in_bounds(
    coordinate: Coordinate,
    expected: bool,
) -> None:
    world = make_world()

    assert world.contains(coordinate) is expected


def test_world_exposes_terrain_by_coordinate() -> None:
    dimensions = WorldDimensions(width=3, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.ROCK,
            TerrainType.WATER,
        ),
    )
    world = World(dimensions=dimensions, terrain=terrain)

    assert world.terrain_at(Coordinate(0, 0)) is TerrainType.SOIL
    assert world.terrain_at(Coordinate(1, 0)) is TerrainType.ROCK
    assert world.terrain_at(Coordinate(2, 0)) is TerrainType.WATER


def test_world_iterates_coordinates_in_row_major_order() -> None:
    world = make_world(width=3, height=2)

    assert list(world.iter_coordinates()) == [
        Coordinate(0, 0),
        Coordinate(1, 0),
        Coordinate(2, 0),
        Coordinate(0, 1),
        Coordinate(1, 1),
        Coordinate(2, 1),
    ]