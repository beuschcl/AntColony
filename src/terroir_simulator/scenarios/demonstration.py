"""Deterministic scenario used to demonstrate the world foundation."""

import uuid

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    Plant,
    PlantGrowthStage,
    PlantId,
    PlantSpecies,
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

    sedge = Plant(
        plant_id=PlantId(value=uuid.UUID("00000000-0000-0000-0000-000000000001")),
        species=PlantSpecies(
            species_id="flora.pennsylvania_sedge",
            common_name="Pennsylvania sedge",
            scientific_name="Carex pensylvanica",
        ),
        growth_stage=PlantGrowthStage.MATURE,
    )

    bellwort = Plant(
        plant_id=PlantId(value=uuid.UUID("00000000-0000-0000-0000-000000000002")),
        species=PlantSpecies(
            species_id="flora.large_flowered_bellwort",
            common_name="Large-flowered bellwort",
            scientific_name="Uvularia grandiflora",
        ),
        growth_stage=PlantGrowthStage.MATURE,
    )

    world = world.register_plant(
        sedge,
        Coordinate(x=0, y=2),
    )
    world = world.register_plant(
        bellwort,
        Coordinate(x=0, y=1),
    )

    return WorldState(world=world)
