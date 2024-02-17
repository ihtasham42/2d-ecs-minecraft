from entity import get_entities_with
from input_type import InputType
from components import Component
from collision_service import handle_collision
from dimension import Axis


def run_rigidbody_system(entities):
    filtered_entities = get_entities_with(entities, Component.VELOCITY)

    for entity in filtered_entities:
        position = entity.get_component(Component.POSITION)
        velocity = entity.get_component(Component.VELOCITY)

        x_diff = 0
        y_diff = 0

        if entity.has_components(Component.INPUT):
            input_component = entity.get_component(Component.INPUT)
            inputs_listened = input_component.inputs_listened

            speed = 6

            if InputType.MOVE_LEFT in inputs_listened:
                x_diff -= speed
            if InputType.MOVE_RIGHT in inputs_listened:
                x_diff += speed
            if InputType.MOVE_UP in inputs_listened:
                y_diff -= speed
            if InputType.MOVE_DOWN in inputs_listened:
                y_diff += speed
            if InputType.JUMP in inputs_listened:
                do_jump(entity, velocity)

        x_diff += velocity.x
        y_diff += velocity.y

        if entity.has_components(Component.COLLISION):
            collision = entity.get_component(Component.COLLISION)
            collision.grounded = False

        position.x += x_diff

        if entity.has_components(Component.COLLISION):
            handle_collision(entities, entity, Axis.X)

        position.y += y_diff

        if entity.has_components(Component.COLLISION):
            handle_collision(entities, entity, Axis.Y)


def do_jump(entity, velocity):
    collision = entity.get_component(Component.COLLISION)

    if collision and not collision.grounded:
        return

    velocity.y = -14

    if collision:
        collision.grounded = False
