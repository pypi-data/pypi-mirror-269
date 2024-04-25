from typing import Optional

from ...objects.effects.colorize_screen import ColorizeScreen
from ..command import Command
from ...util.colors import BLACK,Color


class CommandScreenFade(Command):
    def __init__(
        self,
        duration: float = 0.5,
        color: Optional[Color] = None,
        fadein: bool = False,
    ):
        super().__init__()

        self.duration: float = duration
        if color is None:
            color = self.engine.rtc.colors["gb_dark"]

        self.color: Color = color
        self.fadein: bool = fadein
        self.time_so_far: float = 0.0
        self._start: int = 0
        self._end: int = 255
        self._iter: int = 15

        if fadein:
            self._start = 255
            self._end = 0
            self._iter = -self._iter

        # self._alpha = chain([i for i in range(self._start, self._end, self._iter)])

        self._effect = ColorizeScreen()
        # self.duration -= 0.1
        self._effect.alpha = self._start

    def start(self):
        self.engine.scene.add_effect(self._effect)
        self.engine.player.vx = 0
        self.engine.player.vy = 0

    def update(self, elapsed_time: float):
        self.time_so_far += elapsed_time

        progress = self.time_so_far / self.duration

        alpha = progress * 256
        if self.fadein:
            alpha = 255 - alpha

        self._effect.alpha = min(255, max(0, alpha))
        # print(self, self._effect.alpha)

        self.engine.player.vx = 0
        self.engine.player.vy = 0

        if self.time_so_far >= self.duration:
            self._effect.alpha = self._end
            self.completed = True

    def finalize(self):
        self.completed = True
        self._effect.kill()