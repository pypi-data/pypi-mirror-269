from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from .maps.tilemap import Tilemap
from .objects.dynamic import Dynamic
from .types.direction import Direction
from .types.graphic_state import GraphicState, Until
from .types.nature import Nature
from .types.object import ObjectType

if TYPE_CHECKING:
    from .engine import MimaEngine
    from .view.scene import Scene


def check_object_to_map_collision(
    elapsed_time: float,
    obj: Dynamic,
    tilemap: Tilemap,
    new_px: float,
    new_py: float,
) -> Tuple[float, float]:

    left = new_px + obj.hitbox_px
    right = left + obj.hitbox_width
    top = obj.py + obj.hitbox_py
    bottom = top + obj.hitbox_height

    collided_with_map = False
    if obj.solid_vs_map:
        if collision_with_map(tilemap, left, right, top, bottom):
            # On rare occasions, the object might be pushed towards
            # the wall, i.e. old and new pos are equal
            # Decide depending on the decimal part of the position
            # where to push the object
            if new_px == obj.px:
                decimal_dif = new_px - int(new_px)
                if abs(decimal_dif) > 0.5:
                    new_px += 0.0001
                else:
                    new_px -= 0.0001

            # Did the object move from right to left?
            if new_px < obj.px:
                new_px += int(left) + 1.0 - left
            else:
                new_px -= right - int(right) + 0.001

            obj.vx = 0
            collided_with_map = True
            if (
                obj.facing_direction
                in [
                    Direction.WEST,
                    Direction.EAST,
                ]
                and obj.can_push
            ):
                obj.lock_graphic_state(GraphicState.PUSHING, Until.NEXT_UPDATE)

        left = new_px + obj.hitbox_px
        right = left + obj.hitbox_width
        top = new_py + obj.hitbox_py
        bottom = top + obj.hitbox_height

        if collision_with_map(tilemap, left, right, top, bottom):
            # See comment above
            if new_py == obj.py:
                decimal_dif = new_py - int(new_py)
                if abs(decimal_dif) > 0.5:
                    new_py += 0.0001
                else:
                    new_py -= 0.0001

            if new_py < obj.py:
                new_py += int(top) + 1.0 - top
            else:
                new_py -= bottom - int(bottom) + 0.001

            obj.vy = 0
            collided_with_map = True
            if (
                obj.facing_direction
                in [
                    Direction.NORTH,
                    Direction.SOUTH,
                ]
                and obj.can_push
            ):
                obj.lock_graphic_state(GraphicState.PUSHING, Until.NEXT_UPDATE)

        if obj.type == ObjectType.PROJECTILE and collided_with_map:
            obj.kill()

    return new_px, new_py


def collision_with_map(
    tilemap: Tilemap,
    left: float,
    right: float,
    top: float,
    bottom: float,
    layer: int = 0,
) -> bool:
    if tilemap.is_solid(left, top, layer):
        return True
    if tilemap.is_solid(left, bottom, layer):
        return True
    if tilemap.is_solid(right, top, layer):
        return True
    if tilemap.is_solid(right, bottom, layer):
        return True

    return False


def check_object_to_object_collision(
    engine: MimaEngine,
    scene: Scene,
    obj: Dynamic,
    new_px: float,
    new_py: float,
    other: Dynamic,
) -> Tuple[float, float]:
    pass

    obj_left = new_px + obj.hitbox_px
    obj_right = obj_left + obj.hitbox_width
    obj_top = obj.py + obj.hitbox_py
    obj_bottom = obj_top + obj.hitbox_height

    other_left = other.px + other.hitbox_px
    other_right = other_left + other.hitbox_width
    other_top = other.py + other.hitbox_py
    other_bottom = other_top + other.hitbox_height

    if obj.solid_vs_dyn and other.solid_vs_dyn:
        collided_with_dyn = False
        if collision_with_dyn(
            obj_left,
            obj_right,
            obj_top,
            obj_bottom,
            other_left,
            other_right,
            other_top,
            other_bottom,
        ):
            collided_with_dyn = True
            if obj_left < other_left:
                new_px -= obj_right - other_left + 0.001
            else:
                new_px += other_right - obj_left + 0.001

        obj_left = new_px + obj.hitbox_px
        obj_right = obj_left + obj.hitbox_width
        obj_top = new_py + obj.hitbox_py
        obj_bottom = obj_top + obj.hitbox_height

        if collision_with_dyn(
            obj_left,
            obj_right,
            obj_top,
            obj_bottom,
            other_left,
            other_right,
            other_top,
            other_bottom,
        ):
            collided_with_dyn = True
            if obj_top < other_top:
                new_py -= obj_bottom - other_top + 0.001
            else:
                new_py += other_bottom - obj_top + 0.001

        if collided_with_dyn:
            other.on_interaction(obj, Nature.WALK)

    else:
        if obj.type == ObjectType.PLAYER:
            if collision_with_dyn(
                obj_left,
                obj_right,
                obj_top,
                obj_bottom,
                other_left,
                other_right,
                other_top,
                other_bottom,
            ):
                for quest in engine.quests:
                    if quest.on_interaction(
                        scene.dynamics, other, Nature.WALK
                    ):
                        break
                scene.tilemap.on_interaction(other, Nature.WALK)
                other.on_interaction(obj, Nature.WALK)
        else:
            if collision_with_dyn(
                obj_left,
                obj_right,
                obj_top,
                obj_bottom,
                other_left,
                other_right,
                other_top,
                other_bottom,
            ):
                if obj.type == ObjectType.PROJECTILE:
                    if other.alignment != obj.alignment:
                        # We know object is a projectile
                        if other.attackable and not other.invincible:
                            scene.deal_damage(obj, other)
                        else:
                            other.on_interaction(obj, Nature.WALK)
                else:
                    other.on_interaction(obj, Nature.WALK)

    return new_px, new_py


def collision_with_dyn(
    left1: float,
    right1: float,
    top1: float,
    bottom1: float,
    left2: float,
    right2: float,
    top2: float,
    bottom2: float,
) -> bool:
    if left1 < right2 and right1 > left2 and top1 < bottom2 and bottom1 > top2:
        return True

    return False
