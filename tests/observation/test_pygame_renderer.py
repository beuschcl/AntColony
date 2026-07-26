"""Tests for lifecycle-aware Pygame plant rendering."""

import pygame
import pytest

from terroir_simulator.domain import (
    Plant,
    PlantGrowthStage,
    PlantId,
    PlantSpecies,
)
from terroir_simulator.observation.pygame_renderer import _draw_plant

_BACKGROUND = pygame.Color("#112233")
_TILE = pygame.Rect(0, 0, 32, 32)


def make_plant(species_id: str, growth_stage: PlantGrowthStage) -> Plant:
    return Plant(
        plant_id=PlantId.generate(),
        species=PlantSpecies(
            species_id=species_id,
            common_name="Test plant",
            scientific_name="Planta testis",
        ),
        growth_stage=growth_stage,
    )


def rendered_pixels(plant: Plant) -> bytes:
    canvas = pygame.Surface(_TILE.size)
    canvas.fill(_BACKGROUND)

    _draw_plant(canvas, _TILE, plant)

    return pygame.image.tobytes(canvas, "RGBA")


@pytest.mark.parametrize(
    "species_id",
    [
        "flora.pennsylvania_sedge",
        "flora.large_flowered_bellwort",
    ],
)
@pytest.mark.parametrize(
    "growth_stage",
    [
        PlantGrowthStage.DORMANT,
        PlantGrowthStage.DEAD,
    ],
)
def test_inactive_plant_stage_has_no_aboveground_sprite(
    species_id: str,
    growth_stage: PlantGrowthStage,
) -> None:
    plant = make_plant(species_id, growth_stage)
    unchanged_canvas = pygame.Surface(_TILE.size)
    unchanged_canvas.fill(_BACKGROUND)

    assert rendered_pixels(plant) == pygame.image.tobytes(
        unchanged_canvas,
        "RGBA",
    )


@pytest.mark.parametrize(
    ("species_id", "first_stage", "second_stage"),
    [
        (
            "flora.pennsylvania_sedge",
            PlantGrowthStage.EMERGING,
            PlantGrowthStage.VEGETATIVE,
        ),
        (
            "flora.pennsylvania_sedge",
            PlantGrowthStage.VEGETATIVE,
            PlantGrowthStage.FLOWERING,
        ),
        (
            "flora.large_flowered_bellwort",
            PlantGrowthStage.EMERGING,
            PlantGrowthStage.VEGETATIVE,
        ),
        (
            "flora.large_flowered_bellwort",
            PlantGrowthStage.VEGETATIVE,
            PlantGrowthStage.FLOWERING,
        ),
        (
            "flora.large_flowered_bellwort",
            PlantGrowthStage.FLOWERING,
            PlantGrowthStage.FRUITING,
        ),
        (
            "flora.large_flowered_bellwort",
            PlantGrowthStage.VEGETATIVE,
            PlantGrowthStage.SENESCENT,
        ),
    ],
)
def test_visible_lifecycle_stages_produce_distinct_sprites(
    species_id: str,
    first_stage: PlantGrowthStage,
    second_stage: PlantGrowthStage,
) -> None:
    first_plant = make_plant(species_id, first_stage)
    second_plant = make_plant(species_id, second_stage)

    assert rendered_pixels(first_plant) != rendered_pixels(second_plant)
