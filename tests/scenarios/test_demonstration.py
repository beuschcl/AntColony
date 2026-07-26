from terroir_simulator.domain import (
    Coordinate,
    PlantGrowthStage,
    ResourceDeposit,
    ResourceType,
    SimulationTime,
    TerrainType,
)
from terroir_simulator.scenarios import create_demonstration_state


def test_demonstration_scenario_begins_at_step_zero() -> None:
    state = create_demonstration_state()

    assert state.time == SimulationTime(step=0)


def test_demonstration_scenario_has_expected_dimensions() -> None:
    state = create_demonstration_state()

    assert state.world.dimensions.width == 5
    assert state.world.dimensions.height == 3


def test_demonstration_scenario_contains_varied_terrain() -> None:
    state = create_demonstration_state()

    terrain_types = {
        state.world.terrain_at(coordinate)
        for coordinate in state.world.iter_coordinates()
    }

    assert terrain_types == {
        TerrainType.SOIL,
        TerrainType.MUD,
        TerrainType.ROCK,
        TerrainType.WATER,
    }


def test_demonstration_scenario_is_deterministic() -> None:
    first_state = create_demonstration_state()
    second_state = create_demonstration_state()

    assert first_state == second_state


def test_demonstration_scenario_places_mud_explicitly() -> None:
    state = create_demonstration_state()

    assert state.world.terrain_at(Coordinate(1, 1)) is TerrainType.MUD
    assert state.world.terrain_at(Coordinate(2, 1)) is TerrainType.MUD
    assert state.world.terrain_at(Coordinate(2, 2)) is TerrainType.MUD


def test_demonstration_scenario_contains_explicit_food_deposits() -> None:
    state = create_demonstration_state()

    assert state.world.resource_deposits == (
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
    )


def test_demonstration_scenario_uses_meaningful_plant_lifecycle_stages() -> None:
    state = create_demonstration_state()

    plants_by_species_id = {
        plant.species.species_id: plant for plant in state.world.all_plants()
    }

    assert (
        plants_by_species_id["flora.pennsylvania_sedge"].growth_stage
        is PlantGrowthStage.VEGETATIVE
    )
    assert (
        plants_by_species_id["flora.large_flowered_bellwort"].growth_stage
        is PlantGrowthStage.FLOWERING
    )
