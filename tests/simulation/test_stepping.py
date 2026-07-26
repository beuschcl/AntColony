import pytest

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    Plant,
    PlantGrowthStage,
    PlantId,
    PlantSpecies,
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)
from terroir_simulator.simulation import advance_world


def make_state(step: int = 0) -> WorldState:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.MUD),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(25, 75),
    )
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
    )

    return WorldState(
        world=world,
        time=SimulationTime(step=step),
    )


def make_plant(stage: PlantGrowthStage = PlantGrowthStage.MATURE) -> Plant:
    return Plant(
        plant_id=PlantId.generate(),
        species=PlantSpecies(
            species_id="oak",
            common_name="Oak",
            scientific_name="Quercus robur",
        ),
        growth_stage=stage,
    )


def test_advance_world_advances_time_exactly_once() -> None:
    current_state = make_state(step=3)

    next_state = advance_world(current_state)

    assert next_state.time == SimulationTime(step=4)


def test_advance_world_returns_a_new_state() -> None:
    current_state = make_state()

    next_state = advance_world(current_state)

    assert next_state is not current_state


def test_advance_world_preserves_the_terrain() -> None:
    current_state = make_state()

    next_state = advance_world(current_state)

    assert next_state.world.terrain is current_state.world.terrain


def test_advance_world_does_not_modify_the_current_state() -> None:
    current_state = make_state(step=3)

    advance_world(current_state)

    assert current_state.time == SimulationTime(step=3)


def test_each_explicit_advance_completes_one_step() -> None:
    state_at_zero = make_state()

    state_at_one = advance_world(state_at_zero)
    state_at_two = advance_world(state_at_one)

    assert state_at_zero.time == SimulationTime(step=0)
    assert state_at_one.time == SimulationTime(step=1)
    assert state_at_two.time == SimulationTime(step=2)


def test_advance_world_rejects_invalid_state() -> None:
    with pytest.raises(TypeError, match="state must be WorldState"):
        advance_world(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Plant state preservation across simulation steps
# ---------------------------------------------------------------------------


def test_advance_world_preserves_all_registered_plants() -> None:
    state = make_state()
    plant = make_plant()
    world = state.world.register_plant(plant, Coordinate(0, 0))
    state = WorldState(world=world, time=state.time)

    next_state = advance_world(state)

    assert next_state.world.plant(plant.plant_id) is plant


def test_advance_world_preserves_current_plant_locations() -> None:
    state = make_state()
    plant = make_plant()
    coord = Coordinate(1, 0)
    world = state.world.register_plant(plant, coord)
    state = WorldState(world=world, time=state.time)

    next_state = advance_world(state)

    assert next_state.world.location_of(plant.plant_id) == coord


def test_advance_world_preserves_multiple_plants_at_same_coordinate() -> None:
    state = make_state()
    plant_a = make_plant()
    plant_b = make_plant()
    coord = Coordinate(0, 0)
    world = state.world.register_plant(plant_a, coord)
    world = world.register_plant(plant_b, coord)
    state = WorldState(world=world, time=state.time)

    next_state = advance_world(state)

    result = next_state.world.plants_at(coord)
    assert plant_a in result
    assert plant_b in result
    assert len(result) == 2


def test_advance_world_preserves_removed_plant_in_all_plants() -> None:
    state = make_state()
    active_plant = make_plant()
    removed_plant = make_plant()
    world = state.world.register_plant(active_plant, Coordinate(0, 0))
    world = world.register_plant(removed_plant, Coordinate(1, 0))
    world = world.remove_plant_from_world(removed_plant.plant_id)
    state = WorldState(world=world, time=state.time)

    next_state = advance_world(state)

    assert removed_plant in next_state.world.all_plants()
    assert removed_plant not in next_state.world.active_plants()
    assert active_plant in next_state.world.active_plants()


def test_advance_world_prior_state_plant_registry_unchanged() -> None:
    state = make_state()
    plant = make_plant()
    world = state.world.register_plant(plant, Coordinate(0, 0))
    state_with_plant = WorldState(world=world, time=state.time)

    advance_world(state_with_plant)

    assert plant in state_with_plant.world.all_plants()
