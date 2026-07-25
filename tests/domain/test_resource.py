from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import Coordinate, ResourceDeposit, ResourceType


def test_resource_type_includes_food() -> None:
    assert ResourceType.FOOD.value == "food"


def test_resource_deposit_retains_coordinate_type_and_quantity() -> None:
    deposit = ResourceDeposit(
        coordinate=Coordinate(x=2, y=3),
        resource_type=ResourceType.FOOD,
        quantity=25,
    )

    assert deposit.coordinate == Coordinate(x=2, y=3)
    assert deposit.resource_type is ResourceType.FOOD
    assert deposit.quantity == 25


def test_resource_deposit_is_immutable() -> None:
    deposit = ResourceDeposit(
        coordinate=Coordinate(x=0, y=0),
        resource_type=ResourceType.FOOD,
        quantity=1,
    )

    with pytest.raises(FrozenInstanceError):
        deposit.quantity = 2  # type: ignore[misc]


@pytest.mark.parametrize("quantity", [1, 10, 99])
def test_resource_deposit_accepts_positive_integer_quantities(quantity: int) -> None:
    deposit = ResourceDeposit(
        coordinate=Coordinate(x=0, y=0),
        resource_type=ResourceType.FOOD,
        quantity=quantity,
    )

    assert deposit.quantity == quantity


@pytest.mark.parametrize("quantity", [0, -1, True, False, 1.5, "1", None])
def test_resource_deposit_rejects_invalid_quantities(quantity: object) -> None:
    with pytest.raises(ValueError, match="quantity must be a positive integer"):
        ResourceDeposit(
            coordinate=Coordinate(x=0, y=0),
            resource_type=ResourceType.FOOD,
            quantity=quantity,  # type: ignore[arg-type]
        )
