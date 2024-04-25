from typing import List

from ...types.alignment import Alignment
from ...types.blend import Blend
from ...util.colors import BLACK, DARK_GREY, VERY_LIGHT_GREY, WHITE
from ...util.constants import TILE_HEIGHT, TILE_WIDTH
from ..dynamic import Dynamic
from ..projectile import Projectile


class Light(Projectile):
    def __init__(
        self,
        follow: Dynamic,
        max_size: int = 64,
        fixed_size: bool = False,
        update_from_target: bool = False,
    ):
        super().__init__(0, 0, 0, 0, 0, Alignment.GOOD)
        self.layer = 1
        self.sprite.name = "light_small"
        self.sprite.width = 48
        self.sprite.height = 48
        self.solid_vs_map = False
        self._follow: Dynamic = follow
        self._fixed_size: bool = fixed_size
        self._update_from_target: bool = update_from_target

        self._timer: float = 0.2
        self._timer_reset: float = 0.2
        self._size_idx: int = 0

        self._sizes: List[int]
        self._max_size: int

        self._prepare_light(max_size)

        # print(f"Light({id(self)}, {self.layer}, {self.sprite.name}, {self.sprite.width, self.sprite.height}, {self._follow}, {self._max_size}, {self._fixed_size}, {self._sizes}, {self._size_idx})")

    def update(self, elapsed_time: float, target: Dynamic = None):
        self.px = (
            self._follow.px + self._follow.sprite.width / TILE_WIDTH * 0.5
        )
        self.py = (
            self._follow.py + self._follow.sprite.height / TILE_HEIGHT * 0.5
        )

        rad = self._follow.light_radius()
        if self._max_size != rad:
            self._prepare_light(rad)

        if self._follow.redundant:
            self.kill()

        if self._fixed_size:
            return

        self._timer -= elapsed_time
        if self._timer <= 0.0:
            self._timer += self._timer_reset
            self._size_idx = (self._size_idx + 1) % len(self._sizes)

        # self.sprite.update(elapsed_time, self.facing_direction, self.graphic_state)

    def draw_self(self, ox: float, oy: float):
        # color = Color(self.color.red, self.color.green, self.color.blue, self.alpha)
        # self.engine.backend.fill_rect(self.px, self.py, WIDTH, HEIGHT, color)
        # self.engine.backend.draw_partial_sprite(
        #     (self.px - ox) * TILE_WIDTH,
        #     (self.py - oy) * TILE_WIDTH,
        #     self.sprite.name,
        #     0,
        #     0,
        #     self.sprite.width,
        #     self.sprite.height,
        #     draw_to_filter=True,
        # )
        # print(f"Drawing light {self} of {self._follow} at {(self.px - ox + self._follow.extra_ox) * TILE_WIDTH,(self.py - oy + self._follow.extra_oy) * TILE_HEIGHT}")
        self.engine.backend.fill_circle(
            (self.px - ox + self._follow.extra_ox) * TILE_WIDTH,
            (self.py - oy + self._follow.extra_oy) * TILE_HEIGHT,
            self._sizes[self._size_idx] * 0.65,  # 0.3125 *
            DARK_GREY,
            blend_mode=Blend.SUB,
            draw_to_filter=True,
        )
        self.engine.backend.fill_circle(
            (self.px - ox + self._follow.extra_ox) * TILE_WIDTH,
            (self.py - oy + self._follow.extra_oy) * TILE_HEIGHT,
            self._sizes[self._size_idx] * 0.5,  # 0.3125 *
            VERY_LIGHT_GREY,
            blend_mode=Blend.SUB,
            draw_to_filter=True,
        )

    def _prepare_light(self, max_size):

        self._max_size = max_size
        self._sizes = [max_size]
        if not self._fixed_size:
            self._sizes.extend(
                [
                    int(max_size * 0.97),
                    int(max_size * 0.94),
                    int(max_size * 0.97),
                ]
            )
