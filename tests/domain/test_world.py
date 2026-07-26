import pytest

from terroir_simulator.domain import (
    Coordinate,
    MoistureMap,
    ResourceDeposit,
    ResourceType,
    TerrainMap,
    TerrainType,
    World,
    WorldDimensions,
)


def make_world(
    width: int = 10,
    height: int = 6,
    resource_deposits: tuple[ResourceDeposit, ...] = (),
) -> World:
    dimensions = WorldDimensions(width=width, height=height)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL,) * (width * height),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(50,) * (width * height),
    )
    return World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=moisture,
        resource_deposits=resource_deposits,
    )


def test_world_preserves_its_dimensions_and_terrain() -> None:
    dimensions = WorldDimensions(width=2, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.WATER),
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

    assert world.dimensions is dimensions
    assert world.terrain is terrain
    assert world.moisture is moisture


def test_world_rejects_invalid_dimensions() -> None:
    dimensions = WorldDimensions(width=1, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL,),
    )
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(50,),
    )

    with pytest.raises(TypeError, match="dimensions must be WorldDimensions"):
        World(
            dimensions=(1, 1),  # type: ignore[arg-type]
            terrain=terrain,
            moisture=moisture,
        )


def test_world_rejects_invalid_terrain() -> None:
    dimensions = WorldDimensions(width=1, height=1)
    moisture = MoistureMap(
        dimensions=dimensions,
        values=(50,),
    )

    with pytest.raises(TypeError, match="terrain must be TerrainMap"):
        World(
            dimensions=dimensions,
            terrain=None,  # type: ignore[arg-type]
            moisture=moisture,
        )


def test_world_rejects_terrain_with_different_dimensions() -> None:
    terrain = TerrainMap(
        dimensions=WorldDimensions(width=2, height=1),
        tiles=(TerrainType.SOIL, TerrainType.ROCK),
    )

    with pytest.raises(
        ValueError,
        match="terrain dimensions must match world dimensions",
    ):
        World(
            dimensions=WorldDimensions(width=1, height=2),
            terrain=terrain,
            moisture=MoistureMap(
                dimensions=WorldDimensions(width=1, height=2),
                values=(50, 75),
            ),
        )


def test_world_rejects_invalid_moisture() -> None:
    dimensions = WorldDimensions(width=1, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL,),
    )

    with pytest.raises(TypeError, match="moisture must be MoistureMap"):
        World(
            dimensions=dimensions,
            terrain=terrain,
            moisture=None,  # type: ignore[arg-type]
        )


def test_world_rejects_moisture_with_different_dimensions() -> None:
    dimensions = WorldDimensions(width=1, height=2)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(TerrainType.SOIL, TerrainType.MUD),
    )
    moisture = MoistureMap(
        dimensions=WorldDimensions(width=2, height=1),
        values=(25, 75),
    )

    with pytest.raises(
        ValueError,
        match="moisture dimensions must match world dimensions",
    ):
        World(
            dimensions=dimensions,
            terrain=terrain,
            moisture=moisture,
        )


@pytest.mark.parametrize(
    ("coordinate", "expected"),
    [
        (Coordinate(0, 0), True),
        (Coordinate(9, 5), True),
        (Coordinate(-1, 0), False),
        (Coordinate(10, 5), False),
    ],
)
def test_world_determines_whether_coordinate_is_in_bounds(
    coordinate: Coordinate,
    expected: bool,
) -> None:
    world = make_world()

    assert world.contains(coordinate) is expected


def test_world_exposes_terrain_by_coordinate() -> None:
    dimensions = WorldDimensions(width=3, height=1)
    terrain = TerrainMap(
        dimensions=dimensions,
        tiles=(
            TerrainType.SOIL,
            TerrainType.ROCK,
            TerrainType.WATER,
        ),
    )
    world = World(
        dimensions=dimensions,
        terrain=terrain,
        moisture=MoistureMap(
            dimensions=dimensions,
            values=(10, 20, 30),
        ),
    )

    assert world.terrain_at(Coordinate(0, 0)) is TerrainType.SOIL
    assert world.terrain_at(Coordinate(1, 0)) is TerrainType.ROCK
    assert world.terrain_at(Coordinate(2, 0)) is TerrainType.WATER


