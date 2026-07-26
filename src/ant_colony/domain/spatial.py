"""Spatial value objects for the simulated world."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Coordinate:
    """An immutable position in two-dimensional space."""

    x: int
    y: int


@dataclass(frozen=True, slots=True)
class WorldDimensions:
    """The validated width and height of a bounded world."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if (
            isinstance(self.width, bool)
            or not isinstance(self.width, int)
            or self.width <= 0
        ):
            raise ValueError("width must be a positive integer")

        if (
            isinstance(self.height, bool)
            or not isinstance(self.height, int)
            or self.height <= 0
        ):
            raise ValueError("height must be a positive integer")

    def contains(self, coordinate: Coordinate) -> bool:
        """Return whether a coordinate lies within these dimensions."""

        return 0 <= coordinate.x < self.width and 0 <= coordinate.y < self.height
