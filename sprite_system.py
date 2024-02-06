from entity import get_entities_with
from components import Component
import pygame

image_cache = {}


def run_sprite_system(entities, screen):
    filtered_entities = get_entities_with(
        entities, Component.SPRITE, Component.SIZE, Component.POSITION
    )

    for entity in filtered_entities:
        size = entity.get_component(Component.SIZE)
        sprite = entity.get_component(Component.SPRITE)
        position = entity.get_component(Component.POSITION)

        sprite_image = pygame.image.load(sprite.filepath)
        resized_sprite_image = pygame.transform.scale(
            sprite_image, (size.width, size.height)
        )

        screen.blit(resized_sprite_image, (position.x, position.y))
