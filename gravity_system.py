from entity import get_entities_with
from components import Component
from constants import GRAVITY, TERMINAL_VELOCITY


def run_gravity_system(entities):
    filtered_entities = get_entities_with(
        entities, Component.PHYSICS, Component.VELOCITY
    )

    for entity in filtered_entities:
        velocity = entity.get_component(Component.VELOCITY)

        if velocity.y < TERMINAL_VELOCITY:
            velocity.y += GRAVITY
