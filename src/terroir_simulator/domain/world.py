"""The simulated world's spatial foundation."""

from dataclasses import dataclass, field

from terroir_simulator.domain.moisture import MoistureMap
from terroir_simulator.domain.resource import ResourceDeposit, ResourceType
from terroir_simulator.domain.spatial import Coordinate, WorldDimensions
from terroir_simulator.domain.terrain import TerrainMap, TerrainType


@dataclass(frozen=True, slots=True)
class World:
    """An immutable collection of dimension-matched world layers."""

    dimensions: WorldDimensions
    terrain: TerrainMap
    moisture: MoistureMap
    resource_deposits: tuple[ResourceDeposit, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.dimensions, WorldDimensions):
            raise TypeError("dimensions must be WorldDimensions")

        if not isinstance(self.terrain, TerrainMap):
            raise TypeError("terrain must be TerrainMap")

        if not isinstance(self.moisture, MoistureMap):
            raise TypeError("moisture must be MoistureMap")

        if self.terrain.dimensions != self.dimensions:
            raise ValueError("terrain dimensions must match world dimensions")

        if self.moisture.dimensions != self.dimensions:
            raise ValueError("moisture dimensions must match world dimensions")

        if not isinstance(self.resource_deposits, tuple):
            raise TypeError("resource_deposits must be a tuple")

        seen_deposit_locations: set[tuple[Coordinate, ResourceType]] = set()

        for deposit in self.resource_deposits:
            if not isinstance(deposit, ResourceDeposit):
                raise TypeError("every resource deposit must be ResourceDeposit")

            if not self.contains(deposit.coordinate):
                raise ValueError(
                    "resource deposit coordinate must be within world bounds"
                )

            deposit_location = (deposit.coordinate, deposit.resource_type)
            if deposit_location in seen_deposit_locations:
                raise ValueError(
                    "duplicate resource deposit for coordinate and resource type"
                )
            seen_deposit_locations.add(deposit_location)

    def terrain_at(self, coordinate: Coordinate) -> TerrainType:
        """Return the terrain at a world coordinate."""

        return self.terrain.terrain_at(coordinate)

    def moisture_at(self, coordinate: Coordinate) -> int:
        """Return the moisture percentage at a world coordinate."""

        return self.moisture.moisture_at(coordinate)

    def resource_deposits_at(
        self,
        coordinate: Coordinate,
    ) -> tuple[ResourceDeposit, ...]:
        """Return immutable resource deposits located at one coordinate."""

        if not isinstance(coordinate, Coordinate):
            raise TypeError("coordinate must be Coordinate")

        if not self.contains(coordinate):
            raise ValueError("coordinate must be within world bounds")

        return tuple(
            deposit
            for deposit in self.resource_deposits
            if deposit.coordinate == coordinate
        )

    def resource_quantity_at(
        self,
        coordinate: Coordinate,
        resource_type: ResourceType,
    ) -> int:
        """Return the resource quantity at a coordinate for one resource type."""

        if not isinstance(resource_type, ResourceType):
            raise TypeError("resource_type must be ResourceType")

        for deposit in self.resource_deposits_at(coordinate):
            if deposit.resource_type is resource_type:
                return deposit.quantity

        return 0

    def contains(self, coordinate: Coordinate) -> bool:
        """Return whether a coordinate is within the world bounds."""

        return self.dimensions.contains(coordinate)

    def iter_coordinates(self):
        """Return coordinates in deterministic row-major order."""

        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                yield Coordinate(x=x, y=y)
