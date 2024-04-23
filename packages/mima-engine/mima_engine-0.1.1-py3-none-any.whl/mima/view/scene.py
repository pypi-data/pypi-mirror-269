from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from mima.types.nature import Nature
from mima.util.constants import TILE_HEIGHT, TILE_WIDTH


from ..collision import (
    check_object_to_map_collision,
    check_object_to_object_collision,
)
from ..types.mode import Mode
from ..util.constants import BIG_FONT_HEIGHT, BIG_FONT_WIDTH
from .camera import Camera

if TYPE_CHECKING:
    from mima.objects.loader import ObjectLoader
    from ..engine import MimaEngine
    from ..maps.tilemap import Tilemap
    from ..objects.dynamic import Dynamic
    from ..objects.projectile import Projectile


class Scene:
    engine: MimaEngine

    def __init__(self):
        self.tilemap: Tilemap
        self.dynamics: List[Dynamic] = []
        self.projectiles: List[Projectile] = []
        self.effects: List[Projectile] = []
        self.dialog_to_show: Optional[List[str]] = None
        self.camera: Camera = Camera(0, 0)
        self.loader: ObjectLoader
        self.autosave: bool = False

    def update(self, elapsed_time):
        pass

    def add_dynamic(self, dynamic: Dynamic):
        self.dynamics.append(dynamic)

    def add_projectile(self, projectile: Projectile):
        self.projectiles.append(projectile)

    def add_effect(self, effect: Projectile):
        self.effects.append(effect)

    def change_map(self, map_name: str, spawn_px: float, spawn_py: float):
        pass

    def delete_map_dynamics(self):
        self.dynamics = [obj for obj in self.dynamics if obj.persistent]
        if not self.dynamics:
            self.dynamics = [self.engine.player]
        for p in self.projectiles:
            if not p.persistent:
                p.cancel()
        for e in self.effects:
            if not e.persistent:
                e.cancel()
        self.projectiles = [p for p in self.projectiles if p.persistent]
        self.effects = [e for e in self.effects if e.persistent]

    def show_dialog(self, lines: List[str]):
        self.dialog_to_show = lines
        self.engine.dialog_active = True

    def display_dialog(
        self,
        lines: str,
        px: float,
        py: float,
        background_color=None,
        border_color=None,
    ):
        if background_color is None:
            background_color = self.engine.rtc.colors["gb_dark"]
        if border_color is None:
            border_color = self.engine.rtc.colors["gb_light"]

        max_line_length = 0
        num_lines = len(lines)

        for line in lines:
            if len(line) > max_line_length:
                max_line_length = len(line)

        self.engine.backend.fill_rect(
            px - 1,
            py - 1,
            max_line_length * BIG_FONT_WIDTH + 2,
            num_lines * BIG_FONT_HEIGHT + 2,
            background_color,
        )

        self.engine.backend.draw_rect(
            px - 2,
            py - 2,
            max_line_length * BIG_FONT_WIDTH + 4,
            num_lines * BIG_FONT_HEIGHT + 4,
            border_color,
        )
        # self.apf.draw_line(
        #     Vector2D(pos.x - 2, pos.y - 2),
        #     Vector2D(pos.x - 2, pos.y + num_lines * BIG_FONT_HEIGHT + 1),
        #     border_color,
        # )  # topleft to bottomleft
        # self.apf.draw_line(
        #     Vector2D(pos.x + max_line_length * BIG_FONT_WIDTH + 1, pos.y - 2),
        #     Vector2D(
        #         pos.x + max_line_length * BIG_FONT_WIDTH + 1,
        #         pos.y + num_lines * BIG_FONT_HEIGHT + 1,
        #     ),
        #     border_color,
        # )  # topright to bottomright
        # self.apf.draw_line(
        #     Vector2D(pos.x - 2, pos.y - 2),
        #     Vector2D(pos.x + max_line_length * BIG_FONT_WIDTH + 1, pos.y - 2),
        #     border_color,
        # )  # topleft to topright
        # self.apf.draw_line(
        #     Vector2D(pos.x - 2, pos.y + num_lines * BIG_FONT_HEIGHT + 1),
        #     Vector2D(
        #         pos.x + max_line_length * BIG_FONT_WIDTH + 1,
        #         pos.y + num_lines * BGI_FONT_HEIGHT + 1,
        #     ),
        #     border_color,
        # )  # bottomleft to bottomright

        for idx, line in enumerate(lines):
            self.engine.backend.draw_big_text(
                line, px, py + idx * BIG_FONT_HEIGHT
            )

    def draw_map_and_objects(self):
        # First, background layers of the map
        self.draw_map_layers([-1, 0])

        # Second, dynamics and projectiles
        self.draw_objects_y_sorted()
        # for obj in self.dynamics + self.projectiles:
        #     obj.draw_self(self.camera.ox, self.camera.oy)

        # Third, effects
        for effect in self.effects:
            if effect.layer == 0:
                effect.draw_self(self.camera.ox, self.camera.oy)

        # Fourth, all the foreground layers of the map
        self.draw_map_layers([1, 2])

        # Fifth, there might be foreground effects
        for effect in self.effects:
            if effect.layer >= 1:
                effect.draw_self(self.camera.ox, self.camera.oy)

    def draw_map_layers(self, layers: List[int]):
        for pos in layers:
            self.tilemap.draw_self(
                self.camera.ox,
                self.camera.oy,
                self.camera.visible_tiles_sx,
                self.camera.visible_tiles_sy,
                self.camera.visible_tiles_ex,
                self.camera.visible_tiles_ey,
                pos,
            )

    def draw_objects_y_sorted(self):
        y_sorted = sorted(
            self.dynamics + self.projectiles, key=lambda obj: obj.py
        )
        for layer in range(3):
            for obj in y_sorted:
                if not obj.redundant and obj.visible:
                    if obj.layer == layer:
                        obj.draw_self(self.camera.ox, self.camera.oy)

                        # if self.engine.draw_debug:
                        #     color = CYAN
                        #     if obj.type == ObjectType.PROJECTILE:
                        #         color = RED
                        #     color.alpha = 128
                        #     self.engine.backend.fill_rect(
                        #         (obj.px + obj.hitbox_px - self.camera.ox)
                        #         * TILE_WIDTH,
                        #         (obj.py + obj.hitbox_py - self.camera.oy)
                        #         * TILE_HEIGHT,
                        #         obj.hitbox_width * TILE_WIDTH,
                        #         obj.hitbox_height * TILE_HEIGHT,
                        #         color,
                        #     )
                # elif (
                #     not obj.redundant and self.engine.draw_bounding_rectangles
                # ):
                #     self.engine.backend.fill_rect(
                #         (obj.px + obj.hitbox_px - self.camera.ox)
                #         * obj.sprite.width,
                #         (obj.py + obj.hitbox_py - self.camera.oy)
                #         * obj.sprite.height,
                #         obj.hitbox_width * TILE_WIDTH,
                #         obj.hitbox_height * TILE_HEIGHT,
                #         CYAN,
                #     )

    def delete_redundant_objects(self):
        if self.engine.player.redundant:
            self.engine.scene_stack.append(Mode.GAME_OVER)
            # self.engine.session_seconds = self.engine.total_seconds

        # Find and erase redundant dynamics
        d2rm = [d for d in self.dynamics if d.redundant]
        for dyn in d2rm:
            for quest in self.engine.quests:
                quest.on_interaction(self.dynamics, dyn, Nature.KILLED)
            dyn.on_death()
            self.dynamics.remove(dyn)

        # Find and erase redundant projectiles
        p2rm = [p for p in self.projectiles if p.redundant]
        for pro in p2rm:
            pro.on_death()
            self.projectiles.remove(pro)

        # Find and erase redundant effects
        e2rm = [e for e in self.effects if e.redundant]
        for eff in e2rm:
            eff.on_death()
            self.effects.remove(eff)

        # Find and erase completed quests
        q2rm = [q for q in self.engine.quests if q.completed]
        for quest in q2rm:
            self.engine.quests.remove(quest)

    def handle_user_input(self):
        pass

    def handle_collisions(self, elapsed_time: float):
        screen_width = self.engine.backend.render_width // TILE_WIDTH
        screen_height = self.engine.backend.render_height // TILE_HEIGHT

        # Filter for onscreen/offscreen objects
        dynamics = [
            obj
            for obj in self.dynamics
            if (
                not obj.offscreen_collision_skippable
                or (
                    abs(self.engine.player.px - obj.px) < screen_width
                    and abs(self.engine.player.py - obj.py) < screen_height
                )
            )
        ]
        projectiles = [
            obj
            for obj in self.projectiles
            if (
                not obj.offscreen_collision_skippable
                or (
                    abs(self.engine.player.px - obj.px) < screen_width
                    and abs(self.engine.player.py - obj.py) < screen_height
                )
            )
        ]
        for obj in dynamics + projectiles:
            if obj.onscreen_collision_skippable:
                # self.skipped_collision_checks += 1
                continue

            new_px, new_py = self.update_position(obj, elapsed_time)

            new_px, new_py = check_object_to_map_collision(
                elapsed_time, obj, self.tilemap, new_px, new_py
            )

            if self.check_tile_properties(obj, new_px, new_py):
                # If true, something happened to the object
                continue

            for other in dynamics:
                if other == obj:
                    continue

                new_px, new_py = check_object_to_object_collision(
                    self.engine, self, obj, new_px, new_py, other
                )
            obj.px = new_px
            obj.py = new_py

    def update_dynamics(self, elapsed_time: float):
        screen_width = self.engine.backend.render_width // TILE_WIDTH
        screen_height = self.engine.backend.render_height // TILE_HEIGHT

        for obj in self.dynamics + self.projectiles:
            if (
                obj.update_skippable
                and abs(self.engine.player.px - obj.px) > screen_width
            ):
                continue
            if (
                obj.update_skippable
                and abs(self.engine.player.py - obj.py) > screen_height
            ):
                continue

            obj.vz -= obj.attributes.gravity_vz * elapsed_time
            obj.update(elapsed_time, self.engine.player)

            if obj.gravity:
                obj.pz = obj.pz + obj.vz * elapsed_time
                if obj.pz <= 0.0:
                    obj.pz = 0.0
                    obj.vz = 0.0

    def update_position(self, obj: Dynamic, elapsed_time: float):
        vx, vy = min(1, max(-1, obj.vx)), min(1, max(-1, obj.vy))

        # Diagonal movement
        if obj.vx != 0 and obj.vy != 0:
            vx, vy = vx * 0.707, vy * 0.707

        def calculate(v, real_v):
            if v == 0 and obj.use_friction:
                mod = obj.attributes.friction
            elif v != 0 and obj.use_acceleration:
                mod = obj.attributes.acceleration
            else:
                return v

            dif = v - real_v
            if abs(dif) < 0.01:
                return v
            return real_v + (v - real_v) * mod * elapsed_time

        obj.real_vx = vx if vx == obj.real_vx else calculate(vx, obj.real_vx)
        obj.real_vy = vy if vy == obj.real_vy else calculate(vy, obj.real_vy)

        new_px = (
            obj.px
            + obj.real_vx * obj.speed * obj.attributes.speed_mod * elapsed_time
        )
        new_py = (
            obj.py
            + obj.real_vy * obj.speed * obj.attributes.speed_mod * elapsed_time
        )

        return new_px, new_py
