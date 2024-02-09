from enum import Enum


class Corner(Enum):
    TOP_LEFT = "top left"
    TOP_RIGHT = "top right"
    BOTTOM_LEFT = "bottom left"
    BOTTOM_RIGHT = "bottom right"


class Axis(Enum):
    X = "x"
    Y = "y"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
