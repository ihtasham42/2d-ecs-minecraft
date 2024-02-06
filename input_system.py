from entity import get_entities_with
from components import Component
import pygame


def run_input_system(entities):
    filtered_entities = get_entities_with(entities, Component.INPUT)
    keys_pressed = pygame.key.get_pressed()

    for entity in filtered_entities:
        input_component = entity.get_component(Component.INPUT)
        input_component.inputs_listened = set()

        for input_type, key in input_component.listening_inputs.items():

            if keys_pressed[key]:
                input_component.inputs_listened.add(input_type)
