from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..engine import MimaEngine


class Command:
    engine: MimaEngine

    def __init__(self):
        self.started: bool = False
        self.completed: bool = False
        self.uninterruptible: bool = False

    def start(self):
        pass

    def update(self, elapsed_time: float):
        pass

    def finalize(self):
        pass
