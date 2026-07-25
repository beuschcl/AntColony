"""Deterministic scenario used to demonstrate the world foundation."""

from ant_colony.domain import (
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)


def create_demonstration_state() -> WorldState:
    """Create the initial state for the deterministic demonstration."""

    dimensions = WorldDimensions(width=5, height=3)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.ROCK,
            TerrainType.ROCK,
            TerrainType.WATER,
            TerrainType.WATER,
            TerrainType.SOIL,
            TerrainType.MUD,
            TerrainType.MUD,
            TerrainType.WATER,
            TerrainType.WATER,
            TerrainType.SOIL,
            TerrainType.SOIL,
            TerrainType.MUD,
            TerrainType.ROCK,
            TerrainType.ROCK,
        ),
    )
    world = World(dimensions=dimensions, terrain=terrain)

    return WorldState(world=world)