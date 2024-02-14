import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LIGHT_BLUE, TILE_SIZE
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
    CameraComponent,
)
from gravity_system import run_gravity_system
from sprite_system import run_sprite_system
from rigidbody_system import run_rigidbody_system
from input_system import run_input_system
from chunk_system import run_chunk_system

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

entities = []


def create_flying_player():
    return Entity(
        {
            Component.POSITION: PositionComponent(),
            Component.VELOCITY: VelocityComponent(),
            Component.SIZE: SizeComponent(width=TILE_SIZE, height=TILE_SIZE),
            Component.SPRITE: SpriteComponent("sprites/entity.png"),
            Component.INPUT: InputComponent(
                {
                    InputType.MOVE_LEFT: pygame.K_a,
                    InputType.MOVE_RIGHT: pygame.K_d,
                    InputType.MOVE_DOWN: pygame.K_s,
                    InputType.MOVE_UP: pygame.K_w,
                }
            ),
            Component.CAMERA: CameraComponent(),
        }
    )


def create_player():
    return Entity(
        {
            Component.COLLISION: CollisionComponent(),
            Component.POSITION: PositionComponent(),
            Component.VELOCITY: VelocityComponent(),
            Component.SIZE: SizeComponent(width=TILE_SIZE, height=TILE_SIZE),
            Component.PHYSICS: PhysicsComponent(),
            Component.SPRITE: SpriteComponent("sprites/entity.png"),
            Component.INPUT: InputComponent(
                {
                    InputType.MOVE_LEFT: pygame.K_a,
                    InputType.MOVE_RIGHT: pygame.K_d,
                    InputType.JUMP: pygame.K_w,
                }
            ),
            Component.CAMERA: CameraComponent(),
        }
    )


# def generate_world(entities):
#     for i in range(0, 800, TILE_SIZE):
#         tile = create_tile(i, 400)
#         entities.append(tile)

#     for i in range(320, 1200, TILE_SIZE):
#         tile = create_tile(i, 400 - TILE_SIZE)
#         entities.append(tile)


def init_game():
    # generate_world(entities)

    player = create_flying_player()
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
    run_chunk_system(entities)
    screen.fill(LIGHT_BLUE)
    run_sprite_system(entities, screen)
    pygame.display.update()

pygame.quit()
