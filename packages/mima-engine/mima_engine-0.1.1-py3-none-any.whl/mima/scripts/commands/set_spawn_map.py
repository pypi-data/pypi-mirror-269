from ...scripts.command import Command


class CommandSetSavePosition(Command):
    def __init__(self, map_name: str, px: float, py: float):
        self._map_name = map_name
        self._px = px
        self._py = py

    def start(self):
        self.engine.player_state.save_map = self._map_name
        self.engine.player_state.save_px = self._px
        self.engine.player_state.save_py = self._py
        self.completed = True
