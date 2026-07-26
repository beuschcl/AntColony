"""The simulated world's spatial foundation."""

from collections.abc import Iterator
from dataclasses import dataclass, field

from terroir_simulator.domain.moisture import MoistureMap
from terroir_simulator.domain.plant import Plant, PlantId
from terroir_simulator.domain.resource import ResourceDeposit, ResourceType
from terroir_simulator.domain.spatial import Coordinate, WorldDimensions
from terroir_simulator.domain.terrain import TerrainMap, TerrainType


@dataclass(frozen=True, slots=True)
class World:
    """An immutable snapshot of dimension-matched world layers and plant state.

    Plant state is stored as frozen sets so that every ``World`` value is a
    true immutable snapshot.  Mutating plant registration or placement returns
    a new ``World`` rather than modifying the existing one.
    """

    dimensions: WorldDimensions
    terrain: TerrainMap
    moisture: MoistureMap
    resource_deposits: tuple[ResourceDeposit, ...] = field(default_factory=tuple)

    # Immutable plant state.  Both fields participate in equality so that two
    # World values with different plant states are never considered equal.
    # frozenset gives order-independent set equality, which is the correct
    # semantic: the same set of plants is the same state regardless of
    # registration order.
    _plant_registry: frozenset[tuple[PlantId, Plant]] = field(
        default=frozenset(),
        repr=False,
    )
    _plant_locations: frozenset[tuple[PlantId, Coordinate]] = field(
        default=frozenset(),
        repr=False,
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

        if not isinstance(self._plant_registry, frozenset):
            raise TypeError("_plant_registry must be frozenset")

        seen_registry_ids: set[PlantId] = set()

        for registry_entry in self._plant_registry:
            if (
                not isinstance(registry_entry, tuple)
                or len(registry_entry) != 2
                or not isinstance(registry_entry[0], PlantId)
                or not isinstance(registry_entry[1], Plant)
            ):
                raise TypeError(
                    "each _plant_registry entry must be a (PlantId, Plant) tuple"
                )
            registry_key, registry_plant = registry_entry
            if registry_key != registry_plant.plant_id:
                raise ValueError("registry key must match plant.plant_id")
            if registry_key in seen_registry_ids:
                raise ValueError("duplicate PlantId in _plant_registry")
            seen_registry_ids.add(registry_key)

        if not isinstance(self._plant_locations, frozenset):
            raise TypeError("_plant_locations must be frozenset")

        seen_location_ids: set[PlantId] = set()

        for location_entry in self._plant_locations:
            if (
                not isinstance(location_entry, tuple)
                or len(location_entry) != 2
                or not isinstance(location_entry[0], PlantId)
                or not isinstance(location_entry[1], Coordinate)
            ):
                raise TypeError(
                    "each _plant_locations entry must be a (PlantId, Coordinate) tuple"
                )
            location_id, location_coord = location_entry
            if location_id not in seen_registry_ids:
                raise ValueError(
                    "location PlantId must be registered in _plant_registry"
                )
            if location_id in seen_location_ids:
                raise ValueError("duplicate PlantId in _plant_locations")
            seen_location_ids.add(location_id)
            if not self.contains(location_coord):
                raise ValueError(
                    "plant location coordinate must be within world bounds"
                )

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
    # Internal helpers
    # ------------------------------------------------------------------

    def _replace_moisture(self, moisture: MoistureMap) -> "World":
        """Return a new World identical to this one except for the moisture map.

        Intended for use by simulation stepping code that updates moisture
        while carrying all plant state forward unchanged.
        """

        return World(
            dimensions=self.dimensions,
            terrain=self.terrain,
            moisture=moisture,
            resource_deposits=self.resource_deposits,
            _plant_registry=self._plant_registry,
            _plant_locations=self._plant_locations,
        )

    # ------------------------------------------------------------------
    # Plant registry — copy-on-write operations
    # ------------------------------------------------------------------

    def register_plant(self, plant: Plant, coordinate: Coordinate) -> "World":
        """Return a new World with the plant registered at the coordinate.

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

        registry_ids = {pid for pid, _ in self._plant_registry}
        if plant.plant_id in registry_ids:
            raise ValueError("plant is already registered")

        return World(
            dimensions=self.dimensions,
            terrain=self.terrain,
            moisture=self.moisture,
            resource_deposits=self.resource_deposits,
            _plant_registry=self._plant_registry | {(plant.plant_id, plant)},
            _plant_locations=self._plant_locations | {(plant.plant_id, coordinate)},
        )

    def plant(self, plant_id: PlantId) -> Plant:
        """Return the registered plant for plant_id.

        Raises TypeError for a wrong argument type.
        Raises KeyError if plant_id is not registered.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        for pid, p in self._plant_registry:
            if pid == plant_id:
                return p

        raise KeyError(plant_id)

    def location_of(self, plant_id: PlantId) -> Coordinate:
        """Return the current coordinate of an active plant.

        Raises TypeError for a wrong argument type.
        Raises KeyError if the plant is not currently placed in the world.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        for pid, coord in self._plant_locations:
            if pid == plant_id:
                return coord

        raise KeyError(plant_id)

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

        registry: dict[PlantId, Plant] = dict(self._plant_registry)
        placed_ids = {
            pid for pid, coord in self._plant_locations if coord == coordinate
        }
        return tuple(
            sorted(
                (registry[pid] for pid in placed_ids),
                key=lambda p: p.plant_id.value,
            )
        )

    def active_plants(self) -> tuple[Plant, ...]:
        """Return all currently placed plants in deterministic order."""

        registry: dict[PlantId, Plant] = dict(self._plant_registry)
        active_ids = {pid for pid, _ in self._plant_locations}
        return tuple(
            sorted(
                (registry[pid] for pid in active_ids),
                key=lambda p: p.plant_id.value,
            )
        )

    def all_plants(self) -> tuple[Plant, ...]:
        """Return all registered plants, including those no longer placed."""

        return tuple(
            sorted(
                (p for _, p in self._plant_registry),
                key=lambda p: p.plant_id.value,
            )
        )

    def remove_plant_from_world(self, plant_id: PlantId) -> "World":
        """Return a new World with the plant's placement removed.

        The plant remains in the permanent registry of the returned world and
        can still be retrieved via plant() and all_plants().

        Raises TypeError for a wrong argument type.
        Raises KeyError if plant_id is not registered.
        Raises ValueError if the plant is not currently placed in the world.
        """

        if not isinstance(plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        registry_ids = {pid for pid, _ in self._plant_registry}
        if plant_id not in registry_ids:
            raise KeyError(plant_id)

        location_ids = {pid for pid, _ in self._plant_locations}
        if plant_id not in location_ids:
            raise ValueError("plant is not currently placed in the world")

        new_locations = frozenset(
            (pid, coord) for pid, coord in self._plant_locations if pid != plant_id
        )

        return World(
            dimensions=self.dimensions,
            terrain=self.terrain,
            moisture=self.moisture,
            resource_deposits=self.resource_deposits,
            _plant_registry=self._plant_registry,
            _plant_locations=new_locations,
        )
