from __future__ import annotations

from typing import TYPE_CHECKING

from ..util.constants import DEFAULT_SPRITE_HEIGHT, DEFAULT_SPRITE_WIDTH

if TYPE_CHECKING:
    from ..engine import MimaEngine
    from ..objects.creature import Creature
    from ..objects.dynamic import Dynamic


class Item:
    engine: MimaEngine

    def __init__(self, name: str, sprite_name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.sprite_name: str = sprite_name
        self.sprite_ox: int = 0
        self.sprite_oy: int = 0
        self.sprite_width: int = DEFAULT_SPRITE_WIDTH
        self.sprite_height: int = DEFAULT_SPRITE_HEIGHT
        self.key_item: bool = False
        self.equipable: bool = False

    def on_interaction(self, obj: Dynamic):
        return False

    def on_use(self, obj: Creature):
        return False
