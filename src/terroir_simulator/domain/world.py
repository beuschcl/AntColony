"""The simulated world's spatial foundation."""

from collections.abc import Iterator
from dataclasses import dataclass, field

from terroir_simulator.domain.moisture import MoistureMap
from terroir_simulator.domain.plant import Plant, PlantId
from terroir_simulator.domain.resource import ResourceDeposit, ResourceType
from terroir_simulator.domain.spatial import Coordinate, WorldDimensions
from terroir_simulator.domain.terrain import TerrainMap, TerrainType


@dataclass(slots=True)
class World:
    """A mutable collection of dimension-matched world layers with a plant registry."""

    dimensions: WorldDimensions
    terrain: TerrainMap
    moisture: MoistureMap
    resource_deposits: tuple[ResourceDeposit, ...] = field(default_factory=tuple)

    # Plant registries — maintained internally; never expose raw references.
    _plant_registry: dict[PlantId, Plant] = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=dict,
    )
    _plant_locations: dict[PlantId, Coordinate] = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=dict,
    )
    _coordinate_index: dict[Coordinate, set[PlantId]] = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=dict,
    )

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

    def iter_coordinates(self) -> Iterator[Coordinate]:
        """Return coordinates in deterministic row-major order."""

        for y in range(self.dimensions.height):
            for x in range(self.dimensions.width):
                yield Coordinate(x=x, y=y)

    # ------------------------------------------------------------------
    # Plant registry
    # ------------------------------------------------------------------

    def register_plant(self, plant: Plant, coordinate: Coordinate) -> None:
        """Register a plant at a coordinate and add it to all indexes.

        Raises TypeError for wrong argument types.
        Raises ValueError if the coordinate is outside the world bounds or the
        plant's PlantId is already registered.
        """

        if not isinstance(plant, Plant):
            raise TypeError("plant must be Plant")

        if not isinstance(coordinate, Coordinate):
            raise TypeError("coordinate must be Coordinate")

        if not self.contains(coordinate):
            raise ValueError("coordinate must be within world bounds")

        if plant.plant_id in self._plant_registry:
            raise ValueError("plant is already registered")

        self._plant_registry[plant.plant_id] = plant
        self._plant_locations[plant.plant_id] = coordinate
        self._coordinate_index.setdefault(coordinate, set()).add(plant.plant_id)

    def plant(self, plant_id: PlantId) -> Plant:
        """Return the registered plant for plant_id.

        Raises TypeError for a wrong argument type.
        Raises KeyError if plant_id is not registered.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        return self._plant_registry[plant_id]

    def location_of(self, plant_id: PlantId) -> Coordinate:
        """Return the current coordinate of an active plant.

        Raises TypeError for a wrong argument type.
        Raises KeyError if the plant is not currently placed in the world.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        return self._plant_locations[plant_id]

    def plants_at(self, coordinate: Coordinate) -> tuple[Plant, ...]:
        """Return all currently placed plants at a coordinate.

        Plants are returned in a deterministic order sorted by PlantId value.
        Raises TypeError for a wrong argument type.
        Raises ValueError if the coordinate is outside the world bounds.
        """

        if not isinstance(coordinate, Coordinate):
            raise TypeError("coordinate must be Coordinate")

        if not self.contains(coordinate):
            raise ValueError("coordinate must be within world bounds")

        plant_ids = self._coordinate_index.get(coordinate, set())
        return tuple(
            sorted(
                (self._plant_registry[pid] for pid in plant_ids),
                key=lambda p: p.plant_id.value,
            )
        )

    def active_plants(self) -> tuple[Plant, ...]:
        """Return all currently placed plants in deterministic order."""

        return tuple(
            sorted(
                (self._plant_registry[pid] for pid in self._plant_locations),
                key=lambda p: p.plant_id.value,
            )
        )

    def all_plants(self) -> tuple[Plant, ...]:
        """Return all registered plants, including those no longer placed."""

        return tuple(
            sorted(
                self._plant_registry.values(),
                key=lambda p: p.plant_id.value,
            )
        )

    def remove_plant_from_world(self, plant_id: PlantId) -> None:
        """Remove a plant's current placement without deleting its record.

        The plant remains in the permanent registry and can still be retrieved
        via plant() and all_plants().

        Raises TypeError for a wrong argument type.
        Raises KeyError if plant_id is not registered.
        Raises ValueError if the plant is not currently placed in the world.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        if plant_id not in self._plant_registry:
            raise KeyError(plant_id)

        if plant_id not in self._plant_locations:
            raise ValueError("plant is not currently placed in the world")

        coordinate = self._plant_locations.pop(plant_id)
        self._coordinate_index[coordinate].discard(plant_id)
        if not self._coordinate_index[coordinate]:
            del self._coordinate_index[coordinate]
