from typing import List, Optional, Union

from ...types.direction import Direction
from ...types.gate_color import GateColor
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..dynamic import Dynamic
from .switch import Switch


class ColorSwitch(Switch):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        facing_direction: Direction,
        graphic_state: GraphicState,
        color: GateColor,
        initial_signal=True,
        dyn_id=-1,
        name="ColorSwitch",
    ):

        super().__init__(
            px,
            py,
            tileset_name,
            image_name,
            sprite_name,
            facing_direction,
            graphic_state,
            initial_signal,
            dyn_id,
            name,
        )
        self.type = ObjectType.COLOR_SWITCH

        self.color = color
        self.graphic_state = (
            GraphicState.CLOSED
            if color == self.engine.gate_color
            else GraphicState.OPEN
        )
        # self.signal = self.graphic_state == GraphicState.CLOSED
        self.send_initial_signal = False

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        self.graphic_state = (
            GraphicState.CLOSED
            if self.color == self.engine.gate_color
            else GraphicState.OPEN
        )
        # self.signal = self.graphic_state == GraphicState.CLOSED
        #
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def on_interaction(self, target: Dynamic, nature: Nature):
        if (
            nature == Nature.TALK
            and target.type == ObjectType.PLAYER
            and self.visible
        ):
            if self.engine.gate_color != self.color:
                self.engine.gate_color = self.color
            else:
                self.engine.gate_color = GateColor(
                    (self.color.value + 1) % self.engine.n_gate_colors
                )
            self.state_changed = True
            self.engine.audio.play_sound("switch")
            return True

        return False

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        switch = ColorSwitch(
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
            color=GateColor[obj.get_string("color", "red").upper()],
            initial_signal=False,
            dyn_id=obj.object_id,
            name=obj.name,
        )

        switch.sprite.width = int(width * TILE_WIDTH)
        switch.sprite.height = int(height * TILE_HEIGHT)

        return [switch]
