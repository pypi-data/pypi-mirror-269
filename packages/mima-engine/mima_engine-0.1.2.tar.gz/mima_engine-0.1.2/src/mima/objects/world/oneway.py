from ...scripts.commands.oneway_move import CommandOnewayMove
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.constants import ONEWAY_ACTIVATION_DELAY, TILE_HEIGHT, TILE_WIDTH
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic


class Oneway(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        facing_direction: Direction,
        graphic_state: GraphicState,
        jump_vx: float,
        jump_vy: float,
        width: float,
        height: float,
        dyn_id=-1,
        name="Oneway",
    ):
        super().__init__(name, px, py, dyn_id)
        self.sprite = AnimatedSprite(
            tileset_name,
            image_name,
            sprite_name,
            graphic_state,
            facing_direction,
        )
        self.type = ObjectType.ONEWAY
        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self.sprite.width = int(width * TILE_WIDTH)
        self.sprite.height = int(height * TILE_HEIGHT)

        self.hitbox_px, self.hitbox_py = 0.0, 0.0
        self.hitbox_width, self.hitbox_height = 1.0, 1.0
        self.solid_vs_map = False

        self.width: float = width
        self.height: float = height
        self.jump_vx: float = 0.0
        self.jump_vy: float = 0.0
        self.activation_delay: float = ONEWAY_ACTIVATION_DELAY
        self.triggered: bool = False
        self.cooldown: float = 0.0

        if jump_vx < 0:
            self.jump_vx = jump_vx - 1
            self.hitbox_px += 0.1
        elif jump_vx > 0:
            self.jump_vx = jump_vx + 1
            self.hitbox_px -= 0.1

        if jump_vy < 0:
            self.jump_vy = jump_vy - 1
            self.hitbox_py += 0.1
        elif jump_vy > 0:
            self.jump_vy = jump_vy + 1
            self.hitbox_py -= 0.1

    def update(self, elapsed_time, target=None):
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

        # Can only be triggered again after a certain time has passed.
        if self.cooldown >= 0.0:
            self.cooldown -= elapsed_time
            return
        else:
            self.cooldown = 0.0

        # If no interaction happened in a frame, the activation timer
        # gets resetted.
        if not self.triggered:
            self.timer = 0.0
            return

        # Activation countdown
        if self.timer > 0.0:
            self.timer -= elapsed_time

        # Activation countdown reached 0 and the jump is initiated.
        if self.timer <= 0.0:
            self.engine.script.add_command(
                CommandOnewayMove(target, self.jump_vx, self.jump_vy)
            )
            self.cooldown = 2.0

        # Reset the triggered flag so it has to be activated again
        # by interaction
        self.triggered = False

    def on_interaction(self, target, nature=Nature.WALK):
        if target.type == ObjectType.PLAYER and nature == Nature.WALK:
            # No interaction when target is higher than the oneway
            if target.pz > 0:
                return False

            # We have to check that target is not placed "more" in the
            # target direction than the oneway
            if (
                self.jump_vx < 0
                and target.px < self.px + self.width - target.hitbox_px
            ):
                return False
            if self.jump_vx > 0 and target.px >= self.px:
                return False
            if (
                self.jump_vy < 0
                and target.py <= self.py + self.height - target.hitbox_py
            ):
                return False
            if self.jump_vy > 0 and target.py >= self.py:
                return False

            if self.jump_vx == 0:
                if target.px >= self.px + self.width:
                    return False
                if target.px + 1.0 <= self.px:
                    return False

            if self.jump_vy == 0:
                if target.py >= self.py + self.height:
                    return False
                if target.py + 1.0 <= self.py:
                    return False

            self.triggered = True
            if self.timer <= 0.0:
                self.timer = self.activation_delay

            return True

        return False

    def draw_self(self, ox: float, oy: float):
        self.sprite.draw_self(self.px - ox, self.py - oy)

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        oneway = Oneway(
            px=px,
            py=py,
            tileset_name=obj.get_string("tileset_name"),
            image_name=obj.get_string("tileset_name"),
            sprite_name=obj.get_string("sprite_name"),
            graphic_state=GraphicState[
                obj.get_string("graphic_state", "standing").upper()
            ],
            facing_direction=Direction[
                obj.get_string("facing_direction", "south").upper()
            ],
            jump_vx=obj.get_float("jump_vx"),
            jump_vy=obj.get_float("jump_vy"),
            width=width,
            height=height,
            dyn_id=obj.object_id,
            name=obj.name,
        )
        return [oneway]
