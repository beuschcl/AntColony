from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import SimulationTime


def test_simulation_time_begins_at_step_zero_by_default() -> None:
    time = SimulationTime()

    assert time.step == 0


def test_simulation_time_accepts_a_non_negative_step() -> None:
    time = SimulationTime(step=12)

    assert time.step == 12


@pytest.mark.parametrize(
    "step",
    [
        -1,
        1.5,
        "1",
        True,
        False,
        None,
    ],
)
def test_simulation_time_rejects_invalid_steps(step: object) -> None:
    with pytest.raises(
        ValueError,
        match="step must be a non-negative integer",
    ):
        SimulationTime(step=step)  # type: ignore[arg-type]


def test_simulation_time_is_immutable() -> None:
    time = SimulationTime(step=3)

    with pytest.raises(FrozenInstanceError):
        time.step = 4  # type: ignore[misc]


def test_advance_returns_the_next_simulation_step() -> None:
    current_time = SimulationTime(step=3)

    next_time = current_time.advance()

    assert next_time == SimulationTime(step=4)


def test_advance_does_not_modify_the_current_time() -> None:
    current_time = SimulationTime(step=3)

    next_time = current_time.advance()

    assert current_time.step == 3
    assert next_time is not current_time
