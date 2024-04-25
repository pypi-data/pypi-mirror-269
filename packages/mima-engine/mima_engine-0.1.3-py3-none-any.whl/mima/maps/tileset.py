from typing import List

from .tile import Tile


class Tileset:
    def __init__(self):
        self.name: str = "Unnamed Tileset"
        self.sprite_name: str = ""
        # self.filename: str = ""
        self.sprite_width: int = 0
        self.sprite_height: int = 0
        self.tile_width: int = 0
        self.tile_height: int = 0
        self.tile_count: int = 0
        self.columns: int = 0

        self.tiles: List[Tile] = []
        self.animated_tiles: List[Tile] = []

    def update(self, elapsed_time: float) -> bool:
        for tile in self.animated_tiles:
            tile.update(elapsed_time)

        return True

    def get_tile(self, tile_id: int) -> Tile:
        for tile in self.tiles:
            if tile.basic_tile_id == tile_id:
                return tile

        return self.tiles[0]
