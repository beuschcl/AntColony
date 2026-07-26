"""Immutable resource deposits in the simulated world."""

from dataclasses import dataclass
from enum import StrEnum

from terroir_simulator.domain.spatial import Coordinate


class ResourceType(StrEnum):
    """The type of resource stored at a coordinate."""

    FOOD = "food"


@dataclass(frozen=True, slots=True)
class ResourceDeposit:
    """An immutable quantity of one resource type at a coordinate."""

    coordinate: Coordinate
    resource_type: ResourceType
    quantity: int

    def __post_init__(self) -> None:
        if not isinstance(self.coordinate, Coordinate):
            raise TypeError("coordinate must be Coordinate")

        if not isinstance(self.resource_type, ResourceType):
            raise TypeError("resource_type must be ResourceType")

        if (
            isinstance(self.quantity, bool)
            or not isinstance(self.quantity, int)
            or self.quantity <= 0
        ):
            raise ValueError("quantity must be a positive integer")
