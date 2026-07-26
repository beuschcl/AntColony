"""Observable state of the simulated world."""

from dataclasses import dataclass, field

from terroir_simulator.domain.simulation_time import SimulationTime
from terroir_simulator.domain.world import World


@dataclass(frozen=True, slots=True)
class WorldState:
    """An immutable snapshot of the world at a simulation step."""

    world: World
    time: SimulationTime = field(default_factory=SimulationTime)

    def __post_init__(self) -> None:
        if not isinstance(self.world, World):
            raise TypeError("world must be World")

        if not isinstance(self.time, SimulationTime):
            raise TypeError("time must be SimulationTime")
