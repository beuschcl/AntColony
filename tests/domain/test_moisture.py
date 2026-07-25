from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import (
    Coordinate,
    MoistureMap,
    WorldDimensions,
)


def test_moisture_map_exposes_values_by_coordinate() -> None:
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=3, height=2),
        values=(
            0,
            25,
            50,
            75,
            90,
            100,
        ),
    )

    assert moisture.moisture_at(Coordinate(0, 0)) == 0
    assert moisture.moisture_at(Coordinate(2, 0)) == 50
    assert moisture.moisture_at(Coordinate(0, 1)) == 75
    assert moisture.moisture_at(Coordinate(2, 1)) == 100


def test_moisture_map_accepts_percentage_boundaries() -> None:
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=2, height=1),
        values=(0, 100),
    )

    assert moisture.values == (0, 100)


@pytest.mark.parametrize(
    "value",
    [
        -1,
        101,
        50.5,
        "50",
        True,
        False,
        None,
    ],
)
def test_moisture_map_rejects_invalid_values(
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="moisture values must be integers from 0 to 100",
    ):
        MoistureMap(
            dimensions=WorldDimensions(width=1, height=1),
            values=(value,),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "values",
    [
        (),
        (50,),
        (25, 50, 75),
    ],
)
def test_moisture_map_requires_one_value_per_coordinate(
    values: tuple[int, ...],
) -> None:
    with pytest.raises(
        ValueError,
        match="moisture value count must match dimensions",
    ):
        MoistureMap(
            dimensions=WorldDimensions(width=2, height=1),
            values=values,
        )


def test_moisture_map_requires_an_immutable_tuple() -> None:
    with pytest.raises(TypeError, match="values must be a tuple"):
        MoistureMap(
            dimensions=WorldDimensions(width=1, height=1),
            values=[50],  # type: ignore[arg-type]
        )


def test_moisture_map_rejects_invalid_dimensions() -> None:
    with pytest.raises(
        TypeError,
        match="dimensions must be WorldDimensions",
    ):
        MoistureMap(
            dimensions=None,  # type: ignore[arg-type]
            values=(50,),
        )


@pytest.mark.parametrize(
    "coordinate",
    [
        Coordinate(-1, 0),
        Coordinate(2, 0),
        Coordinate(0, -1),
        Coordinate(0, 1),
    ],
)
def test_moisture_map_rejects_out_of_bounds_coordinates(
    coordinate: Coordinate,
) -> None:
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=2, height=1),
        values=(25, 75),
    )

    with pytest.raises(
        ValueError,
        match="coordinate must be within moisture map bounds",
    ):
        moisture.moisture_at(coordinate)


def test_moisture_map_rejects_invalid_coordinate() -> None:
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=1, height=1),
        values=(50,),
    )

    with pytest.raises(TypeError, match="coordinate must be Coordinate"):
        moisture.moisture_at(None)  # type: ignore[arg-type]


def test_moisture_map_is_immutable() -> None:
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=1, height=1),
        values=(50,),
    )

    with pytest.raises(FrozenInstanceError):
        setattr(moisture, "values", (75,))