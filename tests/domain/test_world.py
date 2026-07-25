import pytest

from ant_colony.domain import Coordinate, World, WorldDimensions


def test_world_preserves_its_dimensions() -> None:
    dimensions = WorldDimensions(width=10, height=6)

    world = World(dimensions=dimensions)

    assert world.dimensions is dimensions


def test_world_rejects_invalid_dimensions() -> None:
    with pytest.raises(TypeError, match="dimensions must be WorldDimensions"):
        World(dimensions=(10, 6))  # type: ignore[arg-type]


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
    world = World(dimensions=WorldDimensions(width=10, height=6))

    assert world.contains(coordinate) is expected


def test_world_iterates_coordinates_in_row_major_order() -> None:
    world = World(dimensions=WorldDimensions(width=3, height=2))

    assert list(world.iter_coordinates()) == [
        Coordinate(0, 0),
        Coordinate(1, 0),
        Coordinate(2, 0),
        Coordinate(0, 1),
        Coordinate(1, 1),
        Coordinate(2, 1),
    ]