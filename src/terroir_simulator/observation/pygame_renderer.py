"""Pygame observation of an immutable world snapshot."""

import pygame

from terroir_simulator.domain import (
    Coordinate,
    Plant,
    PlantGrowthStage,
    ResourceType,
    TerrainType,
    WorldDimensions,
    WorldState,
)
from terroir_simulator.simulation import advance_world

_TILE_SIZE = 32
_DISPLAY_SCALE = 4
_PLAYBACK_STEP_MS = 300
_EVAPORATION_RATE = 1
_PANEL_WIDTH = 380
_PANEL_MARGIN = 16
_PANEL_BACKGROUND = pygame.Color("#1d1c18")
_PANEL_TEXT = pygame.Color("#ebe2c8")
_PANEL_DIVIDER = pygame.Color("#4a4435")
_SELECTION_COLOR = pygame.Color("#f6e37a")
_MOISTURE_OVERLAY = pygame.Color("#6d9dd8")

_TERRAIN_COLORS: dict[TerrainType, pygame.Color] = {
    TerrainType.SOIL: pygame.Color("#667449"),
    TerrainType.MUD: pygame.Color("#514936"),
    TerrainType.ROCK: pygame.Color("#77745f"),
    TerrainType.WATER: pygame.Color("#4e7f80"),
}


def show_world(state: WorldState) -> None:
    """Open a window displaying a world snapshot."""

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    pygame.init()

    logical_size = (
        state.world.dimensions.width * _TILE_SIZE,
        state.world.dimensions.height * _TILE_SIZE,
    )
    world_display_size = (
        logical_size[0] * _DISPLAY_SCALE,
        logical_size[1] * _DISPLAY_SCALE,
    )
    display_size = (world_display_size[0] + _PANEL_WIDTH, world_display_size[1])

    try:
        canvas = pygame.Surface(logical_size)
        window = pygame.display.set_mode(display_size)
        pygame.display.set_caption("Terroir Simulator")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)

        initial_state = state
        current_state = state
        selected_coordinate: Coordinate | None = None
        show_moisture_overlay = False
        is_playing = False
        accumulated_playback_ms = 0

        running = True
        while running:
            elapsed_ms = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_state = advance_world(
                            current_state,
                            evaporation_rate=_EVAPORATION_RATE,
                        )
                        accumulated_playback_ms = 0
                    elif event.key == pygame.K_p:
                        is_playing = not is_playing
                        accumulated_playback_ms = 0
                    elif event.key == pygame.K_r:
                        current_state = initial_state
                        is_playing = False
                        accumulated_playback_ms = 0
                    elif event.key == pygame.K_m:
                        show_moisture_overlay = not show_moisture_overlay
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    selected_coordinate = _coordinate_from_screen_position(
                        event.pos,
                        current_state.world.dimensions,
                    )

            if is_playing:
                accumulated_playback_ms += elapsed_ms
                while accumulated_playback_ms >= _PLAYBACK_STEP_MS:
                    current_state = advance_world(
                        current_state,
                        evaporation_rate=_EVAPORATION_RATE,
                    )
                    accumulated_playback_ms -= _PLAYBACK_STEP_MS

            _draw_world(
                canvas,
                current_state,
                selected_coordinate=selected_coordinate,
                show_moisture_overlay=show_moisture_overlay,
            )

            window.fill(_PANEL_BACKGROUND)
            enlarged = pygame.transform.scale(canvas, world_display_size)
            window.blit(enlarged, (0, 0))
            _draw_inspector_panel(
                window,
                pygame.Rect(
                    world_display_size[0],
                    0,
                    _PANEL_WIDTH,
                    world_display_size[1],
                ),
                font,
                current_state,
                selected_coordinate,
            )
            pygame.display.flip()
    finally:
        pygame.quit()


def _draw_world(
    canvas: pygame.Surface,
    state: WorldState,
    *,
    selected_coordinate: Coordinate | None = None,
    show_moisture_overlay: bool = False,
) -> None:
    """Draw terrain and resources without changing world state."""

    canvas.fill(pygame.Color("black"))

    for coordinate in state.world.iter_coordinates():
        terrain = state.world.terrain_at(coordinate)
        tile = pygame.Rect(
            coordinate.x * _TILE_SIZE,
            coordinate.y * _TILE_SIZE,
            _TILE_SIZE,
            _TILE_SIZE,
        )

        pygame.draw.rect(canvas, _TERRAIN_COLORS[terrain], tile)
        _draw_terrain_details(canvas, tile, terrain, coordinate)

        if show_moisture_overlay:
            _draw_moisture_overlay(
                canvas,
                tile,
                moisture=state.world.moisture_at(coordinate),
            )

        food = state.world.resource_quantity_at(
            coordinate,
            ResourceType.FOOD,
        )
        if food > 0:
            _draw_berries(canvas, tile)

        for plant in state.world.plants_at(coordinate):
            _draw_plant(canvas, tile, plant)

        if coordinate == Coordinate(x=4, y=2):
            _draw_preview_ant(canvas, tile)

        if coordinate == selected_coordinate:
            _draw_selection_outline(canvas, tile)


