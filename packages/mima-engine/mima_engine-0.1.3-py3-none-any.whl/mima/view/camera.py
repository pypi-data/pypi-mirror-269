from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..util.constants import TILE_HEIGHT, TILE_WIDTH

if TYPE_CHECKING:
    from ..maps.tilemap import Tilemap
    from ..objects.dynamic import Dynamic


class Camera:
    def __init__(
        self,
        visible_tiles_sx: int = 0,
        visible_tiles_sy: int = 0,
        visible_tiles_ex: Optional[int] = None,
        visible_tiles_ey: Optional[int] = None,
    ):
        self.visible_tiles_sx: int = visible_tiles_sx
        self.visible_tiles_sy: int = visible_tiles_sy
        self.visible_tiles_ex: int = visible_tiles_ex
        self.visible_tiles_ey: int = visible_tiles_ey

        if self.visible_tiles_ex is None:
            self.visible_tiles_ex = (
                self.engine.backend.render_width / TILE_WIDTH
                - self.visible_tiles_sx
            )

        if self.visible_tiles_ey is None:
            self.visible_tiles_ey = (
                self.engine.backend.render_height / TILE_HEIGHT
                - self.visible_tiles_sy
            )

    def update(self, target: Dynamic, tilemap: Tilemap):

        # Calculate x offset
        self.ox = target.px - self.visible_tiles_ex / 2.0
        self.ox = min(tilemap.width - self.visible_tiles_ex, max(0, self.ox))
        if tilemap.width < self.visible_tiles_ex:
            self.ox += (self.visible_tiles_ex - tilemap.width) / 2.0
        self.ox -= self.visible_tiles_sx

        # Calculate y offset
        self.oy = target.py - self.visible_tiles_ey / 2.0
        self.oy = min(tilemap.height - self.visible_tiles_ey, max(0, self.oy))
        if tilemap.height < self.visible_tiles_ey:
            self.oy += (self.visible_tiles_ey - tilemap.height) / 2.0
        self.oy -= self.visible_tiles_sy
