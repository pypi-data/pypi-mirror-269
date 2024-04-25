from ..command import Command


class CommandChangeMap(Command):
    def __init__(self, map_name: str, spawn_px: float, spawn_py):
        super().__init__()

        self._map_name: str = map_name
        self._spawn_px: float = spawn_px
        self._spawn_py: float = spawn_py

    def start(self):
        self.engine.scene_stack.pop()
        self.engine.change_map(self._map_name, self._spawn_px, self._spawn_py)
        self.completed = True
