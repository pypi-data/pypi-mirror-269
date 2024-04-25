from ...objects.dynamic import Dynamic
from ...types.nature import Nature
from ...types.object import ObjectType
from ...types.terrain import Terrain
from ...util.colors import BLACK
from ..effects.walking_on_grass import WalkingOnGrass
from ..effects.walking_on_water import WalkingOnWater


class Pickup(Dynamic):
    def __init__(self, px: float, py: float, item_name: str, dyn_id=-1):
        super().__init__("Pickup", px, py, dyn_id)
        self.type: ObjectType = ObjectType.PICKUP
        self.item = self.engine.get_item(item_name)
        self.collected = False
        self.solid_vs_dyn = False

    def update(self, elapsed_time: float, target=None):
        if self.collected:
            self.kill()
        else:
            self._handle_terrain(elapsed_time)

    def on_interaction(self, target: Dynamic, nature: Nature):
        if self.collected:
            return False

        if target.type == ObjectType.PLAYER:
            if self.item.on_interaction(target):
                if self.engine.give_item(self.item):
                    self.collected = True
                    return True
            else:
                self.collected = True

        return False

    def draw_self(self, ox: float, oy: float):
        if self.collected:
            return

        if self.pz != 0:
            self.engine.backend.fill_circle(
                (self.px - ox + 0.5) * self.item.sprite_width,
                (self.py - oy + 0.7) * self.item.sprite_height,
                0.2875 * self.item.sprite_width,
                BLACK,
            )

        self.engine.backend.draw_partial_sprite(
            (self.px - ox) * self.item.sprite_width,
            (self.py - oy - self.pz) * self.item.sprite_height,
            self.item.sprite_name,
            self.item.sprite_ox * self.item.sprite_width,
            self.item.sprite_oy * self.item.sprite_height,
            self.item.sprite_width,
            self.item.sprite_height,
        )

    def _handle_terrain(self, elapsed_time: float):
        """Method is duplicated."""
        e2rm = []
        for effect in self.effects:
            if isinstance(effect, WalkingOnGrass):
                if self.walking_on == Terrain.DEFAULT:
                    e2rm.append(effect)

        for effect in e2rm:
            self.effects.remove(effect)

        if self.walking_on in [Terrain.GRASS, Terrain.SHALLOW_WATER]:
            # self.attributes.speed_mod = 0.7
            effect_active = False
            for effect in self.effects:
                if isinstance(effect, (WalkingOnGrass, WalkingOnWater)):
                    effect_active = True
                    effect.renew = True
                    break

            if not effect_active:
                if self.walking_on == Terrain.GRASS:
                    eff = WalkingOnGrass(self)
                else:
                    eff = WalkingOnWater(self)
                self.effects.append(eff)
                self.engine.scene.add_effect(eff)
        # else:
        #     self.attributes.speed_mod = 1.0
