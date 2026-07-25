"""Domain model for the Ant Colony environment."""

from ant_colony.domain.spatial import Coordinate, WorldDimensions
from ant_colony.domain.terrain import TerrainMap, TerrainType
from ant_colony.domain.world import World

__all__ = [
    "Coordinate",
    "TerrainMap",
    "TerrainType",
    "World",
    "WorldDimensions",
]