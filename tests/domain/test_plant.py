"""Tests for the living plant domain model."""

import uuid
from dataclasses import FrozenInstanceError

import pytest

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    Plant,
    PlantGrowthStage,
    PlantId,
    PlantSpecies,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_world(width: int = 5, height: int = 4) -> World:
    dimensions = WorldDimensions(width=width, height=height)
    return World(
        dimensions=dimensions,
        terrain=TerrainMap(
            dimensions=dimensions,
            tiles=(TerrainType.SOIL,) * (width * height),
        ),
        moisture=MoistureMap(
            dimensions=dimensions,
            values=(50,) * (width * height),
        ),
    )


def make_species(species_id: str = "oak") -> PlantSpecies:
    return PlantSpecies(
        species_id=species_id,
        common_name="Oak",
        scientific_name="Quercus robur",
    )


def make_plant(
    species_id: str = "oak",
    growth_stage: PlantGrowthStage = PlantGrowthStage.MATURE,
) -> Plant:
    return Plant(
        plant_id=PlantId.generate(),
        species=make_species(species_id),
        growth_stage=growth_stage,
    )


# ---------------------------------------------------------------------------
# PlantId — stable and value-based identity
# ---------------------------------------------------------------------------


def test_plant_id_generate_returns_plant_id() -> None:
    plant_id = PlantId.generate()

    assert isinstance(plant_id, PlantId)
    assert isinstance(plant_id.value, uuid.UUID)


def test_plant_id_generate_returns_unique_ids() -> None:
    id_a = PlantId.generate()
    id_b = PlantId.generate()

    assert id_a != id_b


def test_plant_id_value_based_equality() -> None:
    shared_uuid = uuid.uuid4()

    id_a = PlantId(value=shared_uuid)
    id_b = PlantId(value=shared_uuid)

    assert id_a == id_b


def test_plant_id_inequality_for_different_uuids() -> None:
    id_a = PlantId(value=uuid.uuid4())
    id_b = PlantId(value=uuid.uuid4())

    assert id_a != id_b


def test_plant_id_is_hashable_and_usable_as_dict_key() -> None:
    plant_id = PlantId.generate()
    registry: dict[PlantId, str] = {plant_id: "oak"}

    assert registry[plant_id] == "oak"


def test_plant_id_equal_instances_share_hash() -> None:
    shared_uuid = uuid.uuid4()
    id_a = PlantId(value=shared_uuid)
    id_b = PlantId(value=shared_uuid)

    assert hash(id_a) == hash(id_b)


def test_plant_id_is_immutable() -> None:
    plant_id = PlantId.generate()

    with pytest.raises(FrozenInstanceError):
        plant_id.value = uuid.uuid4()  # type: ignore[misc]


def test_plant_id_rejects_non_uuid_value() -> None:
    with pytest.raises(TypeError, match=r"value must be uuid\.UUID"):
        PlantId(value="not-a-uuid")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# PlantSpecies — immutable structured data
# ---------------------------------------------------------------------------


def test_plant_species_preserves_all_fields() -> None:
    species = PlantSpecies(
        species_id="quercus_robur",
        common_name="English Oak",
        scientific_name="Quercus robur",
    )

    assert species.species_id == "quercus_robur"
    assert species.common_name == "English Oak"
    assert species.scientific_name == "Quercus robur"


def test_plant_species_is_immutable() -> None:
    species = make_species()

    with pytest.raises(FrozenInstanceError):
        species.common_name = "changed"  # type: ignore[misc]


def test_plant_species_value_based_equality() -> None:
    species_a = PlantSpecies(
        species_id="oak",
        common_name="Oak",
        scientific_name="Quercus robur",
    )
    species_b = PlantSpecies(
        species_id="oak",
        common_name="Oak",
        scientific_name="Quercus robur",
    )

    assert species_a == species_b


def test_plant_species_rejects_non_str_species_id() -> None:
    with pytest.raises(TypeError, match="species_id must be str"):
        PlantSpecies(
            species_id=123,  # type: ignore[arg-type]
            common_name="Oak",
            scientific_name="Quercus robur",
        )


