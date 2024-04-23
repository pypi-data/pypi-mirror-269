from ...types.direction import Direction
from ...types.graphic_state import GraphicState
from ..dynamic import Dynamic
from ..projectile import Projectile


class WalkingOnGrass(Projectile):
    def __init__(self, follow: Dynamic):
        super().__init__(follow.px, follow.py, 0, 0, 1.0, follow.alignment)
        self.layer = 0
        self.sprite.name = "simple_sheet"
        self.sprite.ox = 32
        self.sprite.oy = 10
        self.sprite.num_frames = 2
        self.sprite.timer = 0.2
        self.sprite.timer_reset = 0.2
        self._follow = follow
        self.renew: bool = True
        self.solid_vs_map = False

    def update(self, elapsed_time: float, target: Dynamic = None):
        if not self.renew:
            self.kill()

        self.px = self._follow.px
        self.py = self._follow.py

        if self._follow.graphic_state == GraphicState.STANDING:
            elapsed_time = 0
        self.sprite.update(elapsed_time, Direction.SOUTH, GraphicState.STANDING)

        self.renew = False

    def draw_self(self, ox: float, oy: float):
        if self.sprite.name is None or self.sprite.name == "" or self.redundant:
            return

        self.sprite.draw_self(self.px - ox, self.py - oy)
