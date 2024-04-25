import logging

from ..types.object import ObjectType
from ..util.constants import TILE_HEIGHT, TILE_WIDTH
from .world.container import Container
from .world.floor_switch import FloorSwitch
from .world.gate import Gate
from .world.light_source import LightSource
from .world.logic_gate import LogicGate
from .world.movable import Movable
from .world.oneway import Oneway
from .world.color_switch import ColorSwitch
from .world.color_gate import ColorGate

# from .world.pickup import Pickup
from .world.switch import Switch
from .world.teleport import Teleport

LOG = logging.getLogger(__name__)


class ObjectLoader:
    def __init__(self, object_dispatcher, creature_dispatcher):
        self._base_dispatcher = {
            "color_switch": ColorSwitch.load_from_tiled_object,
            "color_gate": ColorGate.load_from_tiled_object,
            "container": Container.load_from_tiled_object,
            "floor_switch": FloorSwitch.load_from_tiled_object,
            "gate": Gate.load_from_tiled_object,
            "light_source": LightSource.load_from_tiled_object,
            "logic_gate": LogicGate.load_from_tiled_object,
            "movable": Movable.load_from_tiled_object,
            "oneway": Oneway.load_from_tiled_object,
            "switch": Switch.load_from_tiled_object,
            "teleport": Teleport.load_from_tiled_object,
            "creature": self.load_creature_from_tiled_object,
        }
        self._cstm_object_dispatcher = object_dispatcher
        self._cstm_creature_dispatcher = creature_dispatcher
        # self._current_map = None

    def populate_dynamics(self, tilemap, dynamics):
        # self._current_map = tilemap
        for obj in tilemap.objects:
            px = obj.px / TILE_WIDTH
            py = obj.py / TILE_HEIGHT
            width = max(obj.width / TILE_WIDTH, 1.0)
            height = max(obj.height / TILE_HEIGHT, 1.0)

            LOG.debug(
                f"Loading object {obj.name} ({obj.object_id}): {obj.type}) "
                f"at {px, py}."
            )
            if obj.type in self._cstm_object_dispatcher:
                dispatcher = self._cstm_object_dispatcher
            else:
                dispatcher = self._base_dispatcher

            try:
                dynamics.extend(
                    dispatcher[obj.type](obj, px, py, width, height)
                )
            except (KeyError, ValueError):
                LOG.exception(
                    f"Failed to load '{obj.name}' ({obj.object_id}: {obj.type})"
                )
                raise

        # Connect listener IDs to actual listeners
        for dyn in dynamics:
            if dyn.type in [
                ObjectType.SWITCH,
                ObjectType.FLOOR_SWITCH,
                ObjectType.LOGIC_GATE,
            ]:
                for listener_id in dyn.listener_ids:
                    for listener in dynamics:
                        if listener.dyn_id == listener_id:
                            dyn.listeners.append(listener)

                            if listener.type == ObjectType.LOGIC_GATE:
                                if listener.input_id1 == -1:
                                    listener.input_id1 = dyn.dyn_id
                                elif listener.input_id2 == -1:
                                    listener.input_id2 = dyn.dyn_id
                                else:
                                    LOG.warning(
                                        f"Object with ID {dyn.dyn_id} "
                                        "has no free input port at "
                                        f"Logic Gate {listener.dyn_id}"
                                    )

    def load_creature_from_tiled_object(self, obj, px, py, width, height):
        creature_type = obj.get_string("creature_type")
        try:
            return self._cstm_creature_dispatcher[creature_type](
                obj, px, py, width, height
            )
        except (KeyError, ValueError):
            LOG.exception(
                f"Failed to load '{obj.name}' ({obj.object_id}: {obj.type})"
            )
            raise
