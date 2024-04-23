from typing import List
from ...scripts.command import Command


class CommandShowDialog(Command):
    def __init__(self, lines: List[str]):
        super().__init__()
        self.lines: List[str] = lines

    def start(self):
        self.engine.scene.show_dialog(self.lines)