def test_plant_species_rejects_non_str_common_name() -> None:
    with pytest.raises(TypeError, match="common_name must be str"):
        PlantSpecies(
            species_id="oak",
            common_name=None,  # type: ignore[arg-type]
            scientific_name="Quercus robur",
        )


def test_plant_species_rejects_non_str_scientific_name() -> None:
    with pytest.raises(TypeError, match="scientific_name must be str"):
        PlantSpecies(
            species_id="oak",
            common_name="Oak",
            scientific_name=42,  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# PlantGrowthStage — lifecycle representation
# ---------------------------------------------------------------------------


def test_plant_growth_stage_includes_all_required_stages() -> None:
    stages = {stage.name for stage in PlantGrowthStage}

    assert stages == {"DORMANT", "EMERGING", "MATURE", "SENESCENT", "DEAD"}


# ---------------------------------------------------------------------------
# Plant — construction and lifecycle
# ---------------------------------------------------------------------------


def test_plant_preserves_id_species_and_stage() -> None:
    plant_id = PlantId.generate()
    species = make_species()

    plant = Plant(
        plant_id=plant_id,
        species=species,
        growth_stage=PlantGrowthStage.EMERGING,
    )

    assert plant.plant_id is plant_id
    assert plant.species is species
    assert plant.growth_stage is PlantGrowthStage.EMERGING


def test_plant_is_immutable() -> None:
    plant = make_plant()

    with pytest.raises(FrozenInstanceError):
        plant.growth_stage = PlantGrowthStage.DEAD  # type: ignore[misc]


def test_plant_has_no_coordinate_attribute() -> None:
    plant = make_plant()

    assert not hasattr(plant, "coordinate")
    assert not hasattr(plant, "x")
    assert not hasattr(plant, "y")


def test_plant_rejects_invalid_plant_id() -> None:
    with pytest.raises(TypeError, match="plant_id must be PlantId"):
        Plant(
            plant_id="bad-id",  # type: ignore[arg-type]
            species=make_species(),
            growth_stage=PlantGrowthStage.MATURE,
        )


def test_plant_rejects_invalid_species() -> None:
    with pytest.raises(TypeError, match="species must be PlantSpecies"):
        Plant(
            plant_id=PlantId.generate(),
            species="not a species",  # type: ignore[arg-type]
            growth_stage=PlantGrowthStage.MATURE,
        )


def test_plant_rejects_invalid_growth_stage() -> None:
    with pytest.raises(TypeError, match="growth_stage must be PlantGrowthStage"):
        Plant(
            plant_id=PlantId.generate(),
            species=make_species(),
            growth_stage="mature",  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# World — registration and lookup by ID
# ---------------------------------------------------------------------------


def test_register_plant_makes_it_retrievable_by_id() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(1, 1))

    assert world.plant(plant.plant_id) is plant


def test_register_plant_stores_its_location() -> None:
    world = make_world()
    plant = make_plant()
    coord = Coordinate(2, 3)

    world = world.register_plant(plant, coord)

    assert world.location_of(plant.plant_id) == coord


def test_register_plant_returns_a_new_world() -> None:
    original = make_world()
    plant = make_plant()

    updated = original.register_plant(plant, Coordinate(0, 0))

    assert updated is not original


def test_register_plant_leaves_original_world_unchanged() -> None:
    original = make_world()
    plant = make_plant()

    original.register_plant(plant, Coordinate(0, 0))

    assert original.all_plants() == ()


def test_register_plant_rejects_out_of_bounds_coordinate() -> None:
    world = make_world(width=3, height=3)
    plant = make_plant()

    with pytest.raises(ValueError, match="coordinate must be within world bounds"):
        world.register_plant(plant, Coordinate(5, 5))


def test_register_plant_rejects_duplicate_plant_id() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))

    with pytest.raises(ValueError, match="plant is already registered"):
        world.register_plant(plant, Coordinate(1, 1))


