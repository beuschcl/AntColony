"""The bounded world containing the simulation environment."""

from collections.abc import Iterator
from dataclasses import dataclass

from ant_colony.domain.spatial import Coordinate, WorldDimensions


@dataclass(frozen=True, slots=True)
class World:
    """A bounded two-dimensional world."""

    dimensions: WorldDimensions

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

    def contains(self, coordinate: Coordinate) -> bool:
        """Return whether a coordinate lies within this world."""

        return self.dimensions.contains(coordinate)

    def iter_coordinates(self) -> Iterator[Coordinate]:
        """Yield every world coordinate in deterministic row-major order."""

        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                yield Coordinate(x=x, y=y)