from enum import Enum


class Component(Enum):
    POSITION = "position"
    VELOCITY = "velocity"
    SIZE = "size"
    COLLISION = "collision"
    WEIGHT = "weight"
    SPRITE = "sprite"
    PHYSICS = "physics"
    INPUT = "input"
    CAMERA = "camera"
    TILE = "tile"


class PositionComponent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class VelocityComponent:
    def __init__(self, x=0, y=0):
        self.x = 0
        self.y = 0


class SizeComponent:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height


class CollisionComponent:
    def __init__(self):
        self.grounded = False


class PhysicsComponent:
    def __init__(self):
        self.gravity_velocity = 0


class WeightComponent:
    def __init__(self, weight=10):
        self.weight = weight


class SpriteComponent:
    def __init__(self, filepath):
        self.filepath = filepath


class InputComponent:
    def __init__(self, listening_inputs):
        self.listening_inputs = listening_inputs
        self.inputs_listened = set()


class CameraComponent:
    pass


class TileComponent:
    pass