def test_plant_raises_key_error_for_unknown_id() -> None:
    world = make_world()

    with pytest.raises(KeyError):
        world.plant(PlantId.generate())


def test_location_of_raises_key_error_for_unknown_id() -> None:
    world = make_world()

    with pytest.raises(KeyError):
        world.location_of(PlantId.generate())


# ---------------------------------------------------------------------------
# World — snapshot semantics
# ---------------------------------------------------------------------------


def test_world_with_different_plants_are_not_equal() -> None:
    base = make_world()
    plant = make_plant()

    world_with = base.register_plant(plant, Coordinate(0, 0))

    assert base != world_with


def test_world_is_immutable() -> None:
    world = make_world()

    with pytest.raises(FrozenInstanceError):
        world.dimensions = WorldDimensions(width=1, height=1)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# World — lookup by coordinate
# ---------------------------------------------------------------------------


def test_plants_at_returns_plant_at_coordinate() -> None:
    world = make_world()
    plant = make_plant()
    coord = Coordinate(0, 0)

    world = world.register_plant(plant, coord)

    result = world.plants_at(coord)
    assert result == (plant,)


def test_plants_at_returns_empty_tuple_for_empty_coordinate() -> None:
    world = make_world()

    result = world.plants_at(Coordinate(0, 0))
    assert result == ()


def test_plants_at_returns_tuple() -> None:
    world = make_world()

    result = world.plants_at(Coordinate(0, 0))
    assert isinstance(result, tuple)


def test_plants_at_rejects_out_of_bounds_coordinate() -> None:
    world = make_world(width=2, height=2)

    with pytest.raises(ValueError, match="coordinate must be within world bounds"):
        world.plants_at(Coordinate(10, 10))


# ---------------------------------------------------------------------------
# World — multiple plants at one coordinate
# ---------------------------------------------------------------------------


def test_plants_at_returns_all_plants_at_shared_coordinate() -> None:
    world = make_world()
    plant_a = make_plant()
    plant_b = make_plant()
    coord = Coordinate(0, 0)

    world = world.register_plant(plant_a, coord)
    world = world.register_plant(plant_b, coord)

    result = world.plants_at(coord)
    assert len(result) == 2
    assert plant_a in result
    assert plant_b in result


def test_plants_at_shared_coordinate_is_deterministically_ordered() -> None:
    world = make_world()
    coord = Coordinate(0, 0)

    plants = [make_plant() for _ in range(4)]
    for p in plants:
        world = world.register_plant(p, coord)

    result_a = world.plants_at(coord)
    result_b = world.plants_at(coord)

    assert result_a == result_b


# ---------------------------------------------------------------------------
# World — active vs. all plants
# ---------------------------------------------------------------------------


def test_all_plants_includes_registered_plant() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))

    assert plant in world.all_plants()


def test_active_plants_includes_placed_plant() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))

    assert plant in world.active_plants()


def test_all_plants_is_empty_initially() -> None:
    world = make_world()

    assert world.all_plants() == ()


def test_active_plants_is_empty_initially() -> None:
    world = make_world()

    assert world.active_plants() == ()


# ---------------------------------------------------------------------------
# World — non-destructive removal
# ---------------------------------------------------------------------------


def test_remove_plant_from_world_keeps_plant_in_registry() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))
    world = world.remove_plant_from_world(plant.plant_id)

    assert world.plant(plant.plant_id) is plant
    assert plant in world.all_plants()


def test_remove_plant_from_world_removes_from_active_plants() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))
    world = world.remove_plant_from_world(plant.plant_id)

    assert plant not in world.active_plants()


def test_remove_plant_from_world_returns_a_new_world() -> None:
    world = make_world()
    plant = make_plant()

    world_with = world.register_plant(plant, Coordinate(0, 0))
    world_without = world_with.remove_plant_from_world(plant.plant_id)

    assert world_without is not world_with


