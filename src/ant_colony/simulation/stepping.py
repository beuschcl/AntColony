"""Orchestration for advancing the simulated world."""

from ant_colony.domain import WorldState


def advance_world(state: WorldState) -> WorldState:
    """Return the world state produced by one completed simulation step."""

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    return WorldState(
        world=state.world,
        time=state.time.advance(),
    )