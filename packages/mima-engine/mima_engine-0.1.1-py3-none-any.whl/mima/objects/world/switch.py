from typing import List, Optional, Union

from ...types.alignment import Alignment
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic


class Switch(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        facing_direction: Direction,
        graphic_state: GraphicState,
        initial_signal=True,
        dyn_id=-1,
        name="Switch",
    ):
        assert graphic_state in [GraphicState.OPEN, GraphicState.CLOSED], (
            f"graphic_state of Switch {name}{dyn_id} must be either 'open'"
            f" or 'closed', but it {graphic_state}"
        )
        super().__init__(name, px, py, dyn_id)

        self.sprite = AnimatedSprite(
            tileset_name,
            image_name,
            sprite_name,
            graphic_state,
            facing_direction,
        )

        self.type = ObjectType.SWITCH
        self.alignment = Alignment.NEUTRAL
        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self.signal = self.graphic_state == GraphicState.CLOSED
        self.listener_ids: List[int] = []
        self.listeners: List[Dynamic] = []
        self.send_initial_signal = initial_signal

        # self._gs_map = {False: GraphicState.OPEN, True: GraphicState.CLOSED}

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        if self.send_initial_signal:
            self.send_signal(self.signal)
            self.send_initial_signal = False

        self.solid_vs_dyn = self.visible
        self.graphic_state = (
            GraphicState.CLOSED if self.signal else GraphicState.OPEN
        )
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def draw_self(self, ox: float, oy: float):
        if not self.visible:
            # print(f"{self.name} is not visible")
            return
        self.sprite.draw_self(self.px - ox, self.py - oy)

    def on_interaction(self, target: Dynamic, nature: Nature):
        if (
            nature == Nature.TALK
            and target.type == ObjectType.PLAYER
            and self.visible
        ):
            self.state_changed = True
            self.engine.audio.play_sound("switch")

        elif nature == Nature.WALK and target.type == ObjectType.PROJECTILE:
            if self.signal:
                # Projectiles from the right will activate the switch
                if target.px > self.px and target.vx < 0:
                    self.state_changed = True
            else:
                # Projectiles from the left will (de)activate the switch
                if target.px <= self.px and target.vx > 0:
                    self.state_changed = True
            if "body" not in target.name:
                self.engine.audio.play_sound("switch")

        elif nature == Nature.SIGNAL:
            self.visible = False
            return True

        elif nature == Nature.NO_SIGNAL:
            self.visible = True
            return True

        if self.state_changed:
            self.signal = not self.signal
            self.send_signal(self.signal)

            if target.type == ObjectType.PROJECTILE:
                target.kill()
            return True
        return False

    def send_signal(self, nature: Union[Nature, bool]):
        if isinstance(nature, bool):
            nature = Nature.SIGNAL if nature else Nature.NO_SIGNAL

        for listener in self.listeners:
            listener.on_interaction(self, nature)

        if (
            not self.send_initial_signal
            and abs(self.engine.player.px - self.px)
            < (self.engine.backend.render_width // (TILE_WIDTH * 2))
            and abs(self.engine.player.py - self.py)
            < (self.engine.backend.render_height // (TILE_HEIGHT * 2))
        ):
            print(
                (
                    self.engine.player.px - self.px,
                    self.engine.player.py - self.py,
                ),
                (
                    self.engine.backend.render_width // (TILE_WIDTH * 2),
                    self.engine.backend.render_height // (TILE_HEIGHT * 2),
                ),
            )

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        switch = Switch(
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
            initial_signal=obj.get_bool("initial_signal", True),
            dyn_id=obj.object_id,
            name=obj.name,
        )

        switch.sprite.width = int(width * TILE_WIDTH)
        switch.sprite.height = int(height * TILE_HEIGHT)

        ctr = 1
        while True:
            key = f"output{ctr}"
            listener_id = obj.get_int(key, -1)
            if listener_id < 0:
                break
            switch.listener_ids.append(listener_id)
            ctr += 1

        return [switch]