def test_remove_plant_from_world_leaves_prior_world_unchanged() -> None:
    world = make_world()
    plant = make_plant()

    world_with = world.register_plant(plant, Coordinate(0, 0))
    world_with.remove_plant_from_world(plant.plant_id)

    assert plant in world_with.active_plants()


def test_remove_plant_from_world_raises_for_unknown_id() -> None:
    world = make_world()

    with pytest.raises(KeyError):
        world.remove_plant_from_world(PlantId.generate())


def test_remove_plant_from_world_raises_when_already_removed() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(0, 0))
    world = world.remove_plant_from_world(plant.plant_id)

    with pytest.raises(ValueError, match="plant is not currently placed in the world"):
        world.remove_plant_from_world(plant.plant_id)


def test_location_of_raises_after_removal() -> None:
    world = make_world()
    plant = make_plant()

    world = world.register_plant(plant, Coordinate(1, 2))
    world = world.remove_plant_from_world(plant.plant_id)

    with pytest.raises(KeyError):
        world.location_of(plant.plant_id)


# ---------------------------------------------------------------------------
# World — dead plants remain registered and placed
# ---------------------------------------------------------------------------


def test_dead_plant_remains_registered_after_stage_does_not_change_placement() -> None:
    world = make_world()
    plant = Plant(
        plant_id=PlantId.generate(),
        species=make_species(),
        growth_stage=PlantGrowthStage.DEAD,
    )
    coord = Coordinate(0, 0)

    world = world.register_plant(plant, coord)

    assert world.plant(plant.plant_id) is plant
    assert world.location_of(plant.plant_id) == coord
    assert plant in world.plants_at(coord)
    assert plant in world.active_plants()
    assert plant in world.all_plants()


# ---------------------------------------------------------------------------
# World — spatial index consistency after removal
# ---------------------------------------------------------------------------


def test_plants_at_is_empty_after_sole_plant_removed() -> None:
    world = make_world()
    plant = make_plant()
    coord = Coordinate(0, 0)

    world = world.register_plant(plant, coord)
    world = world.remove_plant_from_world(plant.plant_id)

    assert world.plants_at(coord) == ()


def test_plants_at_retains_other_plants_after_one_is_removed() -> None:
    world = make_world()
    plant_a = make_plant()
    plant_b = make_plant()
    coord = Coordinate(0, 0)

    world = world.register_plant(plant_a, coord)
    world = world.register_plant(plant_b, coord)
    world = world.remove_plant_from_world(plant_a.plant_id)

    result = world.plants_at(coord)
    assert result == (plant_b,)


def test_all_plants_includes_both_active_and_removed_plants() -> None:
    world = make_world()
    active_plant = make_plant()
    removed_plant = make_plant()

    world = world.register_plant(active_plant, Coordinate(0, 0))
    world = world.register_plant(removed_plant, Coordinate(1, 0))
    world = world.remove_plant_from_world(removed_plant.plant_id)

    all_plants = world.all_plants()
    assert active_plant in all_plants
    assert removed_plant in all_plants
    assert len(all_plants) == 2


# ---------------------------------------------------------------------------
# World — constructor plant state validation
# ---------------------------------------------------------------------------


def _base_world_kwargs() -> dict:
    """Return keyword arguments for a minimal valid World constructor call."""
    dimensions = WorldDimensions(width=3, height=3)
    return {
        "dimensions": dimensions,
        "terrain": TerrainMap(
            dimensions=dimensions,
            tiles=(TerrainType.SOIL,) * 9,
        ),
        "moisture": MoistureMap(
            dimensions=dimensions,
            values=(50,) * 9,
        ),
    }


def test_world_rejects_non_frozenset_plant_registry() -> None:
    kwargs = _base_world_kwargs()
    with pytest.raises(TypeError, match="_plant_registry must be frozenset"):
        World(**kwargs, _plant_registry=[], _plant_locations=frozenset())  # type: ignore[arg-type]


