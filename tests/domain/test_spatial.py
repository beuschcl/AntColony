from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import Coordinate, WorldDimensions


def test_coordinate_preserves_its_components() -> None:
    coordinate = Coordinate(x=3, y=7)

    assert coordinate.x == 3
    assert coordinate.y == 7


def test_coordinate_is_immutable() -> None:
    coordinate = Coordinate(x=3, y=7)

    with pytest.raises(FrozenInstanceError):
        coordinate.x = 4  # type: ignore[misc]


@pytest.mark.parametrize(
    ("width", "height"),
    [
        (0, 1),
        (-1, 1),
        (1, 0),
        (1, -1),
        (1.5, 1),
        (1, 1.5),
        (True, 1),
        (1, False),
    ],
)
def test_world_dimensions_reject_invalid_values(
    width: object,
    height: object,
) -> None:
    with pytest.raises(ValueError):
        WorldDimensions(width=width, height=height)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("coordinate", "expected"),
    [
        (Coordinate(0, 0), True),
        (Coordinate(9, 5), True),
        (Coordinate(-1, 0), False),
        (Coordinate(0, -1), False),
        (Coordinate(10, 0), False),
        (Coordinate(0, 6), False),
    ],
)
def test_world_dimensions_determine_whether_coordinate_is_in_bounds(
    coordinate: Coordinate,
    expected: bool,
) -> None:
    dimensions = WorldDimensions(width=10, height=6)

    assert dimensions.contains(coordinate) is expected