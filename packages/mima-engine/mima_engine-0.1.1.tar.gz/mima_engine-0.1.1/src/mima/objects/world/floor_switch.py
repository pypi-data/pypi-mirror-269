from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..dynamic import Dynamic
from .switch import Switch


class FloorSwitch(Switch):
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
        name="Floor Switch",
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
        self.layer = 0

        self.type = ObjectType.FLOOR_SWITCH
        self.interacted = False
        self.interacted_before = False
        self.solid_vs_dyn = False

    def update(self, elapsed_time: float, target: Dynamic):
        if self.send_initial_signal:
            self.send_signal(self.signal)
            self.send_initial_signal = False
        self.state_changed = False
        if not self.interacted:
            if self.interacted_before:
                self.state_changed = True
            self.interacted_before = False

        else:
            if not self.interacted_before:
                self.state_changed = True
            self.interacted_before = True

        self.interacted = False

        if self.state_changed:
            self.signal = not self.signal
            self.send_signal(self.signal)

        self.graphic_state = (
            GraphicState.CLOSED if self.signal else GraphicState.OPEN
        )
        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def on_interaction(self, target: Dynamic, nature: Nature):
        if nature == Nature.WALK and not target.type == ObjectType.PROJECTILE:
            if target.type == ObjectType.MOVABLE:
                if not target.visible:
                    return False
            self.interacted = True
            return True

        return False

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height):
        fswitch = FloorSwitch(
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
        fswitch.sprite.width = int(width * TILE_WIDTH)
        fswitch.sprite.height = int(height * TILE_HEIGHT)

        ctr = 1
        while True:
            key = f"output{ctr}"
            listener_id = obj.get_int(key, -1)
            if listener_id < 0:
                break
            fswitch.listener_ids.append(listener_id)
            ctr += 1

        return [fswitch]
