"""The bounded world containing the simulation environment."""

from collections.abc import Iterator
from dataclasses import dataclass

from ant_colony.domain.spatial import Coordinate, WorldDimensions
from ant_colony.domain.terrain import TerrainMap, TerrainType


@dataclass(frozen=True, slots=True)
class World:
    """A bounded two-dimensional world with immutable terrain."""

    dimensions: WorldDimensions
    terrain: TerrainMap

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

        if not isinstance(self.terrain, TerrainMap):
            raise TypeError("terrain must be TerrainMap")

        if self.terrain.dimensions != self.dimensions:
            raise ValueError("terrain dimensions must match world dimensions")

    def contains(self, coordinate: Coordinate) -> bool:
        """Return whether a coordinate lies within this world."""

        return self.dimensions.contains(coordinate)

    def terrain_at(self, coordinate: Coordinate) -> TerrainType:
        """Return the terrain assigned to a world coordinate."""

        return self.terrain.terrain_at(coordinate)

    def iter_coordinates(self) -> Iterator[Coordinate]:
        """Yield every world coordinate in deterministic row-major order."""

        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                yield Coordinate(x=x, y=y)