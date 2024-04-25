from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from ..types.damage import Damage
from ..types.direction import Direction
from .item import Item

if TYPE_CHECKING:
    from ..objects.creature import Creature


class Weapon(Item):
    def __init__(self, name: str, sprite: str, description: str):
        super().__init__(name, sprite, description)

        self.equipable = True

        self.damage: int = 0
        self.dtype: Damage = Damage.BODY
        self.health_cost: int = 0
        self.magic_cost: int = 0
        self.stamina_cost: int = 0
        self.arrow_cost: int = 0
        self.bomb_cost: int = 0
        self.swing_timer: int = 0.2
        # self.projectiles: List[Projectile] = []

    def _determine_attack_origin(self, obj: Creature) -> Tuple[float, float]:
        vx = 0.0
        vy = 0.0

        if obj.facing_direction == Direction.SOUTH:
            vy = 1.0
        if obj.facing_direction == Direction.WEST:
            vx = -1.0
        if obj.facing_direction == Direction.NORTH:
            vy = -1.0
        if obj.facing_direction == Direction.EAST:
            vx = 1.0

        return vx, vy

    def on_equip(self, obj: Creature):
        pass

    def on_unequip(self, obj: Creature):
        pass
