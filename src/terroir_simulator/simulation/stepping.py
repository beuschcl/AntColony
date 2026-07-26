"""Orchestration for advancing the simulated world."""

from terroir_simulator.domain import WorldState
from terroir_simulator.simulation.evaporation import evaporate_moisture


def advance_world(state: WorldState, evaporation_rate: int = 0) -> WorldState:
    """Return the world state produced by one completed simulation step.

    evaporation_rate is the amount of moisture lost per non-water cell per
    step.  It must be a non-negative integer; booleans are rejected.  A rate
    of 0 leaves non-water moisture unchanged.
    """

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    if (
        isinstance(evaporation_rate, bool)
        or not isinstance(evaporation_rate, int)
        or evaporation_rate < 0
    ):
        raise ValueError("evaporation_rate must be a non-negative integer")

    new_moisture = evaporate_moisture(state.world, evaporation_rate)
    new_world = state.world._replace_moisture(new_moisture)

    return WorldState(
        world=new_world,
        time=state.time.advance(),
    )
