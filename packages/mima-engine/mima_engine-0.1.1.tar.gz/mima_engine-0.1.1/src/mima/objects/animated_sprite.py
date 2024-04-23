import logging
import math
from typing import Any, Dict, Optional

from ..types.direction import Direction
from ..types.graphic_state import GraphicState
from ..util.constants import TILE_HEIGHT, TILE_WIDTH

LOG = logging.getLogger(__name__)


class AnimatedSprite:
    engine = None
    sprite_sets = {}

    def __init__(
        self,
        tileset_name: str,
        image_name: str,
        sprite_name: Optional[str] = None,
        graphic_state: GraphicState = GraphicState.STANDING,
        facing_direction: Direction = Direction.SOUTH,
    ):
        self._sprite_name = (
            tileset_name if sprite_name is None else sprite_name
        )

        self._tileset_name = tileset_name
        self.name = image_name
        # TODO: Handle ""
        if tileset_name and image_name and self._sprite_name:
            LOG.info(
                {
                    "operation": "load sprite",
                    "tileset": tileset_name,
                    "image": image_name,
                    "sprite": self._sprite_name,
                },
            )
            tileset = self.engine.assets.get_tileset(tileset_name)

            self.width = tileset.tile_width
            self.height = tileset.tile_height

            self._sprites: Dict[
                GraphicState, Dict[Direction, Dict[str, Any]]
            ] = self._load_sprites_from_tileset(tileset, self._sprite_name)

            self._last_direction: Direction = facing_direction
            self._last_graphic_state: GraphicState = graphic_state
            data = self._get_data(
                self._last_graphic_state, self._last_direction
            )

            self._frame_index: int = 0
            self._timer: float = data["duration"][0]
        else:
            LOG.debug(
                f"Sprite information uncomplete. Tileset={tileset_name}, Image"
                f"={image_name}, Sprite={self._sprite_name}. Will continue without "
                "sprite."
            )
            self.name = self._tileset_name = self._sprite_name = ""

    def update(
        self,
        elapsed_time: float,
        direction: Direction = Direction.SOUTH,
        graphic_state: GraphicState = GraphicState.STANDING,
    ):
        if not self.name:
            return

        data = self._get_data(graphic_state, direction)
        # try:
        #     self._timer_reset = data["duration"][self._frame_index]
        # except KeyError as err:
        #     LOG.exception(
        #         f"Data of {self._tileset_name, self.name} is "
        #         f"malformed: {data}"
        #     )

        if (
            direction == self._last_direction
            and graphic_state == self._last_graphic_state
        ):
            # No changes, normal case
            self._timer -= elapsed_time
            if self._timer <= 0.0:
                self._frame_index = (self._frame_index + 1) % len(
                    data["duration"]
                )
                self._timer += data["duration"][self._frame_index]

        else:
            self._frame_index = 0
            # Something changed
            # if graphic_state != self._last_graphic_state:
            # State changed

            self._timer = data["duration"][0]

        self._last_direction = direction
        self._last_graphic_state = graphic_state

    def draw_self(self, px: float, py: float, absolute_position: bool = False):
        if self.name == "":
            return

        data = self._get_data(self._last_graphic_state, self._last_direction)
        if not absolute_position:
            px *= TILE_WIDTH
            py *= TILE_HEIGHT
        px, py = math.floor(px), math.floor(py)
        try:
            self.engine.backend.draw_partial_sprite(
                px,
                py,
                self.name,
                data["ox"][self._frame_index] * self.width,
                data["oy"][self._frame_index] * self.height,
                self.width,
                self.height,
            )
        except KeyError as err:
            LOG.exception(
                f"Data of {self._tileset_name, self.name} is malformed: {data}"
            )

    def _load_sprites_from_tileset(self, tileset, sprite_name):
        if sprite_name in AnimatedSprite.sprite_sets:
            # Caching
            return AnimatedSprite.sprite_sets[sprite_name]

        sprites = {}

        for tile in tileset.tiles:
            if tile.sprite_name != sprite_name:
                continue

            if tile.animated:
                data = {"duration": [], "ox": [], "oy": []}
                for frame in tile._frames:
                    data["duration"].append(frame.duration)
                    data["ox"].append(frame.frame_id % tileset.columns)
                    data["oy"].append(frame.frame_id // tileset.columns)
            else:
                data = {
                    "duration": [1000],
                    "ox": [tile.tile_id % tileset.columns],
                    "oy": [tile.tile_id // tileset.columns],
                }

            sprites.setdefault(tile.graphic_state, {})
            sprites[tile.graphic_state][tile.facing_direction] = data
            LOG.debug(
                {
                    "operation": "add frames",
                    "image": self.name,
                    "sprite": sprite_name,
                    "graphic_state": tile.graphic_state.name,
                    "direction": tile.facing_direction.name,
                    "frame_data": data,
                }
            )

        AnimatedSprite.sprite_sets[sprite_name] = sprites
        return sprites
        # for tile in tileset.tiles
        # Check non-animated tiles if necessary

    def reset(self):
        self._frame_index = 0
        self._timer = 0.0

    def _get_data(self, graphic_state, direction):
        if graphic_state == GraphicState.DEFEATED:
            graphic_state = graphic_state.DEAD

        data = self._sprites.get(
            graphic_state, self._sprites.get(GraphicState.STANDING, {})
        )
        data = data.get(
            direction,
            data.get(Direction.SOUTH, {}),
        )
        if not data:
            try:
                LOG.debug(
                    f"Animation of sprite {self._tileset_name,self._sprite_name}"
                    f" is empty for {graphic_state.name, direction.name} "
                )
            except Exception:
                # print(graphic_state, direction)
                LOG.exception(graphic_state, direction)
                raise
            data = {"ox": [0], "oy": [0], "duration": [1.0]}
        return data
