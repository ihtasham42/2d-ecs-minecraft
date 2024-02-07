from entity import get_entities_with
from components import Component
from enum import Enum


class Corner(Enum):
    TOP_LEFT = "top left"
    TOP_RIGHT = "top right"
    BOTTOM_LEFT = "bottom left"
    BOTTOM_RIGHT = "bottom right"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def run_collision_system(entities):
    filtered_entities = get_entities_with(
        entities, Component.COLLISION, Component.POSITION, Component.SIZE
    )

    for entity1 in filtered_entities:
        for entity2 in filtered_entities:
            if not entity1.has_components(Component.VELOCITY):
                continue

            if entity1.id == entity2.id:
                continue

            position = entity1.get_component(Component.POSITION)
            collision = entity1.get_component(Component.COLLISION)

            while is_corner_contained_within(
                get_entity_corners(entity1)[Corner.BOTTOM_LEFT],
                get_entity_corners(entity2),
            ) or is_corner_contained_within(
                get_entity_corners(entity1)[Corner.BOTTOM_RIGHT],
                get_entity_corners(entity2),
            ):

                position.y -= 1
                collision.grounded = True


def is_corner_contained_within(contained_corner, corners):
    return (
        corners[Corner.TOP_LEFT].x <= contained_corner.x <= corners[Corner.TOP_RIGHT].x
        and corners[Corner.TOP_LEFT].y
        <= contained_corner.y
        <= corners[Corner.BOTTOM_LEFT].y
    )


def are_entities_colliding(entity1, entity2):
    pass


def get_entity_corners(entity):
    position = entity.get_component(Component.POSITION)
    size = entity.get_component(Component.SIZE)

    return {
        Corner.TOP_LEFT: Position(position.x, position.y),
        Corner.TOP_RIGHT: Position(position.x + size.width, position.y),
        Corner.BOTTOM_LEFT: Position(position.x, position.y + size.height),
        Corner.BOTTOM_RIGHT: Position(
            position.x + size.width, position.x + size.height
        ),
    }
