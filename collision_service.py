from entity import get_entities_with
from components import Component
from dimension import Corner, Position, Axis


def handle_collision(entities, colliding_entity, axis):
    filtered_entities = get_entities_with(
        entities, Component.COLLISION, Component.POSITION, Component.SIZE
    )

    for entity in filtered_entities:
        if colliding_entity.id == entity.id:
            continue

        position = colliding_entity.get_component(Component.POSITION)
        collision = colliding_entity.get_component(Component.COLLISION)
        velocity = colliding_entity.get_component(Component.VELOCITY)

        if axis == Axis.X:
            while is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.TOP_RIGHT],
                get_entity_corners(entity),
            ) or is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.BOTTOM_RIGHT],
                get_entity_corners(entity),
            ):

                position.x -= 1
                velocity.x = 0

            while is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.TOP_LEFT],
                get_entity_corners(entity),
            ) or is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.BOTTOM_LEFT],
                get_entity_corners(entity),
            ):

                position.x += 1
                velocity.x = 0

        if axis == Axis.Y:
            while is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.BOTTOM_LEFT],
                get_entity_corners(entity),
            ) or is_corner_contained_within(
                get_entity_corners(colliding_entity)[Corner.BOTTOM_RIGHT],
                get_entity_corners(entity),
            ):
                position.y -= 1
                collision.grounded = True
                velocity.y = 0

        # for corner in get_entity_corners(entity1).values():
        #     pygame.draw.rect(screen, (255, 0, 0), (corner.x, corner.y, 2, 2))


def is_corner_contained_within(contained_corner, corners):
    return (
        corners[Corner.TOP_LEFT].x < contained_corner.x <= corners[Corner.TOP_RIGHT].x
        and corners[Corner.TOP_LEFT].y
        < contained_corner.y
        <= corners[Corner.BOTTOM_LEFT].y
    )


def get_entity_corners(entity):
    position = entity.get_component(Component.POSITION)
    size = entity.get_component(Component.SIZE)

    return {
        Corner.TOP_LEFT: Position(position.x, position.y),
        Corner.TOP_RIGHT: Position(position.x + size.width, position.y),
        Corner.BOTTOM_LEFT: Position(position.x, position.y + size.height),
        Corner.BOTTOM_RIGHT: Position(
            position.x + size.width, position.y + size.height
        ),
    }
