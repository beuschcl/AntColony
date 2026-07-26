"""Immutable moisture conditions across world coordinates."""

from dataclasses import dataclass

from ant_colony.domain.spatial import Coordinate, WorldDimensions


@dataclass(frozen=True, slots=True)
class MoistureMap:
    """A whole-number moisture percentage for every coordinate."""

    dimensions: WorldDimensions
    values: tuple[int, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

        if not isinstance(self.values, tuple):
            raise TypeError("values must be a tuple")

        expected_count = self.dimensions.width * self.dimensions.height

        if len(self.values) != expected_count:
            raise ValueError("moisture value count must match dimensions")

        if any(
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 0 <= value <= 100
            for value in self.values
        ):
            raise ValueError("moisture values must be integers from 0 to 100")

    def moisture_at(self, coordinate: Coordinate) -> int:
        """Return the moisture percentage at a coordinate."""

        if not isinstance(coordinate, Coordinate):
            raise TypeError("coordinate must be Coordinate")

        if not (
            0 <= coordinate.x < self.dimensions.width
            and 0 <= coordinate.y < self.dimensions.height
        ):
            raise ValueError("coordinate must be within moisture map bounds")

        index = coordinate.y * self.dimensions.width + coordinate.x
        return self.values[index]
