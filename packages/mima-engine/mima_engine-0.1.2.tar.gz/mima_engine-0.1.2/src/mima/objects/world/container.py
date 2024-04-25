from __future__ import annotations

from typing import List, Optional

from ...scripts.commands.give_item import CommandGiveItem
from ...scripts.commands.give_resource import CommandGiveResource
from ...scripts.commands.parallel import CommandParallel
from ...scripts.commands.present_item import CommandPresentItem
from ...scripts.commands.show_dialog import CommandShowDialog
from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ...types.nature import Nature
from ...types.object import ObjectType
from ..animated_sprite import AnimatedSprite
from ..dynamic import Dynamic


class Container(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        tileset_name: str,
        image_name: str,
        sprite_name: str,
        graphic_state: GraphicState,
        facing_direction: Direction,
        item_name: str,
        dyn_id: int = -1,
        name: str = "Container",
    ):
        assert graphic_state in [
            GraphicState.OPEN,
            GraphicState.CLOSED,
        ], (
            f"graphic_state of Container {name}{dyn_id} must be either 'open'"
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

        self.type = ObjectType.CONTAINER
        self.graphic_state = graphic_state
        self.facing_direction = facing_direction
        self.closed: bool = self.graphic_state != GraphicState.OPEN

        self.item_name: str = item_name
        self.solid_vs_dyn: bool = True
        self.solid_vs_map: bool = True
        self.visible: bool = True

        self.is_resource: bool = False
        self.amount: int = 1

        # self.sprite = AnimatedSprite("simple_sheet", "simple_sheet", "chest01")
        self._gs_map = {False: GraphicState.OPEN, True: GraphicState.CLOSED}

    def update(self, elapsed_time: float, target: Optional[Dynamic] = None):
        if self.visible:
            self.solid_vs_dyn = True
        else:
            self.solid_vs_dyn = False

        self.graphic_state = (
            GraphicState.CLOSED if self.closed else GraphicState.OPEN
        )

        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def draw_self(self, ox: float, oy: float):
        if not self.visible:
            return

        self.sprite.draw_self(self.px - ox, self.py - oy)

    def on_interaction(self, target: Dynamic, nature: Nature):
        if nature == Nature.SIGNAL:
            self.visible = True
            return True

        if nature == Nature.NO_SIGNAL:
            self.visible = False
            return True

        if not self.visible:
            return False

        if nature == Nature.TALK:
            if self.closed:
                if self.is_resource:
                    text = "You received "
                    if self.amount > 1:
                        text += f"{self.amount} {self.item_name}s!"
                    elif self.amount == 1:
                        text += f"one {self.item_name}!"
                    else:
                        text += "nothing. The chest was empty!"

                    if self.item_name == "Coin":
                        cgr = CommandGiveResource(target, coins=self.amount)
                    elif self.item_name == "Bomb Refill":
                        cgr = CommandGiveResource(target, bombs=self.amount)
                    elif self.item_name == "Arrow Refill":
                        cgr = CommandGiveResource(target, arrows=self.amount)
                    elif self.item_name == "Key":
                        cgr = CommandGiveResource(target, keys=self.amount)
                    else:
                        print(f"Invalid resource type: {self.item_name}")
                        return False

                    self.engine.script.add_command(
                        CommandParallel(
                            [
                                CommandShowDialog([text]),
                                CommandPresentItem(self.item_name, target),
                                cgr,
                            ],
                            CommandParallel.FIRST_COMPLETED,
                        )
                    )

                else:
                    self.engine.script.add_command(
                        CommandParallel(
                            [
                                CommandShowDialog(
                                    [f"You received {self.item_name}"],
                                ),
                                CommandPresentItem(self.item_name, target),
                                CommandGiveItem(self.item_name, target),
                            ],
                            CommandParallel.FIRST_COMPLETED,
                        )
                    )
                self.closed = False
                self.state_changed = True
                return True

        return False

    @staticmethod
    def load_from_tiled_object(obj, px, py, width, height) -> List[Container]:
        container = Container(
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
            item_name=obj.get_string("item_name"),
            dyn_id=obj.object_id,
            name=obj.name,
        )
        container.is_resource = obj.get_bool("is_resource", False)
        container.amount = obj.get_int("amount", 1)

        return [container]
