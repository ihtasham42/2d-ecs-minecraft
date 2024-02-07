from entity import get_entities_with
from input_type import InputType
from components import Component


def run_rigidbody_system(entities):
    filtered_entities = get_entities_with(entities, Component.VELOCITY)

    for entity in filtered_entities:
        position = entity.get_component(Component.POSITION)
        velocity = entity.get_component(Component.VELOCITY)

        velocity.x = 0
        velocity.y = 0

        if entity.has_components(Component.PHYSICS):
            physics = entity.get_component(Component.PHYSICS)
            velocity.y = physics.gravity_velocity

        if entity.has_components(Component.INPUT):
            input_component = entity.get_component(Component.INPUT)
            inputs_listened = input_component.inputs_listened

            if InputType.MOVE_LEFT in inputs_listened:
                velocity.x -= 1
            if InputType.MOVE_RIGHT in inputs_listened:
                velocity.x += 1
            if InputType.JUMP in inputs_listened:
                collision = entity.get_component(Component.COLLISION)
                physics = entity.get_component(Component.PHYSICS)

                if collision and not collision.grounded:
                    continue

                physics.gravity_velocity = -2

                if collision:
                    collision.grounded = False

        position.x += velocity.x
        position.y += velocity.y
