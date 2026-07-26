"""Pygame observation of an immutable world snapshot."""

import pygame

from terroir_simulator.domain import (
    Coordinate,
    Plant,
    ResourceType,
    TerrainType,
    WorldState,
)

_TILE_SIZE = 32
_DISPLAY_SCALE = 4

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
    display_size = (
        logical_size[0] * _DISPLAY_SCALE,
        logical_size[1] * _DISPLAY_SCALE,
    )

    try:
        canvas = pygame.Surface(logical_size)
        window = pygame.display.set_mode(display_size)
        pygame.display.set_caption("Terroir Simulator")
        clock = pygame.time.Clock()

        _draw_world(canvas, state)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    running = False

            enlarged = pygame.transform.scale(canvas, display_size)
            window.blit(enlarged, (0, 0))
            pygame.display.flip()
            clock.tick(30)
    finally:
        pygame.quit()


def _draw_world(canvas: pygame.Surface, state: WorldState) -> None:
    """Draw terrain and resources without changing world state."""

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
    """Draw a plant according to its species identity."""

    if plant.species.species_id == "flora.pennsylvania_sedge":
        _draw_sedge(canvas, tile)
    elif plant.species.species_id == "flora.large_flowered_bellwort":
        _draw_bellwort(canvas, tile)


def _draw_sedge(canvas: pygame.Surface, tile: pygame.Rect) -> None:
    """Draw a soft clump of Pennsylvania sedge."""

    shadow = pygame.Color("#3f4c32")
    dark_green = pygame.Color("#526b3d")
    light_green = pygame.Color("#8da65e")

    pygame.draw.ellipse(
        canvas,
        shadow,
        (tile.centerx - 11, tile.bottom - 8, 22, 5),
    )

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


def _draw_bellwort(canvas: pygame.Surface, tile: pygame.Rect) -> None:
    """Draw an arching large-flowered bellwort."""

    shadow = pygame.Color("#3f4c32")
    stem = pygame.Color("#5f7d43")
    leaf = pygame.Color("#779650")
    flower = pygame.Color("#e7c75a")
    highlight = pygame.Color("#ffe58a")
    center = pygame.Color("#9b7138")

    pygame.draw.ellipse(
        canvas,
        shadow,
        (tile.centerx - 9, tile.bottom - 7, 18, 4),
    )

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
