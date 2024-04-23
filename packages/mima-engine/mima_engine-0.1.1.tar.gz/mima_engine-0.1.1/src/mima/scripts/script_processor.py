from __future__ import annotations

from typing import TYPE_CHECKING, List

from .command import Command

if TYPE_CHECKING:
    from ..engine import MimaEngine


class ScriptProcessor:
    engine: MimaEngine

    def __init__(self):
        self.commands: List[Command] = []
        self.user_control_enabled: bool = True

    def add_command(self, cmd: Command):
        self.commands.append(cmd)

    def process_command(self, elapsed_time: float):
        self.user_control_enabled = len(self.commands) == 0
        if self.commands:
            if not self.commands[0].completed:
                if not self.commands[0].started:
                    self.commands[0].start()
                    self.commands[0].started = True
                else:
                    self.commands[0].update(elapsed_time)
            else:
                self.commands[0].finalize()
                self.commands.pop(0)

    def complete_command(self, force: bool = False):
        if self.commands:
            if self.commands[0].uninterruptible and not force:
                return False
            else:
                self.commands[0].completed = True
                return True
