import pytest

from ant_colony.domain import (
    MoistureMap,
    SimulationTime,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
    WorldState,
)
from ant_colony.simulation import run_steps


def make_state(step: int = 0) -> WorldState:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.MUD),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(25, 75),
    )
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
    )

    return WorldState(
        world=world,
        time=SimulationTime(step=step),
    )


def test_run_steps_advances_the_requested_number_of_steps() -> None:
    initial_state = make_state(step=3)

    final_state = run_steps(initial_state, steps=5)

    assert final_state.time == SimulationTime(step=8)


def test_run_steps_preserves_the_terrain() -> None:
    initial_state = make_state()

    final_state = run_steps(initial_state, steps=5)

    assert final_state.world.terrain is initial_state.world.terrain


def test_run_steps_does_not_modify_the_initial_state() -> None:
    initial_state = make_state(step=3)

    run_steps(initial_state, steps=5)

    assert initial_state.time == SimulationTime(step=3)


def test_running_zero_steps_returns_the_original_state() -> None:
    initial_state = make_state(step=3)

    final_state = run_steps(initial_state, steps=0)

    assert final_state is initial_state


@pytest.mark.parametrize(
    "steps",
    [
        -1,
        1.5,
        "1",
        True,
        False,
        None,
    ],
)
def test_run_steps_rejects_invalid_step_counts(steps: object) -> None:
    with pytest.raises(
        ValueError,
        match="steps must be a non-negative integer",
    ):
        run_steps(
            make_state(),
            steps=steps,  # type: ignore[arg-type]
        )


def test_run_steps_rejects_invalid_state() -> None:
    with pytest.raises(TypeError, match="state must be WorldState"):
        run_steps(None, steps=1)  # type: ignore[arg-type]
