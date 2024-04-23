import configparser
import os
from copy import deepcopy
from typing import Any, Dict

from ..types.keys import Key as K
from .colors import Color
from .functions import strtobool

DEFAULT_CONFIG = {
    "keymap": {
        "UP": "w",
        "DOWN": "s",
        "LEFT": "a",
        "RIGHT": "d",
        "A": "k",
        "B": "h",
        "X": "l",
        "Y": "j",
        "L": "o",
        "R": "c",
        "START": "i",
        "SELECT": "t",
    },
    "colors": {
        "gb_dark": "42,0,0",
        "gb_medium_dark": "91,86,95",
        "gb_medium_light": "186,191,181",
        "gb_light": "255,255,241",
    },
    "flags": {"use_color": "false"},
}


class RuntimeConfig:
    def __init__(self, config_path: str = ""):
        self._loaded: Dict[str, Any] = deepcopy(DEFAULT_CONFIG)
        self._converted: Dict[str, Any] = {}

        if not config_path:
            config_path = os.path.abspath(
                os.path.join(os.getcwd(), "avenight.ini")
            )

        self._config_path = config_path
        config = configparser.ConfigParser()

        if os.path.exists(config_path):
            config.read(config_path)

            if config.sections():
                self._read_config(config)

            else:
                self._write_config(config)

        else:
            self._write_config(config)

    def _read_config(self, config: configparser.ConfigParser):
        for key, mapping in config["keymap"].items():
            vals = mapping.strip().split(",")
            self._loaded["keymap"][key.upper()] = vals

        self._loaded["colors"]["gb_dark"] = config["colors"]["gb_dark"]
        self._loaded["colors"]["gb_medium_dark"] = config["colors"][
            "gb_medium_dark"
        ]
        self._loaded["colors"]["gb_medium_light"] = config["colors"][
            "gb_medium_light"
        ]
        self._loaded["colors"]["gb_light"] = config["colors"]["gb_light"]

        self._loaded["flags"]["use_color"] = config["flags"]["use_color"]

    def _write_config(self, config: configparser.ConfigParser):
        config["keymap"] = {}
        config["colors"] = {}
        config["flags"] = {}
        for key, mapping in self._loaded["keymap"].items():
            config["keymap"][key.lower()] = mapping

        config["colors"]["gb_dark"] = self._loaded["colors"]["gb_dark"]
        config["colors"]["gb_medium_dark"] = self._loaded["colors"][
            "gb_medium_dark"
        ]
        config["colors"]["gb_medium_light"] = self._loaded["colors"][
            "gb_medium_light"
        ]
        config["colors"]["gb_light"] = self._loaded["colors"]["gb_light"]

        config["flags"]["use_color"] = self._loaded["flags"]["use_color"]

        with open(self._config_path, "w") as cfg_file:
            config.write(cfg_file)

    @property
    def keymap(self):
        if "keymap" in self._converted:
            return self._converted["keymap"]
        else:
            self._converted["keymap"] = {}
            for but in K:
                self._converted["keymap"][but] = self._loaded["keymap"][
                    but.name
                ]

        return self._converted["keymap"]

    @property
    def colors(self) -> Dict[str, Color]:
        if "colors" in self._converted:
            return self._converted["colors"]
        else:
            self._converted["colors"] = {}
            for key, val in self._loaded["colors"].items():
                self._converted["colors"][key] = Color(
                    *[int(p) for p in val.strip().split(",")]
                )

            return self._converted["colors"]

    @property
    def flags(self) -> Dict[str, bool]:
        if "flags" in self._converted:
            return self._converted["flags"]
        else:
            self._converted["flags"] = {}
            self._converted["flags"]["use_color"] = strtobool(
                self._loaded["flags"]["use_color"]
            )

            return self._converted["flags"]
