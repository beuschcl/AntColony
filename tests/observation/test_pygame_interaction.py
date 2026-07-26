import uuid

import pygame

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    Plant,
    PlantGrowthStage,
    PlantId,
    PlantSpecies,
    ResourceDeposit,
    ResourceType,
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)
from terroir_simulator.observation.pygame_renderer import (
    _coordinate_from_screen_position,
    _draw_moisture_overlay,
    _draw_selection_outline,
    _inspector_lines,
)


def test_coordinate_from_screen_position_maps_scaled_tile_clicks() -> None:
    dimensions = WorldDimensions(width=5, height=3)

    assert _coordinate_from_screen_position((129, 257), dimensions) == Coordinate(
        x=1,
        y=2,
    )
    assert _coordinate_from_screen_position((640, 10), dimensions) is None


def test_inspector_lines_show_placeholders_without_selection() -> None:
    dimensions = WorldDimensions(width=1, height=1)
    world = World(
        dimensions=dimensions,
        terrain=TerrainMap(dimensions=dimensions, tiles=(TerrainType.SOIL,)),
        moisture=MoistureMap(dimensions=dimensions, values=(25,)),
    )
    state = WorldState(world=world, time=SimulationTime(step=4))

    assert _inspector_lines(state, None) == (
        "step: 4",
        "selected: none",
        "terrain: -",
        "moisture: -",
        "food: -",
        "plants: none",
    )


def test_inspector_lines_include_selected_tile_details_and_plant_ids() -> None:
    coordinate = Coordinate(x=0, y=0)
    dimensions = WorldDimensions(width=2, height=1)
    world = World(
        dimensions=dimensions,
        terrain=TerrainMap(
            dimensions=dimensions,
            tiles=(TerrainType.MUD, TerrainType.SOIL),
        ),
        moisture=MoistureMap(dimensions=dimensions, values=(75, 30)),
        resource_deposits=(
            ResourceDeposit(
                coordinate=coordinate,
                resource_type=ResourceType.FOOD,
                quantity=7,
            ),
        ),
    )
    world = world.register_plant(
        Plant(
            plant_id=PlantId(value=uuid.UUID("00000000-0000-0000-0000-000000000001")),
            species=PlantSpecies(
                species_id="flora.alpha",
                common_name="Alpha plant",
                scientific_name="Alpha botanica",
            ),
            growth_stage=PlantGrowthStage.EMERGING,
        ),
        coordinate,
    )
    world = world.register_plant(
        Plant(
            plant_id=PlantId(value=uuid.UUID("00000000-0000-0000-0000-000000000002")),
            species=PlantSpecies(
                species_id="flora.beta",
                common_name="Beta plant",
                scientific_name="Beta botanica",
            ),
            growth_stage=PlantGrowthStage.FLOWERING,
        ),
        coordinate,
    )
    state = WorldState(world=world, time=SimulationTime(step=2))

    assert _inspector_lines(state, coordinate) == (
        "step: 2",
        "selected: (0, 0)",
        "terrain: mud",
        "moisture: 75",
        "food: 7",
        "plants:",
        "- Alpha plant",
        "  scientific: Alpha botanica",
        "  stage: emerging",
        "  plant_id: 00000000-0000-0000-0000-000000000001",
        "- Beta plant",
        "  scientific: Beta botanica",
        "  stage: flowering",
        "  plant_id: 00000000-0000-0000-0000-000000000002",
    )


def test_draw_selection_outline_marks_tile_border() -> None:
    canvas = pygame.Surface((32, 32))
    background = pygame.Color("#112233")
    canvas.fill(background)

    _draw_selection_outline(canvas, pygame.Rect(0, 0, 32, 32))

    assert canvas.get_at((0, 0)) != background
    assert canvas.get_at((16, 16)) == background


def test_draw_moisture_overlay_tints_tile() -> None:
    canvas = pygame.Surface((32, 32))
    background = pygame.Color("#667449")
    canvas.fill(background)

    _draw_moisture_overlay(canvas, pygame.Rect(0, 0, 32, 32), moisture=80)

    assert canvas.get_at((16, 16)) != background


def test_draw_moisture_overlay_leaves_dry_tile_unchanged() -> None:
    canvas = pygame.Surface((32, 32))
    background = pygame.Color("#667449")
    canvas.fill(background)

    _draw_moisture_overlay(canvas, pygame.Rect(0, 0, 32, 32), moisture=0)

    assert canvas.get_at((16, 16)) == background
