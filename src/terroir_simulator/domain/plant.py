"""Living plant domain model for the Terroir Simulator."""

import uuid
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class PlantId:
    """A stable UUID-backed identifier for an individual plant organism."""

    value: uuid.UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, uuid.UUID):
            raise TypeError("value must be uuid.UUID")

    @classmethod
    def generate(cls) -> "PlantId":
        """Generate a new random PlantId."""
        return cls(value=uuid.uuid4())


@dataclass(frozen=True, slots=True)
class PlantSpecies:
    """Immutable description of a plant species."""

    species_id: str
    common_name: str
    scientific_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.species_id, str):
            raise TypeError("species_id must be str")

        if not isinstance(self.common_name, str):
            raise TypeError("common_name must be str")

        if not isinstance(self.scientific_name, str):
            raise TypeError("scientific_name must be str")


class PlantGrowthStage(Enum):
    """The shared, species-neutral lifecycle stage of a plant."""

    DORMANT = "dormant"
    EMERGING = "emerging"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUITING = "fruiting"
    SENESCENT = "senescent"
    DEAD = "dead"


@dataclass(frozen=True, slots=True)
class Plant:
    """An individual living plant organism."""

    plant_id: PlantId
    species: PlantSpecies
    growth_stage: PlantGrowthStage

    def __post_init__(self) -> None:
        if not isinstance(self.plant_id, PlantId):
            raise TypeError("plant_id must be PlantId")

        if not isinstance(self.species, PlantSpecies):
            raise TypeError("species must be PlantSpecies")

        if not isinstance(self.growth_stage, PlantGrowthStage):
            raise TypeError("growth_stage must be PlantGrowthStage")
