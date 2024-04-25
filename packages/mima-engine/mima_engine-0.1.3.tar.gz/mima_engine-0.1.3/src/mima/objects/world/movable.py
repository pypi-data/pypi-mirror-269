import math
from typing import List, Optional

from ...types.alignment import Alignment
from ...types.damage import Damage
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.keys import Key as K
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.colors import BLACK
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic
from ..projectile import Projectile


class Movable(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        facing_direction: Direction,
        graphic_state: GraphicState,
        mrange: float,
        liftable: bool,
        destroyable: bool,
        movable: bool,
        intangible: bool,
        force_collision_check: bool,
        dyn_id=-1,
        name="Movable",
    ):
        super().__init__(name, px, py, dyn_id)

        self.sprite = AnimatedSprite(
            tileset_name,
            image_name,
            sprite_name,
            graphic_state,
            facing_direction,
        )
        self.type = ObjectType.MOVABLE
        self.alignment = Alignment.NEUTRAL
        self.facing_direction = facing_direction
        self.graphic_state = graphic_state
        self.solid_vs_map = True

        self.range = mrange
        self.total_range = 0
        self.spawn_px = px
        self.spawn_py = py

        self.liftable = liftable
        self.destroyable = destroyable
        self.movable = movable
        self.intangible = intangible
        self.moving = False
        self.lift_started = False
        self.lifted = False
        self.thrown = False
        self.visible = True
        self.visible_pz = 0.0
        self.actor: Optional[Dynamic] = None
        self.vx_mask = 0
        self.vy_mask = 0
        self.move_direction: str = ""
        self.onscreen_collision_skippable = (
            not self.movable and not force_collision_check
        )

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        if self.intangible:
            self.solid_vs_dyn = False
        else:
            self.solid_vs_dyn = (
                self.visible and not self.lifted and not self.thrown
            )
        if self.pz > 1.0:
            self.solid_vs_map = False
        else:
            self.solid_vs_map = True

        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

        if self.thrown:
            return self._throw()

        self.vx = self.vy = 0.0

        if self.moving:
            return self._move()

        if self.lift_started or self.lifted:
            return self._lift()

    def on_interaction(self, target: Dynamic, nature: Nature):
        if self.moving:
            return False
        if self.lifted:
            return False

        if target.type == ObjectType.PLAYER:
            if nature == Nature.TALK and self.liftable and target.can_lift:
                self.lift_started = True
                self.actor = target
                self.solid_vs_dyn = False
                target.can_attack = False
                return True

            if (
                self.movable
                and self.visible
                and self.total_range < self.range
                and target.graphic_state
                in [
                    GraphicState.WALKING,
                    GraphicState.PUSHING,
                ]
            ):
                if (
                    target.facing_direction == Direction.WEST
                    and self.engine.keys.key_held(K.LEFT)
                    and target.vy == 0
                ):
                    self.move_direction = K.LEFT
                    self.vx_mask = -1
                elif (
                    target.facing_direction == Direction.EAST
                    and self.engine.keys.key_held(K.RIGHT)
                    and target.vy == 0
                ):
                    self.move_direction = K.RIGHT
                    self.vx_mask = 1
                elif (
                    target.facing_direction == Direction.SOUTH
                    and self.engine.keys.key_held(K.DOWN)
                    and target.vx == 0
                ):
                    self.move_direction = K.DOWN
                    self.vy_mask = 1
                elif (
                    target.facing_direction == Direction.NORTH
                    and self.engine.keys.key_held(K.UP)
                    and target.vx == 0
                ):
                    self.move_direction = K.UP
                    self.vy_mask = -1
                else:
                    return False

                self.actor = target
                self.moving = True
                self.actor.lock_graphic_state(GraphicState.PUSHING)
                return True

        elif target.type == ObjectType.PROJECTILE:
            if self.destroyable:
                damage = target.damage - self.attributes.defense[target.dtype]
                if damage > 0:
                    self.kill()
                    if target.one_hit:
                        target.kill()
                return True

        elif nature == Nature.SIGNAL:
            self.visible = False
            return True

        elif nature == Nature.NO_SIGNAL:
            self.visible = True
            return True

        return False

    def draw_self(self, ox: float, oy: float):
        if not self.visible:
            return

        py = self.py - oy - (self.pz + self.visible_pz)

        if self.pz != 0:
            self.engine.backend.fill_circle(
                (self.px - ox + 0.5) * self.sprite.width,
                (self.py - oy + 0.7) * self.sprite.height,
                0.3125 * self.sprite.width,
                BLACK,
            )
        self.sprite.draw_self(self.px - ox, py)

    def _throw(self):
        if self.pz < 0.5:
            self.solid_vs_dyn = True
        if self.pz > 0:
            return

        self._create_impact()

        # self.solid_vs_dyn = True
        self.thrown = False
        self.vx = self.vy = 0.0
        if self.destroyable:
            self.kill()
        return

    def _move(self):
        if self.actor.graphic_state == GraphicState.PUSHING:
            stop_moving = False
            for button in [K.DOWN, K.LEFT, K.UP, K.RIGHT]:
                if button == self.move_direction:
                    if self.engine.keys.key_held(button):
                        self.vx = self.vx_mask
                        self.vy = self.vy_mask
                else:
                    if self.engine.keys.key_held(button):
                        stop_moving = True
                        self.vx = 0
                        self.vy = 0
                        break
            if (
                abs(self.actor.px - self.px) > 1.1
                or abs(self.actor.py - self.py) > 1.1
            ):
                stop_moving = True

            if not stop_moving and abs(self.vx) > abs(self.vy):
                self.vy = 0
            elif not stop_moving and abs(self.vy) > abs(self.vx):
                self.vx = 0
            else:
                self.vx = self.vy = 0.0

        dx = self.px - self.spawn_px
        dy = self.py - self.spawn_py
        self.total_range = math.sqrt(dx * dx + dy * dy)

        if self.total_range >= self.range:
            self.vx = self.vy = 0.0

        if self.vx == 0.0 and self.vy == 0.0:
            self.moving = False
            self.vx_mask = self.vy_mask = 0
            self.actor.unlock_graphic_state()
            self.engine.audio.stop_sound("move_block")
        else:
            self.engine.audio.play_sound("move_block")
        return

    def _lift(self):
        if self.lifted and self.engine.keys.new_key_press(K.A):
            # Throw away
            self.vx = self.vy = 0
            if self.actor.facing_direction == Direction.SOUTH:
                self.vy = 4
            if self.actor.facing_direction == Direction.WEST:
                self.vx = -4
            if self.actor.facing_direction == Direction.NORTH:
                self.vy = -4
            if self.actor.facing_direction == Direction.EAST:
                self.vx = 4

            self.vz = 6.0
            self.pz = self.actor.pz + 0.9
            self.visible_pz = 0
            self.actor.can_attack = True
            self.lifted = False
            self.actor = None
            self.thrown = True

        elif self.lift_started and self.engine.keys.new_key_release(K.A):
            self.lift_started = False
            self.lifted = True
            self.solid_vs_dyn = False
        else:
            self.solid_vs_dyn = False
            self.px = self.actor.px
            self.py = self.actor.py
            self.visible_pz = self.actor.pz + 0.9
            self.vx = self.vy = 0.0

    def _create_impact(self):
        impact: List[Projectile] = []
        impact.append(
            Projectile(self.px + 0.5, self.py + 0.5, 0, 0, 0.2, self.alignment)
        )
        impact.append(
            Projectile(self.px - 0.5, self.py + 0.5, 0, 0, 0.2, self.alignment)
        )
        impact.append(
            Projectile(self.px - 0.5, self.py - 0.5, 0, 0, 0.2, self.alignment)
        )
        impact.append(
            Projectile(self.px + 0.5, self.py - 0.5, 0, 0, 0.2, self.alignment)
        )

        for pro in impact:
            pro.sprite.name = "explosion"
            pro.solid_vs_dyn = False
            pro.solid_vs_map = False
            pro.damage = 5
            self.engine.scene.add_projectile(pro)

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        movable = Movable(
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
            mrange=obj.get_float("range"),
            liftable=obj.get_bool("liftable"),
            destroyable=obj.get_bool("destroyable"),
            movable=obj.get_bool("movable"),
            intangible=obj.get_bool("intangible"),
            force_collision_check=obj.get_bool("force_collision_check"),
            dyn_id=obj.object_id,
            name=obj.name,
        )
        movable.sprite.width = int(width * TILE_WIDTH)
        movable.sprite.height = int(height * TILE_HEIGHT)
        for dt in Damage:
            movable.attributes.defense[dt] = obj.get_int(
                f"defense_{dt.name.lower()}"
            )

        return [movable]
