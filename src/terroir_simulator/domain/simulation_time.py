"""Deterministic time values for the simulation."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationTime:
    """An immutable, non-negative simulation step number."""

    step: int = 0

    def __post_init__(self) -> None:
        if (
            isinstance(self.step, bool)
            or not isinstance(self.step, int)
            or self.step < 0
        ):
            raise ValueError("step must be a non-negative integer")

    def advance(self) -> "SimulationTime":
        """Return the time value for the next completed simulation step."""

        return SimulationTime(step=self.step + 1)
