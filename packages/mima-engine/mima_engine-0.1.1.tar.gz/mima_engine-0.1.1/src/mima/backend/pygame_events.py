import logging
import time
from typing import Dict, List, Union

import pygame

from ..types.keys import Key as K
from ..util.constants import AXIS_ACTIVATION, AXIS_DEADZONE, DOUBLE_TAP_SPEED
from ..util.input_defaults import (
    BUTTONS,
    DEFAULT_JOYSTICK_MAP,
    DEFAULT_KEYBOARD_MAP,
)

LOG = logging.getLogger(__name__)

KEYBOARD_EVENTS = [pygame.KEYUP, pygame.KEYDOWN]
JOYSTICK_EVENTS = [
    pygame.JOYDEVICEADDED,
    pygame.JOYDEVICEREMOVED,
    pygame.JOYBUTTONUP,
    pygame.JOYBUTTONDOWN,
    pygame.JOYAXISMOTION,
    pygame.JOYHATMOTION,
]
TOUCH_EVENTS = [pygame.FINGERUP, pygame.FINGERDOWN, pygame.FINGERMOTION]
SDL2_BACKGROUND_EVENTS = [259, 260, 261, 262]


class PygameUserInput:
    """A class that manages keys and key events."""

    def __init__(
        self,
        key_map: Dict[K, List[str]] = DEFAULT_KEYBOARD_MAP,
        joystick_map: Dict[K, List[Union[str, int]]] = DEFAULT_JOYSTICK_MAP,
        platform: str = "PC",
    ):
        self._last_keys: Dict[K, bool] = {}
        self._new_keys: Dict[K, bool] = {but: False for but in BUTTONS}
        self._left_finger_tap_pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self._right_finger_tap_pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self._left_finger_pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self._right_finger_pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self._last_left_tap: float = 0.0
        self._last_right_tap: float = 0.0
        self._last_left_motion: float = 0.0
        self._last_right_motion: float = 0.0
        self._key_map: Dict[K, int] = {}
        self.vd = pygame.Vector2(0, 0)
        self.joystick_input_enabled: bool = True
        if platform == "android":
            # Disable motion control
            # FIXME allow external controllers
            self.joystick_input_enabled = False
        # self._fingers: List[pygame.Vector2] = []

        # if key_map is None:
        #     self._key_map = dict()
        #     for key, vals in RuntimeConfig().keymap.items():
        #         self._key_map[key] = list()
        #         for val in vals:
        #             self._key_map[key].append(getattr(pygame, f"K_{val}"))
        # else:
        for key, vals in key_map.items():
            self._key_map[key] = []
            for val in vals:
                self._key_map[key].append(getattr(pygame, f"K_{val}"))

        # self._key_map = key_map
        # if joystick_map is None:
        #     self._joystick_map = DEFAULT_JOYSTICK_MAP
        # else:
        self._joystick_map = joystick_map

        self.joystick = None
        self._init_joystick()
        self.width = 0
        self.height = 0

    def reset(self):
        self._last_keys = self._new_keys.copy()

    def process(self, event):
        if event.type in KEYBOARD_EVENTS:
            self._handle_keyboard(event)

        if event.type in JOYSTICK_EVENTS and self.joystick_input_enabled:
            self._handle_joystick(event)

        if event.type in TOUCH_EVENTS:
            self._handle_touch(event)

    def _handle_keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            for but, keys in self._key_map.items():
                if event.key in keys:
                    self.set_key(but)

        if event.type == pygame.KEYUP:
            for but, keys in self._key_map.items():
                if event.key in keys:
                    self.unset_key(but)

    def _handle_joystick(self, event):
        if event.type == pygame.JOYDEVICEREMOVED:
            self.joystick = None
            LOG.info("Gamepad unplugged.")

        if event.type == pygame.JOYDEVICEADDED:
            self._init_joystick()
            LOG.info(
                "Detected new gamepad device %s.", self.joystick.get_name()
            )

        if event.type == pygame.JOYBUTTONDOWN:
            if event.joy != 0:
                return
            for but, keys in self._joystick_map.items():
                if event.button in keys:
                    self.set_key(but)

        if event.type == pygame.JOYBUTTONUP:
            if event.joy != 0:
                return
            for but, keys in self._joystick_map.items():
                if event.button in keys:
                    self.unset_key(but)
        if event.type == pygame.JOYHATMOTION:
            if event.joy != 0 or event.hat != 0:
                return

            if event.value[0] == 0:
                self.unset_key(K.LEFT)
                self.unset_key(K.RIGHT)
            elif event.value[0] == -1:
                self.set_key(K.LEFT)
                self.unset_key(K.RIGHT)
            else:
                self.unset_key(K.LEFT)
                self.set_key(K.RIGHT)

            if event.value[1] == 0:
                self.unset_key(K.UP)
                self.unset_key(K.DOWN)
            elif event.value[1] == 1:
                self.set_key(K.UP)
                self.unset_key(K.DOWN)
            else:
                self.unset_key(K.UP)
                self.set_key(K.DOWN)
        if event.type == pygame.JOYAXISMOTION:
            if event.joy != 0:
                return
            if event.axis == 0:
                if event.value < -AXIS_ACTIVATION:
                    self.set_key(K.LEFT)
                    self.unset_key(K.RIGHT)
                elif event.value > AXIS_ACTIVATION:
                    self.unset_key(K.LEFT)
                    self.set_key(K.RIGHT)
                elif abs(event.value) < AXIS_DEADZONE:
                    self.unset_key(K.LEFT)
                    self.unset_key(K.RIGHT)
                else:
                    pass
            if event.axis == 1:
                if event.value < -AXIS_ACTIVATION:
                    self.set_key(K.UP)
                    self.unset_key(K.DOWN)
                elif event.value > AXIS_ACTIVATION:
                    self.unset_key(K.UP)
                    self.set_key(K.DOWN)
                elif abs(event.value) < AXIS_DEADZONE:
                    self.unset_key(K.UP)
                    self.unset_key(K.DOWN)

    def _handle_touch(self, event):
        finger_pos = pygame.Vector2(
            event.x * self.width, event.y * self.height
        )

        if event.type == pygame.FINGERDOWN:
            tap = time.time()
            if event.x < 0.0625 and event.y < 0.1111:
                self.set_key(K.R)
            elif event.x < 0.5:
                # print(f"Left Finger Down: {finger_pos}")
                self._left_finger_tap_pos = finger_pos

                if tap - self._last_left_tap < DOUBLE_TAP_SPEED:
                    # print("Left Double Tap")
                    self.set_key(K.SELECT)
                self._last_left_tap = tap
                #     self._left_finger_pos.x = event.x
                #     self._left_finger_pos.y = event.y

                #     if tap - self._last_left_tap < 0.2:
                #         print("Left Double Tap")
                #         # self._set_key(K.START)
                #         # self._unset_key(K.RIGHT)
                #         # self._unset_key(K.LEFT)
                #         # self._unset_key(K.UP)
                #         # self._unset_key(K.DOWN)
            else:
                self._right_finger_tap_pos = finger_pos

                # if tap - self._last_right_tap < DOUBLE_TAP_SPEED:
                #     # print("Right Double Tap")
                #     self.set_key(K.SELECT)
                self._last_right_tap = tap
                if event.y < 0.3:
                    self.set_key(K.START)
                elif event.x < 0.75:
                    self.set_key(K.B)
                else:
                    self.set_key(K.A)
            #     self._right_finger_pos.x = event.x
            #     self._right_finger_pos.y = event.y
            #     if tap - self._last_right_tap < 0.2:
            #         print("Right Double Tap")

        if event.type == pygame.FINGERUP:
            # release = time.time()
            # finger_dist = (finger_pos - self._left_finger_tap_pos).length()

            if event.x < 0.5:
                # print(f"Left Finger Up: {finger_pos}")
                # if (
                #     SINGLE_TAP_MIN
                #     < release - self._last_left_tap
                #     < SINGLE_TAP_MAX
                # ) and finger_dist < 2.5:
                #     print("Left Single Tap")
                #     # self.set_key(K.START)

                self.unset_key(K.SELECT)
                self.unset_key(K.RIGHT)
                self.unset_key(K.LEFT)
                self.unset_key(K.UP)
                self.unset_key(K.DOWN)
                self.unset_key(K.R)
                # print(
                #     f"Left Finger moved {finger_dist} "
                #     f"({release - self._last_left_tap} s)"
                # )
            else:
                self.unset_key(K.START)
                self.unset_key(K.A)
                self.unset_key(K.B)
                self.unset_key(K.Y)
                self.unset_key(K.X)
                self.unset_key(K.R)
            # print(f"Right Finger Up: {finger_pos}")
            # if (
            #     SINGLE_TAP_MIN
            #     < release - self._last_right_tap
            #     < SINGLE_TAP_MAX
            # ) and finger_dist < 2.5:
            #     print("Right Single Tap")

            # print(
            #     f"Left Finger moved {finger_dist} "
            #     f"({release - self._last_left_tap} s)"
            # )
            #
            # if event.x < 0.5:
            #     if 0.1 < release - self._last_left_tap < 0.25:
            #         print("Left Single Tap")

            #     self._left_finger_pos.x = 0
            #     self._left_finger_pos.y = 0
            #     self._unset_key(K.DOWN)
            #     self._unset_key(K.LEFT)
            #     self._unset_key(K.UP)
            #     self._unset_key(K.RIGHT)
            #     self._unset_key(K.START)
            # else:
            #     if 0.1 < release - self._last_right_tap < 0.25:
            #         print("Right Single Tap")

            #     self._unset_key(K.A)
            #     self._unset_key(K.B)
        if event.type == pygame.FINGERMOTION:
            if event.x < 0.5:
                vd = finger_pos - self._left_finger_tap_pos
                self.unset_key(K.RIGHT)
                self.unset_key(K.LEFT)
                self.unset_key(K.UP)
                self.unset_key(K.DOWN)
                if abs(vd.x) > 2 * abs(vd.y):
                    # Horizontal
                    if vd.x > 5.0:
                        self.set_key(K.RIGHT)
                        self.unset_key(K.LEFT)
                        self.unset_key(K.UP)
                        self.unset_key(K.DOWN)
                    elif vd.x < -5.0:
                        self.set_key(K.LEFT)
                        self.unset_key(K.RIGHT)
                        self.unset_key(K.UP)
                        self.unset_key(K.DOWN)
                elif abs(vd.x) * 2 < abs(vd.y):
                    # Vertical
                    if vd.y > 5.0:
                        self.unset_key(K.RIGHT)
                        self.unset_key(K.LEFT)
                        self.unset_key(K.UP)
                        self.set_key(K.DOWN)
                    elif vd.y < -5.0:
                        self.unset_key(K.LEFT)
                        self.unset_key(K.RIGHT)
                        self.set_key(K.UP)
                        self.unset_key(K.DOWN)
                elif abs(vd.x) * 1.05 > abs(vd.y) or abs(vd.x) < 1.05 * abs(
                    vd.y
                ):
                    if vd.x < 0:
                        self.set_key(K.LEFT)
                    elif vd.x > 0:
                        self.set_key(K.RIGHT)
                    if vd.y < 0:
                        self.set_key(K.UP)
                    elif vd.y > 0:
                        self.set_key(K.DOWN)
                # else:
                #     vd = finger_pos - self._right_finger_tap_pos
                #     self.unset_key(K.A)
                #     self.unset_key(K.B)
                #     self.unset_key(K.Y)
                #     self.unset_key(K.X)
                #     if abs(vd.x) > 2 * abs(vd.y):
                #         # Horizontal
                #         if vd.x > 5.0:
                #             self.set_key(K.Y)
                #         elif vd.x < -5.0:
                #             self.set_key(K.B)
                #     elif abs(vd.x) * 2 < abs(vd.y):
                #         # Vertical
                #         if vd.y > 5.0:
                #             self.set_key(K.A)
                #         elif vd.y < -5.0:
                #             self.set_key(K.X)

                self.vd = vd

    def _handle_mouse(self, event):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if 0 <= event.pos[0] < 16 and 80 <= event.pos[1] < 96:
        #         self._unset_key(K.RIGHT)
        #         self._set_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     elif 0 <= event.pos[0] < 16 and 64 <= event.pos[1] < 80:
        #         self._unset_key(K.RIGHT)
        #         self._set_key(K.LEFT)
        #         self._set_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     elif 16 <= event.pos[0] < 32 and 64 <= event.pos[1] < 80:
        #         self._unset_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._set_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     elif 32 <= event.pos[0] < 48 and 64 <= event.pos[1] < 80:
        #         self._set_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._set_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     elif 32 <= event.pos[0] < 48 and 80 <= event.pos[1] < 96:
        #         self._set_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     elif 32 <= event.pos[0] < 48 and 96 <= event.pos[1] < 112:
        #         self._set_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._set_key(K.DOWN)
        #     elif 16 <= event.pos[0] < 32 and 96 <= event.pos[1] < 112:
        #         self._unset_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._set_key(K.DOWN)
        #     elif 0 <= event.pos[0] < 16 and 96 <= event.pos[1] < 112:
        #         self._unset_key(K.RIGHT)
        #         self._set_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._set_key(K.DOWN)
        #     if 112 <= event.pos[0] < 144 and 0 <= event.pos[1] < 32:
        #         self._set_key(K.START)
        #         self._unset_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._unset_key(K.DOWN)
        #     if 240 <= event.pos[0] < 256 and 80 <= event.pos[1] < 112:
        #         self._set_key(K.A)
        #         self._unset_key(K.RIGHT)
        #         self._unset_key(K.LEFT)
        #         self._unset_key(K.UP)
        #         self._unset_key(K.DOWN)

        # if event.type == pygame.MOUSEBUTTONUP:
        #     self._unset_key(K.DOWN)
        #     self._unset_key(K.LEFT)
        #     self._unset_key(K.UP)
        #     self._unset_key(K.RIGHT)
        #     self._unset_key(K.START)
        #     self._unset_key(K.A)
        pass

    def _init_joystick(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            LOG.info("Initialized Joystick %s.", self.joystick.get_name())

    def set_key(self, button: K):
        self._new_keys[button] = True

    def unset_key(self, button: K):
        self._new_keys[button] = False

    def new_key_press(self, button: K):
        return self._new_keys[button] and not self._last_keys[button]

    def key_held(self, button: K):
        return self._new_keys[button]

    def new_key_release(self, button: K):
        return self._last_keys[button] and not self._new_keys[button]
