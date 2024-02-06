from entity import get_entities_with
from components import Component


def run_collision_system(entities):
    filtered_entities = get_entities_with(
        entities, Component.COLLISION, Component.POSITION
    )

    for entity in filtered_entities:
        pass
