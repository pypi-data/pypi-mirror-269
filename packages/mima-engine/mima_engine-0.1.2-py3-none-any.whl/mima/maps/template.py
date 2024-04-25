from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from ..util.functions import strtobool
from ..util.property import Property

if TYPE_CHECKING:
    from ..engine import MimaEngine


class Template:
    engine: MimaEngine

    def __init__(self, name: str):
        self.name: str = name
        self.properties: Dict[str, Property] = {}

    def get_string(self, key: str, default_val: str = "") -> str:
        if key in self.properties:
            return self.properties[key].value
        else:
            return default_val

    def get_int(self, key: str, default_val: int = 0) -> int:
        if key in self.properties:
            return int(self.properties[key].value)
        else:
            return default_val

    def get_float(self, key: str, default_val: float = 0.0) -> float:
        if key in self.properties:
            return float(self.properties[key].value)
        else:
            return default_val

    def get_bool(self, key: str, default_val: bool = False) -> bool:
        if key in self.properties:
            return bool(strtobool(self.properties[key].value))
        else:
            return default_val
