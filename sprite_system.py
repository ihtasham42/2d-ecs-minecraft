from entity import get_entities_with
from components import Component
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

image_cache = {}


def run_sprite_system(entities, screen):
    camera_filtered_entities = get_entities_with(
        entities, Component.POSITION, Component.CAMERA
    )

    if len(camera_filtered_entities) == 0:
        return

    camera_entity = camera_filtered_entities[0]
    camera_position = camera_entity.get_component(Component.POSITION)
    camera_size = camera_entity.get_component(Component.SIZE)

    camera_offset_x = SCREEN_WIDTH // 2 - camera_size.width // 2
    camera_offset_y = SCREEN_HEIGHT // 2 - camera_size.height // 2

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

        fx = position.x - camera_position.x + camera_offset_x
        fy = position.y - camera_position.y + camera_offset_y

        screen.blit(resized_sprite_image, (fx, fy))
