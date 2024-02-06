from entity import get_entities_with
from components import Component
from constants import GRAVITY, TERMINAL_VELOCITY


def run_gravity_system(entities):
    filtered_entities = get_entities_with(entities, Component.PHYSICS)

    for entity in filtered_entities:
        physics = entity.get_component(Component.PHYSICS)

        physics.gravity_velocity = min(
            physics.gravity_velocity + GRAVITY, TERMINAL_VELOCITY
        )