def test_world_rejects_non_frozenset_plant_locations() -> None:
    kwargs = _base_world_kwargs()
    with pytest.raises(TypeError, match="_plant_locations must be frozenset"):
        World(**kwargs, _plant_registry=frozenset(), _plant_locations=[])  # type: ignore[arg-type]


def test_world_rejects_registry_entry_of_wrong_type() -> None:
    kwargs = _base_world_kwargs()
    with pytest.raises(
        TypeError,
        match=r"each _plant_registry entry must be a \(PlantId, Plant\) tuple",
    ):
        World(
            **kwargs,
            _plant_registry=frozenset({"not-a-tuple"}),  # type: ignore[arg-type]
            _plant_locations=frozenset(),
        )


def test_world_rejects_location_entry_of_wrong_type() -> None:
    plant = make_plant()
    kwargs = _base_world_kwargs()
    with pytest.raises(
        TypeError,
        match=r"each _plant_locations entry must be a \(PlantId, Coordinate\) tuple",
    ):
        World(
            **kwargs,
            _plant_registry=frozenset({(plant.plant_id, plant)}),
            _plant_locations=frozenset({"not-a-tuple"}),  # type: ignore[arg-type]
        )


def test_world_rejects_registry_entry_with_mismatched_key() -> None:
    plant_a = make_plant()
    plant_b = make_plant()
    kwargs = _base_world_kwargs()
    # Registry key is plant_a.plant_id but the Plant is plant_b (different plant_id).
    with pytest.raises(ValueError, match=r"registry key must match plant\.plant_id"):
        World(
            **kwargs,
            _plant_registry=frozenset({(plant_a.plant_id, plant_b)}),
            _plant_locations=frozenset(),
        )


def test_world_rejects_duplicate_plant_id_in_registry() -> None:
    plant_a = make_plant()
    plant_b = Plant(
        plant_id=plant_a.plant_id,
        species=make_species("pine"),
        growth_stage=PlantGrowthStage.DORMANT,
    )
    kwargs = _base_world_kwargs()
    # Two different Plant objects that share the same PlantId.
    with pytest.raises(ValueError, match="duplicate PlantId in _plant_registry"):
        World(
            **kwargs,
            _plant_registry=frozenset(
                {(plant_a.plant_id, plant_a), (plant_b.plant_id, plant_b)}
            ),
            _plant_locations=frozenset(),
        )


def test_world_rejects_location_referencing_unregistered_plant_id() -> None:
    plant = make_plant()
    unregistered_id = PlantId.generate()
    kwargs = _base_world_kwargs()
    with pytest.raises(
        ValueError,
        match="location PlantId must be registered in _plant_registry",
    ):
        World(
            **kwargs,
            _plant_registry=frozenset({(plant.plant_id, plant)}),
            _plant_locations=frozenset({(unregistered_id, Coordinate(0, 0))}),
        )


def test_world_rejects_duplicate_plant_id_in_locations() -> None:
    plant = make_plant()
    kwargs = _base_world_kwargs()
    # Providing two location tuples with the same PlantId but different coordinates
    # requires two distinct tuple objects; frozenset de-duplication only removes
    # identical tuples, so we embed them in a list first.
    entry_a = (plant.plant_id, Coordinate(0, 0))
    entry_b = (plant.plant_id, Coordinate(1, 0))
    with pytest.raises(ValueError, match="duplicate PlantId in _plant_locations"):
        World(
            **kwargs,
            _plant_registry=frozenset({(plant.plant_id, plant)}),
            _plant_locations=frozenset({entry_a, entry_b}),
        )


def test_world_rejects_plant_location_outside_world_bounds() -> None:
    plant = make_plant()
    kwargs = _base_world_kwargs()
    # World is 3x3; Coordinate(10, 10) is outside.
    with pytest.raises(
        ValueError,
        match="plant location coordinate must be within world bounds",
    ):
        World(
            **kwargs,
            _plant_registry=frozenset({(plant.plant_id, plant)}),
            _plant_locations=frozenset({(plant.plant_id, Coordinate(10, 10))}),
        )
