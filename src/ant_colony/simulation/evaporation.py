"""Moisture evaporation computation for the simulated world."""

from ant_colony.domain import MoistureMap, TerrainType, World


def evaporate_moisture(world: World, evaporation_rate: int) -> MoistureMap:
    """Return a new moisture map with one evaporation step applied.

    Every non-water coordinate loses exactly evaporation_rate moisture,
    clamped to a minimum of 0.  Every WATER coordinate retains moisture 100
    regardless of the rate.  The entire result is calculated from the same
    starting state so coordinate processing order cannot affect the outcome.
    """

    new_values = []

    for coordinate in world.iter_coordinates():
        if world.terrain_at(coordinate) is TerrainType.WATER:
            new_values.append(100)
        else:
            current = world.moisture_at(coordinate)
            new_values.append(max(0, current - evaporation_rate))

    return MoistureMap(dimensions=world.dimensions, values=tuple(new_values))
