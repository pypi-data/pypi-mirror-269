from ..types.keys import Key as K

BUTTONS = [
    K.UP,
    K.DOWN,
    K.LEFT,
    K.RIGHT,
    K.START,
    K.SELECT,
    K.A,
    K.B,
    K.X,
    K.Y,
    K.L,
    K.R,
]


# Keyboard
# The arrow keys need to be uppercase, other keys are lowercase
DEFAULT_KEYBOARD_MAP = {
    K.UP: ["w", "UP"],
    K.DOWN: ["s", "DOWN"],
    K.LEFT: ["a", "LEFT"],
    K.RIGHT: ["d", "RIGHT"],
    K.START: ["i"],
    K.SELECT: ["t"],
    K.A: ["k"],
    K.B: ["h"],
    K.X: ["l"],
    K.Y: ["j"],
    K.L: ["o"],
    K.R: ["c"],
}

DEFAULT_JOYSTICK_MAP = {
    K.UP: ["up"],
    K.DOWN: ["down"],
    K.LEFT: ["left"],
    K.RIGHT: ["right"],
    K.START: [7],
    K.SELECT: [6],
    K.A: [0],
    K.B: [1],
    K.X: [3],
    K.Y: [2],
    K.L: [4],
    K.R: [5],
}
