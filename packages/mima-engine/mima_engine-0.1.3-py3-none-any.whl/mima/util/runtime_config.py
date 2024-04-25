import configparser
import os
from copy import deepcopy
from typing import Any, Dict, Optional

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
    "colors": {},
    "color_remaps": {},
    "flags": {},
}


class RuntimeConfig:
    def __init__(
        self,
        config_path: str = "",
        default_config: Optional[Dict[str, Any]] = None,
    ):
        if default_config is None:
            default_config = DEFAULT_CONFIG

        self._loaded: Dict[str, Any] = deepcopy(default_config)
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

        default_colors = {}
        for color_name, color in self._loaded["colors"].items():
            default_colors[f"{color_name}_default"] = color
            self._loaded["colors"][color_name] = config["colors"][color_name]
        self._loaded["colors"].update(default_colors)

        for flag in self._loaded["flags"]:
            self._loaded["flags"][flag] = config["flags"][flag]

    def _write_config(self, config: configparser.ConfigParser):
        config["keymap"] = {}
        config["colors"] = {}
        config["flags"] = {}
        for key, mapping in self._loaded["keymap"].items():
            config["keymap"][key.lower()] = mapping

        for color_name, color in self._loaded["colors"].items():
            if color_name.endswith("_default"):
                continue
            config["colors"][color_name] = color

        for flag_name, flag in self._loaded["flags"].items():
            config["flags"][flag_name] = flag

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
            for flag, value in self._loaded["flags"].items():
                self._converted["flags"][flag] = strtobool(value)

            return self._converted["flags"]
