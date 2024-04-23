from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Dict

from .backend.pygame_assets import PygameAssets
from .backend.pygame_audio import PygameAudio
from .backend.pygame_backend import PygameBackend
from .backend.pygame_events import PygameUserInput
from .maps.template import Template
from .maps.tilemap import Tilemap
from .objects.animated_sprite import AnimatedSprite
from .objects.creature import Creature
from .objects.dynamic import Dynamic
from .objects.sprite import Sprite
from .scripts import Command, ScriptProcessor
from .states.quest import Quest
from .types.mode import Mode
from .types.gate_color import GateColor
from .usables.item import Item
from .util import RuntimeConfig
from .util.logging import install_trace_logger
from .view.camera import Camera
from .view.scene import Scene

LOG = logging.getLogger(__name__)


class MimaEngine(ABC):
    def __init__(
        self, init_file: str, platform: str = "PC", caption: str = "MimaEngine"
    ):
        self.rtc = RuntimeConfig()
        install_trace_logger()

        self.backend: PygameBackend = PygameBackend(
            self.rtc, init_file, platform
        )

        self._caption: str = caption
        self.seconds_total: float = 0.0
        self.app_fps: float = 0.0
        self.game_fps: float = 0.0
        self.elapsed_time: float = 0.00022
        self._app_time: float = 0.0

        self.mode: Mode = Mode.LOADING
        self.gate_color: GateColor = GateColor.RED
        self.n_gate_colors = 2
        self.script: ScriptProcessor = None
        self.player: Creature
        self.quests: List[Quest] = []
        self._items: Dict[str, Item] = {}

    def construct(
        self,
        width: int,
        height: int,
        pixel_size: int,
        fullscreen: bool = False,
        target_fps: int = 60,
        resizable: bool = False,
    ):
        """Initialize backend and create a window."""
        AnimatedSprite.engine = self
        Camera.engine = self
        Command.engine = self
        Dynamic.engine = self
        PygameBackend.engine = self
        Quest.engine = self
        Scene.engine = self
        ScriptProcessor.engine = self
        Sprite.engine = self
        Template.engine = self
        Tilemap.engine = self
        Item.engine = self

        self.script = ScriptProcessor()
        self.backend.init()
        self.backend.construct(
            width, height, pixel_size, fullscreen, target_fps, resizable
        )
        return True

    def start(self):
        """Start the main loop"""
        app_frames = 0
        game_frames = 0
        app_seconds = 0.0
        game_seconds = 0.0
        app_frames_total = 0
        game_frames_total = 0
        self.seconds_total = 0.0

        if self.on_user_create():
            while self.backend.keep_running():
                self.backend.set_caption(
                    f"{self._caption} ({self.game_fps:.2f}/{self.app_fps:.2f} fps)"
                )
                self.backend.process_events()

                if not self.backend.keep_running():
                    break

                if not self.on_user_update(self.elapsed_time):
                    print("Error in on_user_update")
                    break

                self.backend.update_display()

                self._app_time = self.backend.tick()
                self.elapsed_time = min(self._app_time, 1.0 / 30.0)

                app_seconds += self._app_time
                game_seconds += self.elapsed_time
                app_frames += 1
                game_frames += 1

                if game_seconds >= 1.0:
                    game_frames_total += game_frames
                    self.game_fps = game_frames
                    game_frames = 0
                    game_seconds -= 1.0
                if app_seconds >= 1.0:
                    app_frames_total += app_frames
                    self.seconds_total += app_seconds
                    self.app_fps = app_frames
                    app_frames = 0
                    app_seconds -= 1.0

            print(
                f"App/Game Frames total: {app_frames_total}/{game_frames_total}"
            )
            print(f"Seconds total: {self.seconds_total:.3f}")
            print(
                f"Average App/Game FPS: {app_frames_total/self.seconds_total:.3f}/"
                f"{game_frames_total/self.seconds_total:.3f}"
            )

        self.backend.shutdown()

    @abstractmethod
    def on_user_update(self, elapsed_time: float) -> bool:
        """Update."""
        raise NotImplementedError()

    @abstractmethod
    def on_user_create(self) -> bool:
        raise NotImplementedError()

    def on_user_terminate(self) -> bool:
        self.backend.terminate = True
        return True

    @property
    def assets(self) -> PygameAssets:
        return self.backend.assets

    @property
    def audio(self) -> PygameAudio:
        return self.backend.audio

    @property
    def keys(self) -> PygameUserInput:
        return self.backend.user_input

    def get_map(self, map_name: str):
        return self.backend.assets.get_map(map_name)

    def load_item(self, item: Item):
        LOG.debug(f"Loading item  {item.name}.")
        self._items[item.name] = item

    def get_item(self, item_id: str):
        try:
            return self._items[item_id]
        except KeyError:
            LOG.error(f"Item '{item_id}' is not defined!")
            raise

    def progress_quest(self, quest_name: str, new_state: int):
        for quest in self.quests:
            if quest.name == quest_name:
                quest.state = new_state

    def on_enter_background(self):
        LOG.debug("About to enter background")

    def on_entered_background(self):
        LOG.debug("Entered background")

    def on_enter_foreground(self):
        LOG.debug("About to enter foreground")

    def on_entered_foreground(self):
        LOG.debug("Entered foreground")
