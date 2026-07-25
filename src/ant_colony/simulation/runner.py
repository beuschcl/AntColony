"""Operations for running multiple simulation steps."""

from ant_colony.domain import WorldState
from ant_colony.simulation.stepping import advance_world


def run_steps(state: WorldState, steps: int) -> WorldState:
    """Return the world state produced after a requested number of steps."""

    if not isinstance(state, WorldState):
        raise TypeError("state must be WorldState")

    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer")

    current_state = state

    for _ in range(steps):
        current_state = advance_world(current_state)

    return current_state