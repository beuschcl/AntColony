from dataclasses import FrozenInstanceError

import pytest

from ant_colony.domain import (
    Coordinate,
    TerrainMap,
    TerrainType,
    WorldDimensions,
)


def test_terrain_map_preserves_varied_terrain() -> None:
    terrain = TerrainMap(
        dimensions=WorldDimensions(width=3, height=2),
        tiles=(
            TerrainType.SOIL,
            TerrainType.ROCK,
            TerrainType.WATER,
            TerrainType.WATER,
            TerrainType.SOIL,
            TerrainType.ROCK,
        ),
    )

    assert terrain.terrain_at(Coordinate(0, 0)) is TerrainType.SOIL
    assert terrain.terrain_at(Coordinate(1, 0)) is TerrainType.ROCK
    assert terrain.terrain_at(Coordinate(2, 0)) is TerrainType.WATER
    assert terrain.terrain_at(Coordinate(0, 1)) is TerrainType.WATER
    assert terrain.terrain_at(Coordinate(1, 1)) is TerrainType.SOIL
    assert terrain.terrain_at(Coordinate(2, 1)) is TerrainType.ROCK


def test_terrain_map_is_immutable() -> None:
    terrain = TerrainMap(
        dimensions=WorldDimensions(width=1, height=1),
        tiles=(TerrainType.SOIL,),
    )

    with pytest.raises(FrozenInstanceError):
        terrain.tiles = (TerrainType.WATER,)  # type: ignore[misc]


def test_terrain_map_requires_a_tuple() -> None:
    with pytest.raises(TypeError, match="tiles must be a tuple"):
        TerrainMap(
            dimensions=WorldDimensions(width=1, height=1),
            tiles=[TerrainType.SOIL],  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "tiles",
    [
        (),
        (TerrainType.SOIL,),
        (
            TerrainType.SOIL,
            TerrainType.ROCK,
            TerrainType.WATER,
        ),
    ],
)
def test_terrain_map_requires_one_tile_per_coordinate(
    tiles: tuple[TerrainType, ...],
) -> None:
    with pytest.raises(ValueError, match="terrain requires exactly 2 tiles"):
        TerrainMap(
            dimensions=WorldDimensions(width=2, height=1),
            tiles=tiles,
        )


def test_terrain_map_rejects_unknown_terrain() -> None:
    with pytest.raises(TypeError, match="every tile must be TerrainType"):
        TerrainMap(
            dimensions=WorldDimensions(width=1, height=1),
            tiles=("sand",),  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "coordinate",
    [
        Coordinate(-1, 0),
        Coordinate(0, -1),
        Coordinate(2, 0),
        Coordinate(0, 1),
    ],
)
def test_terrain_map_rejects_out_of_bounds_coordinates(
    coordinate: Coordinate,
) -> None:
    terrain = TerrainMap(
        dimensions=WorldDimensions(width=2, height=1),
        tiles=(TerrainType.SOIL, TerrainType.ROCK),
    )

    with pytest.raises(
        ValueError,
        match="coordinate is outside the terrain map",
    ):
        terrain.terrain_at(coordinate)