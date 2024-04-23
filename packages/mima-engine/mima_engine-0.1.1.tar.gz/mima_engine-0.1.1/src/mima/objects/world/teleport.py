from __future__ import annotations
import logging
from typing import List, Optional

from ...scripts.commands.change_map import CommandChangeMap
from ...scripts.commands.move_map import CommandMoveMap
from ...scripts.commands.parallel import CommandParallel
from ...scripts.commands.screen_fade import CommandScreenFade
from ...scripts.commands.serial import CommandSerial
from ...scripts.commands.set_facing_direction import CommandSetFacingDirection
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.colors import RED
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic

LOG = logging.getLogger(__name__)


class Teleport(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        facing_direction: Direction,
        graphic_state: GraphicState,
        dst_map_name: str,
        dst_px: float,
        dst_py: float,
        direction: Direction,
        invert_exit_direction: bool = False,
        relative: bool = False,
        sliding: bool = False,
        vertical: bool = False,
        dyn_id: int = -1,
        name="Teleport",
    ):
        super().__init__(name, px, py, dyn_id)

        self.sprite = AnimatedSprite(
            tileset_name, image_name, sprite_name, graphic_state, facing_direction
        )

        self.type = ObjectType.TELEPORT
        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self.solid_vs_dyn = False
        self.solid_vs_map = False

        self.dst_px: float = dst_px
        self.dst_py: float = dst_py
        self.dst_map_name: str = dst_map_name
        self.has_sprite = self.sprite.name != ""
        self.teleport_direction: Direction = direction

        self.visible = True
        self.invert_exit_direction = invert_exit_direction
        self.relative = relative
        self.sliding = sliding
        self.vertical = vertical
        self.triggered = False
        self.sfx_on_trigger: str = ""

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        self.sprite.update(elapsed_time, self.facing_direction, self.graphic_state)

    def on_interaction(self, target: Dynamic, nature: Nature):
        if nature == Nature.SIGNAL:
            self.visible = True
            return True
        if nature == Nature.NO_SIGNAL:
            self.visible = False
            return True

        if self.has_sprite and not self.visible:
            return False

        if (
            nature == Nature.WALK
            and target.type == ObjectType.PLAYER
            and not self.engine.teleport_triggered
        ):
            self.engine.teleport_triggered = True
            dst_px = self.dst_px
            dst_py = self.dst_py
            dst_vx = 0
            dst_vy = 0

            dst_vx, dst_vy = Direction.to_velocity(self.teleport_direction)

            # if self.relative:
            #     if self.vertical:
            #         dst_py += target.py
            #     else:
            #         dst_px += target.px

            if self.sliding:
                if dst_vx != 0:
                    dst_py = target.py
                elif dst_vy != 0:
                    dst_px = target.px

                self.engine.script.add_command(
                    CommandMoveMap(
                        self.dst_map_name,
                        target,
                        dst_px,
                        dst_py,
                        dst_vx,
                        dst_vy,
                    )
                )
            else:
                if self.triggered:
                    return False

                new_direction = target.facing_direction
                if self.invert_exit_direction:
                    new_direction = Direction((target.facing_direction.value + 2) % 4)

                self.engine.script.add_command(
                    CommandSerial(
                        [
                            CommandScreenFade(),
                            CommandParallel(
                                [
                                    CommandChangeMap(self.dst_map_name, dst_px, dst_py),
                                    CommandSetFacingDirection(target, new_direction),
                                    CommandScreenFade(fadein=True),
                                ]
                            ),
                        ],
                    )
                )
                if self.sfx_on_trigger:
                    self.engine.audio.play_sound(self.sfx_on_trigger)

                self.triggered = True
            return True

        return False

    def draw_self(self, ox: float, oy: float):
        if not self.visible:
            self.engine.backend.draw_circle(
                (self.px + 0.5 - ox) * TILE_WIDTH,
                (self.py + 0.5 - oy) * TILE_HEIGHT,
                0.5 * TILE_WIDTH,
                RED,
            )
            return

        if self.has_sprite:
            self.sprite.draw_self(self.px - ox, self.py - oy)

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height) -> List[Teleport]:
        sprite_name = obj.get_string("sprite_name")
        tileset_name = obj.get_string("tileset_name")
        image_name = obj.get_string("tileset_name")
        graphic_state = GraphicState[obj.get_string("graphic_state", "closed").upper()]
        facing_direction = Direction[obj.get_string("facing_direction", "south").upper()]
        target_map = obj.get_string("target_map", "map1_c1")
        invert_exit_direction = obj.get_bool("invert_exit_direction")
        relative = obj.get_bool("relative", False)
        sliding = obj.get_bool("sliding", False)
        vertical = obj.get_bool("vertical", False)
        layer = obj.get_int("layer", 1)
        target_px = obj.get_float("target_px")
        target_py = obj.get_float("target_py")
        direction = Direction[obj.get_string("direction", "south").upper()]
        teleports = []
        if width > height and int(width) > 1:
            num_horizontal = int(width)
            for idx in range(num_horizontal):
                from_px = px + idx
                from_py = py
                to_px = target_px + idx
                to_py = target_py

                LOG.debug(
                    "Adding a teleport at (%f, %f) to map %s (%f, %f).",
                    from_px,
                    from_py,
                    target_map,
                    to_px,
                    to_py,
                )
                teleports.append(
                    Teleport(
                        px=from_px,
                        py=from_py,
                        tileset_name=tileset_name,
                        image_name=image_name,
                        sprite_name=sprite_name,
                        graphic_state=graphic_state,
                        facing_direction=facing_direction,
                        dst_map_name=target_map,
                        dst_px=to_px,
                        dst_py=to_py,
                        direction=direction,
                        invert_exit_direction=invert_exit_direction,
                        relative=relative,
                        sliding=sliding,
                        vertical=False,
                        dyn_id=obj.object_id,
                        name=obj.name,
                    )
                )
                teleports[-1].layer = layer
        elif height > width and int(height) > 1:
            num_vertical = int(height)
            for idx in range(num_vertical):
                from_px = px
                from_py = py + idx
                to_px = target_px
                to_py = target_py if relative else from_py

                LOG.debug(
                    "Adding a teleport at (%f, %f) to map %s (%f, %f).",
                    from_px,
                    from_py,
                    target_map,
                    to_px,
                    to_py,
                )
                teleports.append(
                    Teleport(
                        px=from_px,
                        py=from_py,
                        tileset_name=tileset_name,
                        image_name=image_name,
                        sprite_name=sprite_name,
                        graphic_state=graphic_state,
                        facing_direction=facing_direction,
                        dst_map_name=target_map,
                        dst_px=to_px,
                        dst_py=to_py,
                        direction=direction,
                        invert_exit_direction=invert_exit_direction,
                        relative=relative,
                        sliding=sliding,
                        vertical=True,
                        dyn_id=obj.object_id,
                        name=obj.name,
                    )
                )
                teleports[-1].layer = layer
        else:
            LOG.debug(
                "Adding a teleport at (%f, %f) to map %s (%f, %f).",
                px,
                py,
                target_map,
                target_px,
                target_py,
            )
            teleports.append(
                Teleport(
                    px=px,
                    py=py,
                    tileset_name=tileset_name,
                    image_name=image_name,
                    sprite_name=sprite_name,
                    graphic_state=graphic_state,
                    facing_direction=facing_direction,
                    dst_map_name=target_map,
                    dst_px=target_px,
                    dst_py=target_py,
                    direction=direction,
                    invert_exit_direction=invert_exit_direction,
                    relative=relative,
                    sliding=sliding,
                    vertical=vertical,
                    dyn_id=obj.object_id,
                    name=obj.name,
                )
            )
            teleports[-1].sfx_on_trigger = obj.get_string("sfx_name")
            teleports[-1].layer = layer

        return teleports
