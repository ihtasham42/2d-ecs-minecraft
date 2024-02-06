import pygame
from constants import SCREEN_SIZE, BLACK, TILE_SIZE
from entity import Entity
from input_type import InputType
from components import (
    Component,
    CollisionComponent,
    PositionComponent,
    VelocityComponent,
    SpriteComponent,
    SizeComponent,
    PhysicsComponent,
    InputComponent,
)
from gravity_system import run_gravity_system
from sprite_system import run_sprite_system
from rigidbody_system import run_rigidbody_system
from input_system import run_input_system
from collision_system import run_collision_system

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

entities = []


def create_player():
    return Entity(
        {
            Component.COLLISION: CollisionComponent(),
            Component.POSITION: PositionComponent(),
            Component.VELOCITY: VelocityComponent(),
            Component.SIZE: SizeComponent(width=16, height=16),
            Component.PHYSICS: PhysicsComponent(),
            Component.SPRITE: SpriteComponent("sprites/entity.png"),
            Component.INPUT: InputComponent(
                {InputType.MOVE_LEFT: pygame.K_a, InputType.MOVE_RIGHT: pygame.K_d}
            ),
        }
    )


def create_tile(x, y):
    return Entity(
        {
            Component.COLLISION: CollisionComponent(),
            Component.POSITION: PositionComponent(x=x, y=y),
            Component.SIZE: SizeComponent(TILE_SIZE, TILE_SIZE),
            Component.SPRITE: SpriteComponent("sprites/entity.png"),
        }
    )


def generate_world(entities):
    for i in range(0, 800, TILE_SIZE):
        tile = create_tile(i, 400)
        entities.append(tile)


def init_game():
    generate_world(entities)

    player = create_player()
    entities.append(player)


init_game()

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    run_input_system(entities)
    run_gravity_system(entities)
    run_rigidbody_system(entities)
    run_collision_system(entities)
    screen.fill(BLACK)
    run_sprite_system(entities, screen)
    pygame.display.update()

pygame.quit()