def _coordinate_from_screen_position(
    position: tuple[int, int],
    dimensions: WorldDimensions,
) -> Coordinate | None:
    """Return the selected world coordinate for a scaled screen position."""

    if not isinstance(dimensions, WorldDimensions):
        raise TypeError("dimensions must be WorldDimensions")

    x, y = position
    if x < 0 or y < 0:
        return None

    coordinate = Coordinate(
        x=x // (_TILE_SIZE * _DISPLAY_SCALE),
        y=y // (_TILE_SIZE * _DISPLAY_SCALE),
    )
    if not dimensions.contains(coordinate):
        return None

    return coordinate


def _inspector_lines(
    state: WorldState,
    selected_coordinate: Coordinate | None,
) -> tuple[str, ...]:
    """Return deterministic inspector text for the selected coordinate."""

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    lines = [f"step: {state.time.step}"]

    if selected_coordinate is None:
        return (
            *lines,
            "selected: none",
            "terrain: -",
            "moisture: -",
            "food: -",
            "plants: none",
        )

    if not state.world.contains(selected_coordinate):
        raise ValueError("selected_coordinate must be within world bounds")

    food_quantity = state.world.resource_quantity_at(
        selected_coordinate,
        ResourceType.FOOD,
    )
    lines.extend(
        (
            f"selected: ({selected_coordinate.x}, {selected_coordinate.y})",
            f"terrain: {state.world.terrain_at(selected_coordinate).value}",
            f"moisture: {state.world.moisture_at(selected_coordinate)}",
            f"food: {food_quantity}",
        )
    )

    plants = state.world.plants_at(selected_coordinate)
    if not plants:
        lines.append("plants: none")
        return tuple(lines)

    lines.append("plants:")
    for plant in plants:
        lines.extend(
            (
                f"- {plant.species.common_name}",
                f"  scientific: {plant.species.scientific_name}",
                f"  stage: {plant.growth_stage.value}",
                f"  plant_id: {plant.plant_id.value}",
            )
        )

    return tuple(lines)


def _draw_inspector_panel(
    surface: pygame.Surface,
    panel: pygame.Rect,
    font: pygame.font.Font,
    state: WorldState,
    selected_coordinate: Coordinate | None,
) -> None:
    """Draw an inspector panel beside the world view."""

    pygame.draw.rect(surface, _PANEL_BACKGROUND, panel)
    pygame.draw.line(surface, _PANEL_DIVIDER, panel.topleft, panel.bottomleft, 2)

    y = panel.top + _PANEL_MARGIN
    for line in _inspector_lines(state, selected_coordinate):
        label = font.render(line, True, _PANEL_TEXT)
        surface.blit(label, (panel.left + _PANEL_MARGIN, y))
        y += font.get_linesize()


def _draw_selection_outline(canvas: pygame.Surface, tile: pygame.Rect) -> None:
    """Draw a visible outline around the selected tile."""

    pygame.draw.rect(canvas, _SELECTION_COLOR, tile, 2)


