from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame

from ..types.blend import Blend
from ..util.colors import BLACK, WHITE, Color
from ..util.constants import (
    BIG_FONT_HEIGHT,
    BIG_FONT_NAME,
    BIG_FONT_WIDTH,
    SMALL_FONT_HEIGHT,
    SMALL_FONT_NAME,
    SMALL_FONT_WIDTH,
)
from .pygame_assets import PygameAssets
from .pygame_audio import PygameAudio
from .pygame_events import SDL2_BACKGROUND_EVENTS, PygameUserInput

if TYPE_CHECKING:
    from ..engine import MimaEngine
    from ..util import RuntimeConfig

LOG = logging.getLogger(__name__)


class PygameBackend:
    engine: MimaEngine

    def __init__(self, rtc: RuntimeConfig, init_file: str, platform: str):
        self.rtc = rtc
        self.init_file: str = init_file
        self.platform: str = platform
        self.icon_path: str = ""
        self.splash_path: str = ""

        self.render_width: int
        self.render_height: int
        self.pixel_size: int
        self.display_width: int
        self.display_height: int
        self.target_fps: int

        self.clock: pygame.time.Clock
        self.manual_scale: bool = False
        self.terminate: bool = False
        self.user_input: PygameUserInput
        self.assets: PygameAssets
        self.audio: PygameAudio

        self.display: pygame.Surface
        self._screen: pygame.Surface
        self._filter: pygame.Surface
        self._filter_color: Color = BLACK
        self._filter_blend: Blend = Blend.DEFAULT
        self._last_sprite_name: str = ""
        self._last_sprite: pygame.Surface

    def init(self):
        LOG.info("Initializing pygame backend.")
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        self.clock = pygame.time.Clock()
        self.user_input = PygameUserInput(platform=self.platform)
        self.assets = PygameAssets(self.rtc, self.init_file)
        self.audio = PygameAudio(self.assets)

    def construct(
        self,
        width: int,
        height: int,
        pixel_size: int,
        fullscreen: bool = False,
        target_fps: int = 60,
        resizeable: bool = False,
    ):
        LOG.info("Constructing window.")
        self.render_width, self.display_width = width, width
        self.render_height, self.display_height = height, height
        self.pixel_size = pixel_size
        self.target_fps = target_fps

        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if fullscreen:
            flags = flags | pygame.FULLSCREEN | pygame.SCALED
            self.pixel_size = -1  # Calculate later
        elif pixel_size == 0:
            flags = flags | pygame.SCALED
            self.pixel_size = -1  # Calculate later
        else:
            self.display_width = self.render_width * self.pixel_size
            self.display_height = self.render_height * self.pixel_size

        self._screen = pygame.display.set_mode(
            (self.display_width, self.display_height), flags
        )

        if pixel_size > 1:
            self.manual_scale = True
            self.display = pygame.Surface(
                (self.render_width, self.render_height)
            )
        else:
            self.display = self._screen

        if self.platform == "PC":
            if self.icon_path:
                icon = pygame.image.load(self.icon_path).convert_alpha()
                pygame.display.set_icon(icon)

            if self.splash_path:
                splash_screen = pygame.image.load(
                    self.splash_path
                ).convert_alpha()
                self.display.blit(splash_screen, (0, 0))
                pygame.display.flip()

        self.user_input.width = self.render_width
        self.user_input.height = self.render_height
        self.assets.load()
        # self.assets.load_items()

    def clear(self, color: Color = Color(0, 0, 0)):
        self.display.fill(color.getRGBA())
        self._filter = pygame.Surface((self.render_width, self.render_height))
        self._filter.fill(self._filter_color.getRGBA())

    def configure_filter(
        self, color: Color = BLACK, blend_mode: Blend = Blend.DEFAULT
    ):
        self._filter_color = color
        self._filter_blend = blend_mode

    def apply_filter(self):
        if self._filter_blend != Blend.DEFAULT:
            self.display.blit(
                self._filter,
                pygame.Vector2(0, 0),
                special_flags=blend_to_pygame_flag(self._filter_blend),
            )

    def draw_partial_sprite(
        self,
        px: float,
        py: float,
        sprite_name: float,
        sx: float,
        sy: float,
        width: float,
        height: float,
        blend_mode: Blend = Blend.DEFAULT,
        draw_to_filter: bool = False,
    ):
        if sprite_name:
            if draw_to_filter:
                display = self._filter
            else:
                display = self.display

            if sprite_name != self._last_sprite_name:
                self._last_sprite_name = sprite_name
                self._last_sprite = self.assets.get_sprite(sprite_name)

            sprite = self._last_sprite
            if sprite is not None:
                try:
                    display.blit(
                        sprite,
                        pygame.Vector2(px, py),
                        pygame.Rect(sx, sy, width, height),
                        special_flags=0
                        if blend_mode == Blend.DEFAULT
                        else blend_to_pygame_flag(blend_mode),
                    )
                except Exception as e:
                    print(
                        f"Exception drawing sprite {sprite_name}: {px}, {py}, {sx}, {sy}, {width}, {height}"
                    )
                    raise e
        # else:
        #     print(f"Draw sprite {sprite_name} at {(px, py)}.")

    def draw_line(
        self, sx: float, sy: float, ex: float, ey: float, color: Color
    ):
        pygame.draw.line(self.display, color.getRGBA(), (sx, sy), (ex, ey))

    def fill_circle(
        self,
        px: float,
        py: float,
        radius: float,
        color: Color,
        blend_mode: Blend = Blend.DEFAULT,
        draw_to_filter: bool = False,
    ):
        if draw_to_filter:
            display = self._filter
        else:
            display = self.display

        if blend_mode == Blend.DEFAULT:
            pygame.draw.circle(display, color.getRGBA(), (px, py), radius)
        else:
            surf = pygame.Surface((radius * 2, radius * 2))
            surf.fill((0, 0, 0))
            pygame.draw.circle(surf, color.getRGBA(), (radius, radius), radius)
            rect = surf.get_rect(center=(px, py))
            display.blit(
                surf,
                rect,
                special_flags=blend_to_pygame_flag(blend_mode),
            )

    def draw_circle(self, px: float, py: float, radius: float, color: Color):
        pygame.draw.circle(
            self.display, color.getRGBA(), (px, py), radius, width=1
        )

    def fill_rect(
        self,
        px: float,
        py: float,
        width: float,
        height: float,
        color: Color,
        draw_to_filter: bool = False,
    ):
        r, g, b, a = color.getRGBA()
        if draw_to_filter:
            display = self._filter
        else:
            display = self.display

        if a < 255:
            surf = pygame.Surface((width, height))
            surf.set_alpha(a)
            surf.fill((r, g, b))
            display.blit(surf, (px, py))
        else:
            pygame.draw.rect(
                display,
                (r, g, b),
                pygame.Rect(px, py, width, height),
            )

    def draw_rect(
        self,
        px: float,
        py: float,
        width: float,
        height: float,
        color: Color,
        line_width: int = 1,
    ):
        line_width = max(1, line_width)
        pygame.draw.rect(
            self.display,
            color.getRGB(),
            pygame.Rect(px, py, width, height),
            width=line_width,
        )

    def draw_big_text(
        self, text: str, px: float, py: float, color: Color = WHITE
    ):
        self.draw_text(
            text,
            px,
            py,
            BIG_FONT_NAME,
            BIG_FONT_WIDTH,
            BIG_FONT_HEIGHT,
            color,
        )

    def draw_small_text(
        self, text: str, px: float, py: float, color: Color = WHITE
    ):
        self.draw_text(
            text,
            px,
            py,
            SMALL_FONT_NAME,
            SMALL_FONT_WIDTH,
            SMALL_FONT_HEIGHT,
            color,
        )

    def draw_text(
        self,
        text: str,
        px: float,
        py: float,
        font_name: str,
        font_width: int,
        font_height: int,
        color: Color = WHITE,
    ):
        if color != WHITE:
            old_sprite = self.assets.get_sprite(font_name)
            new_sprite = old_sprite.copy()
            new_sprite.fill(
                color.getRGBA(), special_flags=pygame.BLEND_RGBA_MIN
            )
            font_name = f"{font_name}_{color.short_name()}"
            self.assets.new_sprite(font_name, new_sprite)

        idx = 0
        for c in text:
            sx = ((ord(c) - 32) % 16) * font_width
            sy = ((ord(c) - 32) // 16) * font_height
            self.draw_partial_sprite(
                px + idx * font_width,
                py,
                font_name,
                sx,
                sy,
                font_width,
                font_height,
            )
            idx += 1

    def draw_pixel(self, px: float, py: float, color: Color):
        self.display.set_at((int(px), int(py)), color.getRGB())

    def set_caption(self, text: str):
        pygame.display.set_caption(text)

    def keep_running(self) -> bool:
        return not self.terminate

    def process_events(self):
        self.user_input.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.on_user_terminate()
                    continue
            if event.type in SDL2_BACKGROUND_EVENTS:
                self._handle_background(event)
                continue

            self.user_input.process(event)

    def update_display(self):
        if self.manual_scale:
            self._screen.blit(
                pygame.transform.scale(
                    self.display, (self.display_width, self.display_height)
                ),
                (0, 0),
            )

        pygame.display.flip()

    def tick(self) -> float:
        return self.clock.tick(self.target_fps) / 1000.0

    def on_user_terminate(self):
        self.engine.on_user_terminate()

    def shutdown(self):
        pygame.mixer.quit()
        pygame.quit()

    def _handle_background(self, event):
        if event.type == 259:
            self.engine.on_enter_background()
        elif event.type == 260:
            self.engine.on_entered_background()
        elif event.type == 261:
            self.engine.on_enter_foreground()
        else:
            self.engine.on_entered_foreground()

    @property
    def data_path(self):
        return self.assets.data_path


def blend_to_pygame_flag(blend_mode: Blend):
    if blend_mode == Blend.DEFAULT:
        return 0
    elif blend_mode == Blend.ADD:
        return pygame.BLEND_RGBA_ADD
    elif blend_mode == Blend.SUB:
        return pygame.BLEND_RGBA_SUB
    elif blend_mode == Blend.MULT:
        return pygame.BLEND_RGBA_MULT
    else:
        return 0
