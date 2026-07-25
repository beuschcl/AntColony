"""The simulated world's spatial foundation."""

from dataclasses import dataclass

from ant_colony.domain.moisture import MoistureMap
from ant_colony.domain.spatial import Coordinate, WorldDimensions
from ant_colony.domain.terrain import TerrainMap, TerrainType


@dataclass(frozen=True, slots=True)
class World:
    """An immutable collection of dimension-matched world layers."""

    dimensions: WorldDimensions
    terrain: TerrainMap
    moisture: MoistureMap

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

        if not isinstance(self.terrain, TerrainMap):
            raise TypeError("terrain must be TerrainMap")

        if not isinstance(self.moisture, MoistureMap):
            raise TypeError("moisture must be MoistureMap")

        if self.terrain.dimensions != self.dimensions:
            raise ValueError("terrain dimensions must match world dimensions")

        if self.moisture.dimensions != self.dimensions:
            raise ValueError("moisture dimensions must match world dimensions")

    def terrain_at(self, coordinate: Coordinate) -> TerrainType:
        """Return the terrain at a world coordinate."""

        return self.terrain.terrain_at(coordinate)

    def moisture_at(self, coordinate: Coordinate) -> int:
        """Return the moisture percentage at a world coordinate."""

        return self.moisture.moisture_at(coordinate)

    def iter_coordinates(self):
        """Return coordinates in deterministic row-major order."""

        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                yield Coordinate(x=x, y=y)


@dataclass(frozen=True, slots=True)
class World:
    """The spatial foundation of the simulated environment."""

    dimensions: WorldDimensions
    terrain: TerrainMap
    moisture: MoistureMap