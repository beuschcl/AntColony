"""Immutable terrain definitions for the simulated world."""

from dataclasses import dataclass
from enum import StrEnum

from ant_colony.domain.spatial import Coordinate, WorldDimensions


class TerrainType(StrEnum):
    """The physical substrate assigned to a world coordinate."""

    SOIL = "soil"
    MUD = "mud"
    ROCK = "rock"
    WATER = "water"


@dataclass(frozen=True, slots=True)
class TerrainMap:
    """An immutable terrain assignment for every coordinate in a world."""

    dimensions: WorldDimensions
    tiles: tuple[TerrainType, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

        if not isinstance(self.tiles, tuple):
            raise TypeError("tiles must be a tuple")

        expected_tile_count = self.dimensions.width * self.dimensions.height

        if len(self.tiles) != expected_tile_count:
            raise ValueError(f"terrain requires exactly {expected_tile_count} tiles")

        if any(not isinstance(tile, TerrainType) for tile in self.tiles):
            raise TypeError("every tile must be TerrainType")

    def terrain_at(self, coordinate: Coordinate) -> TerrainType:
        """Return the terrain assigned to an in-bounds coordinate."""

        if not self.dimensions.contains(coordinate):
            raise ValueError("coordinate is outside the terrain map")

        index = coordinate.y * self.dimensions.width + coordinate.x
        return self.tiles[index]
