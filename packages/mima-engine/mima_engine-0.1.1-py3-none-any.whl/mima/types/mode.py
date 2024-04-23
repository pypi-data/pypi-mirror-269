from enum import Enum


class Mode(Enum):
    LOADING = 0
    TITLE = 1
    SELECT_GAME = 2
    LOCAL_MAP = 3
    WORLD_MAP = 4
    INVENTORY = 5
    SHOP = 6
    GAME_OVER = 7
    TITLE_SETTINGS = 8
    CONTROLS = 9
    COMBAT = 10
