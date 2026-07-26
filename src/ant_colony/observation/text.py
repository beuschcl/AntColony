"""Plain-text observation of the simulated world."""

from ant_colony.domain import Coordinate, ResourceType, TerrainType, WorldState

_TERRAIN_SYMBOLS: dict[TerrainType, str] = {
    TerrainType.SOIL: "S",
    TerrainType.MUD: "M",
    TerrainType.ROCK: "R",
    TerrainType.WATER: "W",
}


def render_world(state: WorldState) -> str:
    """Return a deterministic textual snapshot of a world state."""

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    lines = [f"step={state.time.step}", "terrain:"]

    for y in range(state.world.dimensions.height):
        row = "".join(
            _TERRAIN_SYMBOLS[state.world.terrain_at(Coordinate(x=x, y=y))]
            for x in range(state.world.dimensions.width)
        )
        lines.append(row)

    lines.append("moisture:")

    for y in range(state.world.dimensions.height):
        row = " ".join(
            f"{state.world.moisture_at(Coordinate(x=x, y=y)):03d}"
            for x in range(state.world.dimensions.width)
        )
        lines.append(row)

    lines.append("food:")

    for y in range(state.world.dimensions.height):
        row = " ".join(
            "{:03d}".format(
                state.world.resource_quantity_at(
                    Coordinate(x=x, y=y), ResourceType.FOOD
                )
            )
            for x in range(state.world.dimensions.width)
        )
        lines.append(row)

    return "\n".join(lines)
