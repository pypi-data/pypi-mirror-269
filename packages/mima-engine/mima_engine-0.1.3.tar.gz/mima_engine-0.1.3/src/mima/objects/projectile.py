from ..types.alignment import Alignment
from ..types.damage import Damage
from ..types.object import ObjectType
from .dynamic import Dynamic


class Projectile(Dynamic):
    def __init__(
        self,
        px: float,
        py: float,
        vx: float,
        vy: float,
        duration: float,
        alignment: Alignment,
        name: str = "Projectile",
    ):
        super().__init__(name, px, py)

        self.type = ObjectType.PROJECTILE
        self.vx = vx
        self.vy = vy
        self.pz = 0.5
        self.duration = duration
        self.alignment = alignment

        self.solid_vs_dyn = False
        self.solid_vs_map = True
        self.is_projectile = True  # redundant
        self.attackable = False
        self.one_hit = False
        self.inherit_pos = False
        self.gravity = False
        self.change_solid_vs_map_timer = 0
        self.dtype = Damage.BODY
        self.damage = 0

    def update(self, elapsed_time: float, target: Dynamic = None):
        self.duration -= elapsed_time
        if self.duration <= 0.0:
            self.kill()

        if self.change_solid_vs_map_timer > 0:
            self.change_solid_vs_map_timer -= elapsed_time
            if self.change_solid_vs_map_timer <= 0:
                self.solid_vs_map = not self.solid_vs_map
                self.change_solid_vs_map_timer = 0

        self.speed = self.attributes.speed

        self.sprite.update(
            elapsed_time, self.facing_direction, self.graphic_state
        )

    def draw_self(self, ox: float, oy: float):
        if (
            self.sprite.name is None
            or self.sprite.name == ""
            or self.redundant
        ):
            return

        self.sprite.draw_self(self.px - ox, self.py - oy)

    def on_death(self) -> bool:
        if self.spawn_on_death:
            for do in self.spawn_on_death:
                if do.type == ObjectType.PROJECTILE:
                    if self.inherit_pos:
                        do.px = self.px
                        do.py = self.py
                    self.engine.scene.add_projectile(do)
                else:
                    self.engine.scene.add_dynamic(do)

        return False

    def cancel(self):
        if self.spawn_on_death:
            for do in self.spawn_on_death:
                if do.type == ObjectType.PROJECTILE:
                    do.cancel()  # Projectile will kill itself
                else:
                    do.kill()
        self.kill()
        return True
