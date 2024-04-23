from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ..types.alignment import Alignment
from ..types.damage import Damage
from ..types.direction import Direction
from ..types.graphic_state import GraphicState, Until
from ..types.nature import Nature
from ..types.object import ObjectType
from ..types.terrain import Terrain
from .attributes import Attributes
from .attribute_effect import Effect
from .sprite import Sprite

if TYPE_CHECKING:
    from ..engine import MimaEngine
    from .projectile import Projectile


class Dynamic:
    engine: MimaEngine

    def __init__(
        self,
        name: str = "Unnamed Dynamic",
        px: float = 0.0,
        py: float = 0.0,
        dyn_id=-1,
    ):
        self.name: str = name
        self.dyn_id: int = dyn_id  # ID given by Tiled
        self.layer: int = 1

        self.px: float = px
        self.py: float = py
        self.pz: float = 0.0
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.vz: float = 0.0
        self.real_vx: float = 0.0
        self.real_vy: float = 0.0
        self.hitbox_px: float = 0.1
        self.hitbox_py: float = 0.1
        self.hitbox_width: float = 0.8
        self.hitbox_height: float = 0.8
        self.attribute_timer: float = 0.25
        self.despawn_timer: float = 0.5
        self.despawn_duration: float = 0.2
        self.timer: float = 0.0
        self.speed: float = 1.0

        self.solid_vs_map: bool = True
        self.solid_vs_dyn: bool = True
        # self.is_player: bool = False
        # self.is_projectile: bool = False
        self.redundant: bool = False
        self.persistent: bool = False
        self.attackable: bool = False
        self.controllable: bool = True
        self.state_changed: bool = False
        self.visible: bool = True
        self.gravity: bool = True
        self.graphic_state_locked: bool = False
        self.use_acceleration: bool = False
        self.use_friction: bool = False

        self.alignment: Alignment = Alignment.GOOD
        self.walking_on: Terrain = Terrain.DEFAULT
        self.attributes: Attributes = Attributes()
        self.facing_direction: Direction = Direction.SOUTH
        self.graphic_state: GraphicState = GraphicState.STANDING
        self._gs_lock_condition: Until = Until.UNLOCK
        self.type: ObjectType = ObjectType.UNDEFINED
        self.spawn_on_death: List[Dynamic] = []
        self.childs: List[Dynamic] = []
        self.effects: List[Projectile] = []
        self.attribute_effects: List[Effect] = []

        self.extra_ox: float = 0.0
        self.extra_oy: float = 0.0

        self.can_attack: bool = True
        self.can_lift: bool = False
        self.can_push: bool = False

        self.sprite: Sprite = Sprite()

        # Performance flags
        self.update_skippable: bool = False
        """Update may be skipped if object is offscreen."""
        self.offscreen_collision_skippable: bool = True
        """Collision checks may be skipped if object is offscreen."""
        self.onscreen_collision_skippable: bool = False
        """Collision checks may be skipped if object is onscreen."""
        self.draw_skippable: bool = True
        """Drawing the unit may be skipped if object is offscreen."""

    def update(self, elapsed_time: float, target: Optional[Dynamic]):
        """Update this dynamic."""
        pass

    def draw_self(self, ox: float, oy: float):
        """Draw self to screen"""
        pass

    def on_interaction(
        self, target: Dynamic = None, nature: Nature = Nature.WALK
    ) -> bool:
        """Handle interaction with other dynamic objects."""
        return False

    def on_death(self) -> bool:
        return False

    def kill(self):
        self.redundant = True

    def change_graphic_state(self, new_state: GraphicState) -> bool:
        if self.graphic_state_locked or new_state == self.graphic_state:
            return False

        self.graphic_state = new_state
        self.sprite.update(0.0, self.facing_direction, self.graphic_state)

        return True

    def lock_graphic_state(
        self,
        new_state: GraphicState = GraphicState.STANDING,
        until: Until = Until.UNLOCK,
    ):
        self.change_graphic_state(new_state)
        self.graphic_state_locked = True
        self._gs_lock_condition = until

    def unlock_graphic_state(self):
        self.graphic_state_locked = False
        self.change_graphic_state(GraphicState.STANDING)

    def get_defense_value(self, dtype: Damage) -> int:
        return self.attributes.defense[dtype]

    def is_py_lower(self, other: Dynamic) -> bool:
        return self.py < other.py

    def get_alignment(self) -> Alignment:
        return self.alignment

    def add_effect(self, eff: Effect):
        self.attribute_effects.append(eff)

    def remove_effect(self, eff: Union[str, Effect]):
        if isinstance(eff, str):
            obj = [e for e in self.attribute_effects if e.effect_id == eff]
            if not obj:
                print("Effect not active")
                return
            else:
                eff = obj[0]

        self.attribute_effects.remove(eff)

    def has_effect(self, eff: Union[str, Effect]):
        if isinstance(eff, str):
            for e in self.attribute_effects:
                if e.effect_id == eff:
                    return True
            return False
        else:
            if eff in self.attribute_effects:
                return True
            else:
                return False

    def light_radius(self):
        rad = self.attributes.light_radius

        for eff in self.attribute_effects:
            rad += eff.light_radius

        return rad