def test_world_exposes_moisture_by_coordinate() -> None:
    dimensions = WorldDimensions(width=3, height=1)
    world = World(
        dimensions=dimensions,
        terrain=TerrainMap(
            dimensions=dimensions,
            tiles=(
                TerrainType.SOIL,
                TerrainType.ROCK,
                TerrainType.WATER,
            ),
        ),
        moisture=MoistureMap(
            dimensions=dimensions,
            values=(10, 20, 30),
        ),
    )

    assert world.moisture_at(Coordinate(0, 0)) == 10
    assert world.moisture_at(Coordinate(1, 0)) == 20
    assert world.moisture_at(Coordinate(2, 0)) == 30


def test_world_iterates_coordinates_in_row_major_order() -> None:
    world = make_world(width=3, height=2)

    assert list(world.iter_coordinates()) == [
        Coordinate(0, 0),
        Coordinate(1, 0),
        Coordinate(2, 0),
        Coordinate(0, 1),
        Coordinate(1, 1),
        Coordinate(2, 1),
    ]


def test_world_exposes_resource_deposits_by_coordinate() -> None:
    world = make_world(
        width=3,
        height=1,
        resource_deposits=(
            ResourceDeposit(
                coordinate=Coordinate(0, 0),
                resource_type=ResourceType.FOOD,
                quantity=25,
            ),
        ),
    )

    deposits = world.resource_deposits_at(Coordinate(0, 0))

    assert deposits == (
        ResourceDeposit(
            coordinate=Coordinate(0, 0),
            resource_type=ResourceType.FOOD,
            quantity=25,
        ),
    )
    assert isinstance(deposits, tuple)


def test_world_returns_resource_quantity_by_coordinate_and_type() -> None:
    world = make_world(
        width=2,
        height=1,
        resource_deposits=(
            ResourceDeposit(
                coordinate=Coordinate(1, 0),
                resource_type=ResourceType.FOOD,
                quantity=10,
            ),
        ),
    )

    assert world.resource_quantity_at(Coordinate(1, 0), ResourceType.FOOD) == 10


def test_world_returns_zero_when_resource_is_absent() -> None:
    world = make_world(
        width=2,
        height=1,
        resource_deposits=(
            ResourceDeposit(
                coordinate=Coordinate(1, 0),
                resource_type=ResourceType.FOOD,
                quantity=10,
            ),
        ),
    )

    assert world.resource_quantity_at(Coordinate(0, 0), ResourceType.FOOD) == 0


def test_world_rejects_non_resource_deposit_entry() -> None:
    with pytest.raises(
        TypeError, match="every resource deposit must be ResourceDeposit"
    ):
        make_world(
            width=1,
            height=1,
            resource_deposits=("not-a-deposit",),  # type: ignore[arg-type]
        )


def test_world_rejects_out_of_bounds_resource_deposit() -> None:
    with pytest.raises(
        ValueError,
        match="resource deposit coordinate must be within world bounds",
    ):
        make_world(
            width=1,
            height=1,
            resource_deposits=(
                ResourceDeposit(
                    coordinate=Coordinate(1, 0),
                    resource_type=ResourceType.FOOD,
                    quantity=1,
                ),
            ),
        )


def test_world_rejects_duplicate_resource_deposit_type_at_same_coordinate() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate resource deposit for coordinate and resource type",
    ):
        make_world(
            width=1,
            height=1,
            resource_deposits=(
                ResourceDeposit(
                    coordinate=Coordinate(0, 0),
                    resource_type=ResourceType.FOOD,
                    quantity=1,
                ),
                ResourceDeposit(
                    coordinate=Coordinate(0, 0),
                    resource_type=ResourceType.FOOD,
                    quantity=2,
                ),
            ),
        )
