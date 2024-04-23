from __future__ import annotations

from ...types.damage import Damage
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic
from .teleport import Teleport


class Gate(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        graphic_state: GraphicState,
        facing_direction: Direction,
        bombable: bool = False,
        dyn_id: int = -1,
        name: str = "Gate",
    ):
        assert graphic_state in [
            GraphicState.OPEN,
            GraphicState.CLOSED,
            GraphicState.LOCKED,
        ], (
            f"graphic_state of Gate {name}{dyn_id} must be either 'open'"
            f", 'closed', or 'locked', but it {graphic_state}"
        )

        super().__init__(name, px, py, dyn_id)

        self.sprite = AnimatedSprite(
            tileset_name,
            image_name,
            sprite_name,
            graphic_state,
            facing_direction,
        )
        self.type = ObjectType.GATE

        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self.open = self.graphic_state == GraphicState.OPEN

        # self.closed_sprite_name = closed_sprite_name
        # self.open_sprite_name = open_sprite_name
        # self.closed_sprite_ox: float = closed_sprite_ox
        # self.closed_sprite_oy: float = closed_sprite_oy
        # self.open_sprite_ox: float = open_sprite_ox
        # self.open_sprite_oy: float = open_sprite_oy

        # self.open = open
        self.bombable = bombable
        self.requires_key = self.graphic_state == GraphicState.LOCKED
        self.unlocked = False
        self.solid_vs_map = False
        self.layer = 0
        self.hitbox_px = self.hitbox_py = 0.0
        self.hitbox_width = self.hitbox_height = 1.0
        # self._set_sprite_state()

    def update(self, elapsed_time: float, target: Dynamic):
        self.solid_vs_dyn = not self.open
        self.graphic_state = (
            GraphicState.OPEN
            if self.open
            else (
                GraphicState.LOCKED
                if self.requires_key
                else GraphicState.CLOSED
            )
        )

        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def on_interaction(self, target: Dynamic, nature: Nature):
        if nature == Nature.TALK:
            if target.type == ObjectType.PLAYER:
                if (
                    not self.open
                    and self.requires_key
                    and target.attributes.keys > 0
                ):
                    target.attributes.keys -= 1
                    self.open = True
                    self.state_changed = True
                    self.unlocked = True
                    return True

        if nature == Nature.SIGNAL:
            self.open = True
            self.state_changed = True
            return True

        if nature == Nature.NO_SIGNAL and not self.unlocked:
            self.open = False
            self.state_changed = True
            return True

        if self.bombable and target.type == ObjectType.PROJECTILE:
            if target.dtype == Damage.EXPLOSION:
                self.open = True
                self.state_changed = True
                if target.one_hit:
                    target.kill()

        return False

    def draw_self(self, ox: float, oy: float):
        self.sprite.draw_self(self.px - ox, self.py - oy)

    @staticmethod
    def load_from_tiled_object(
        obj, px: float, py: float, width: float, height: float
    ) -> Gate:
        gate = [
            Gate(
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
                bombable=obj.get_bool("bombable"),
                dyn_id=obj.object_id,
                name=obj.name,
            )
        ]

        if obj.get_bool("has_teleport"):
            if gate[0].facing_direction == Direction.NORTH:
                py += 0.4
            elif gate[0].facing_direction == Direction.SOUTH:
                py -= 0.1

            teleport = Teleport(
                px=px,
                py=py,
                tileset_name="",
                image_name="",
                sprite_name="",
                dst_map_name=obj.get_string("target_map"),
                dst_px=obj.get_float("target_px"),
                dst_py=obj.get_float("target_py"),
                facing_direction=gate[0].facing_direction,
                graphic_state=GraphicState.STANDING,
                direction=gate[0].facing_direction,
                invert_exit_direction=False,
                relative=False,
                sliding=False,
                vertical=False,
                dyn_id=gate[0].dyn_id + 2000,
                name=f"Teleport of {gate[0].name}",
            )

            teleport.visible = False
            teleport.sfx_on_trigger = "pass_door"

            gate.append(teleport)

        return gate
