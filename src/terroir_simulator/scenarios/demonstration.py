"""Deterministic scenario used to demonstrate the world foundation."""

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    ResourceDeposit,
    ResourceType,
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

    moisture = MoistureMap(
        dimensions=dimensions,
        values=(
            30,
            15,
            10,
            100,
            100,
            40,
            75,
            80,
            100,
            100,
            35,
            45,
            70,
            20,
            15,
        ),
    )

    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
        resource_deposits=(
            ResourceDeposit(
                coordinate=Coordinate(x=0, y=0),
                resource_type=ResourceType.FOOD,
                quantity=25,
            ),
            ResourceDeposit(
                coordinate=Coordinate(x=2, y=2),
                resource_type=ResourceType.FOOD,
                quantity=10,
            ),
        ),
    )

    return WorldState(world=world)