def _draw_moisture_overlay(
    canvas: pygame.Surface,
    tile: pygame.Rect,
    *,
    moisture: int,
) -> None:
    """Tint a tile by its moisture so evaporation becomes visible."""

    if moisture <= 0:
        return

    alpha = 32 + ((moisture * 128) // 100)
    overlay = pygame.Surface(tile.size, pygame.SRCALPHA)
    overlay.fill((*_MOISTURE_OVERLAY[:3], alpha))
    canvas.blit(overlay, tile.topleft)


def _draw_terrain_details(
    canvas: pygame.Surface,
    tile: pygame.Rect,
    terrain: TerrainType,
    coordinate: Coordinate,
) -> None:
    """Add deterministic pixel details that identify each terrain type."""

    if terrain is TerrainType.SOIL:
        color = pygame.Color("#87945d")
        for index in range(5):
            x = tile.left + 4 + ((coordinate.x * 7 + index * 11) % 24)
            y = tile.top + 5 + ((coordinate.y * 9 + index * 7) % 22)
            pygame.draw.rect(canvas, color, (x, y, 2, 2))

    elif terrain is TerrainType.MUD:
        pygame.draw.line(
            canvas,
            pygame.Color("#71664a"),
            (tile.left + 3, tile.centery + 5),
            (tile.right - 4, tile.centery + 2),
            2,
        )
        pygame.draw.rect(
            canvas,
            pygame.Color("#403b2e"),
            (tile.left + 8, tile.top + 8, 3, 2),
        )

    elif terrain is TerrainType.ROCK:
        points = (
            (tile.left + 5, tile.bottom - 6),
            (tile.left + 8, tile.top + 9),
            (tile.centerx + 3, tile.top + 5),
            (tile.right - 5, tile.top + 12),
            (tile.right - 3, tile.bottom - 7),
        )
        pygame.draw.polygon(canvas, pygame.Color("#96917a"), points)
        pygame.draw.line(
            canvas,
            pygame.Color("#b3ad91"),
            points[1],
            points[2],
            2,
        )

    elif terrain is TerrainType.WATER:
        for offset in (8, 17, 25):
            pygame.draw.line(
                canvas,
                pygame.Color("#75a5a0"),
                (tile.left + 3, tile.top + offset),
                (tile.right - 4, tile.top + offset),
                1,
            )


def _draw_berries(canvas: pygame.Surface, tile: pygame.Rect) -> None:
    """Draw food as a readable pile of separate red berries."""

    shadow = pygame.Color("#3f352e")
    red = pygame.Color("#a83f45")
    highlight = pygame.Color("#d66a62")
    leaf = pygame.Color("#394f32")

    pygame.draw.ellipse(
        canvas,
        shadow,
        (tile.centerx - 10, tile.centery + 7, 20, 5),
    )

    centers = (
        (tile.centerx - 6, tile.centery + 4),
        (tile.centerx, tile.centery + 6),
        (tile.centerx + 6, tile.centery + 3),
        (tile.centerx - 2, tile.centery),
        (tile.centerx + 4, tile.centery - 2),
    )

    for x, y in centers:
        pygame.draw.circle(canvas, red, (x, y), 4)
        pygame.draw.rect(canvas, highlight, (x - 1, y - 2, 2, 1))

    pygame.draw.polygon(
        canvas,
        leaf,
        (
            (tile.centerx, tile.centery - 5),
            (tile.centerx - 7, tile.centery - 9),
            (tile.centerx - 5, tile.centery - 3),
        ),
    )


def _draw_plant(
    canvas: pygame.Surface,
    tile: pygame.Rect,
    plant: Plant,
) -> None:
    """Draw a plant according to its species identity and lifecycle stage."""

    if plant.growth_stage in {
        PlantGrowthStage.DORMANT,
        PlantGrowthStage.DEAD,
    }:
        return

    if plant.species.species_id == "flora.pennsylvania_sedge":
        _draw_sedge(canvas, tile, plant.growth_stage)
    elif plant.species.species_id == "flora.large_flowered_bellwort":
        _draw_bellwort(canvas, tile, plant.growth_stage)


def _draw_sedge(
    canvas: pygame.Surface,
    tile: pygame.Rect,
    growth_stage: PlantGrowthStage,
) -> None:
    """Draw Pennsylvania sedge using only its supplied lifecycle stage."""

    shadow = pygame.Color("#3f4c32")
    dark_green = pygame.Color("#526b3d")
    light_green = pygame.Color("#8da65e")

    if growth_stage is PlantGrowthStage.SENESCENT:
        shadow = pygame.Color("#4e4632")
        dark_green = pygame.Color("#7d7046")
        light_green = pygame.Color("#b09a5b")

    pygame.draw.ellipse(
        canvas,
        shadow,
        (tile.centerx - 11, tile.bottom - 8, 22, 5),
    )

    blade_tips: tuple[tuple[int, int], ...]
    if growth_stage is PlantGrowthStage.EMERGING:
        blade_tips = (
            (tile.left + 11, tile.centery),
            (tile.centerx, tile.top + 12),
            (tile.right - 11, tile.centery + 1),
        )
    else:
        blade_tips = (
            (tile.left + 7, tile.top + 9),
            (tile.left + 11, tile.top + 5),
            (tile.centerx, tile.top + 8),
            (tile.right - 11, tile.top + 4),
            (tile.right - 7, tile.top + 10),
        )

    for index, tip in enumerate(blade_tips):
        color = light_green if index % 2 == 0 else dark_green
        pygame.draw.line(
            canvas,
            color,
            (tile.centerx, tile.bottom - 6),
            tip,
            2,
        )

    if growth_stage is PlantGrowthStage.FLOWERING:
        culm = pygame.Color("#a99a68")
        for x_offset, y_offset in ((-5, 5), (5, 7)):
            pygame.draw.line(
                canvas,
                culm,
                (tile.centerx + x_offset, tile.bottom - 7),
                (tile.centerx + x_offset, tile.top + y_offset),
                1,
            )
            pygame.draw.rect(
                canvas,
                culm,
                (tile.centerx + x_offset, tile.top + y_offset, 2, 3),
            )


def _draw_bellwort(
    canvas: pygame.Surface,
    tile: pygame.Rect,
    growth_stage: PlantGrowthStage,
) -> None:
    """Draw large-flowered bellwort using its supplied lifecycle stage."""

    shadow = pygame.Color("#3f4c32")
    stem = pygame.Color("#5f7d43")
    leaf = pygame.Color("#779650")
    flower = pygame.Color("#e7c75a")
    highlight = pygame.Color("#ffe58a")
    center = pygame.Color("#9b7138")

    if growth_stage is PlantGrowthStage.SENESCENT:
        shadow = pygame.Color("#4e4632")
        stem = pygame.Color("#806f43")
        leaf = pygame.Color("#aa9455")

    pygame.draw.ellipse(
        canvas,
        shadow,
        (tile.centerx - 9, tile.bottom - 7, 18, 4),
    )

    if growth_stage is PlantGrowthStage.EMERGING:
        pygame.draw.lines(
            canvas,
            stem,
            False,
            (
                (tile.centerx - 3, tile.bottom - 6),
                (tile.centerx - 2, tile.centery + 3),
                (tile.centerx + 2, tile.centery),
            ),
            2,
        )
        pygame.draw.polygon(
            canvas,
            leaf,
            (
                (tile.centerx - 1, tile.centery + 3),
                (tile.left + 9, tile.centery),
                (tile.centerx - 3, tile.centery + 7),
            ),
        )
        return

    pygame.draw.lines(
        canvas,
        stem,
        False,
        (
            (tile.centerx - 3, tile.bottom - 6),
            (tile.centerx - 2, tile.centery),
            (tile.centerx + 4, tile.top + 8),
        ),
        2,
    )

    pygame.draw.polygon(
        canvas,
        leaf,
        (
            (tile.centerx - 2, tile.centery + 2),
            (tile.left + 5, tile.centery - 2),
            (tile.centerx - 4, tile.centery + 6),
        ),
    )
    pygame.draw.polygon(
        canvas,
        leaf,
        (
            (tile.centerx + 1, tile.centery - 3),
            (tile.right - 5, tile.centery - 7),
            (tile.centerx + 3, tile.centery + 1),
        ),
    )

    if growth_stage is PlantGrowthStage.FRUITING:
        capsule = pygame.Color("#a18c52")
        pygame.draw.polygon(
            canvas,
            capsule,
            (
                (tile.centerx + 3, tile.top + 10),
                (tile.centerx + 8, tile.top + 13),
                (tile.centerx + 4, tile.top + 17),
                (tile.centerx, tile.top + 13),
            ),
        )
        pygame.draw.line(
            canvas,
            center,
            (tile.centerx + 4, tile.top + 11),
            (tile.centerx + 4, tile.top + 16),
            1,
        )
        return

    if growth_stage is not PlantGrowthStage.FLOWERING:
        return

    flower_center = (tile.centerx + 6, tile.top + 11)
    petals = (
        (flower_center[0] - 5, flower_center[1]),
        (flower_center[0] + 5, flower_center[1]),
        (flower_center[0], flower_center[1] - 5),
        (flower_center[0], flower_center[1] + 5),
    )

    for petal in petals:
        pygame.draw.circle(canvas, flower, petal, 3)

    pygame.draw.circle(canvas, highlight, flower_center, 3)
    pygame.draw.rect(
        canvas,
        center,
        (flower_center[0], flower_center[1], 2, 2),
    )


def _draw_preview_ant(
    canvas: pygame.Surface,
    tile: pygame.Rect,
) -> None:
    """Draw a temporary ant preview until ants enter the domain model."""

    body = pygame.Color("#30251f")
    highlight = pygame.Color("#5c4030")
    leg = pygame.Color("#241c19")

    center_x = tile.centerx
    center_y = tile.centery + 3

    legs = (
        ((center_x - 3, center_y), (center_x - 9, center_y - 5)),
        ((center_x - 2, center_y + 1), (center_x - 9, center_y + 5)),
        ((center_x, center_y), (center_x - 5, center_y + 8)),
        ((center_x + 3, center_y), (center_x + 9, center_y - 5)),
        ((center_x + 2, center_y + 1), (center_x + 9, center_y + 5)),
        ((center_x, center_y), (center_x + 5, center_y + 8)),
    )

    for start, end in legs:
        pygame.draw.line(canvas, leg, start, end, 1)

    pygame.draw.ellipse(
        canvas,
        body,
        (center_x - 5, center_y - 4, 8, 9),
    )
    pygame.draw.circle(canvas, highlight, (center_x + 3, center_y), 3)
    pygame.draw.circle(canvas, body, (center_x + 8, center_y - 1), 3)

    pygame.draw.line(
        canvas,
        leg,
        (center_x + 9, center_y - 3),
        (center_x + 12, center_y - 7),
        1,
    )
    pygame.draw.line(
        canvas,
        leg,
        (center_x + 9, center_y - 2),
        (center_x + 13, center_y + 1),
        1,
    )
