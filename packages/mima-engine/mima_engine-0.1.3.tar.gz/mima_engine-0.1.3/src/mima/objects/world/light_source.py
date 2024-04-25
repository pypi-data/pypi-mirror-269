from typing import Optional

from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic
from ..effects.light import Light
from ..projectile import Projectile


class LightSource(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        graphic_state: GraphicState,
        facing_direction: Direction,
        max_size: int,
        dyn_id: int = -1,
        name: str = "LightSource",
    ):
        assert graphic_state in [GraphicState.OFF, GraphicState.ON], (
            f"graphic_state of LightSource {name}{dyn_id} must be either "
            f"'off' or 'on', but it {graphic_state}"
        )
        super().__init__(name, px, py, dyn_id)

        self.sprite = AnimatedSprite(
            tileset_name,
            image_name,
            sprite_name,
            graphic_state,
            facing_direction,
        )

        self.type = ObjectType.LIGHT_SOURCE
        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self._max_size = max_size
        self.active = self.graphic_state == GraphicState.ON
        self._light: Optional[Projectile] = None

        self.hitbox_px = 0.0
        self.hitbox_py = 0.0
        self.hitbox_width = 1.0
        self.hitbox_height = 1.0
        self.solid_vs_dyn = True
        self.solid_vs_map = False
        self.onscreen_collision_skippable = True
        self._state_changed = True

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        if self._state_changed:
            # self._set_sprite_state()
            self._state_changed = False

        if self.active:
            if self._light is None:
                self._light = Light(self, self._max_size)
                self.engine.scene.add_effect(self._light)
        else:
            if self._light is not None:
                self._light.kill()
                self._light = None

        self.graphic_state = (
            GraphicState.ON if self.active else GraphicState.OFF
        )
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def on_interaction(self, target: Dynamic, nature: Nature):
        if nature == Nature.SIGNAL:
            self.active = True
            self._state_changed = True
            return True

        if nature == Nature.NO_SIGNAL:
            self.active = False
            self._state_changed = True
            return True

        if nature == Nature.TALK:
            self.active = not self.active
            self._state_changed = True
            return True

    def draw_self(self, ox: float, oy: float):
        self.sprite.draw_self(self.px - ox, self.py - oy)

    def on_death(self) -> bool:
        self._light.kill()
        return True

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        light = LightSource(
            px=px,
            py=py,
            tileset_name=obj.get_string("tileset_name"),
            image_name=obj.get_string("tileset_name"),
            sprite_name=obj.get_string("sprite_name"),
            graphic_state=GraphicState[
                obj.get_string("graphic_state", "closed").upper()
            ],
            facing_direction=Direction[
                obj.get_string("facing_direction", "south").upper()
            ],
            max_size=obj.get_int("max_size", 32),
            dyn_id=obj.object_id,
            name=obj.name,
        )

        light.sprite.width = int(width * TILE_WIDTH)
        light.sprite.height = int(height * TILE_HEIGHT)

        return [light]
