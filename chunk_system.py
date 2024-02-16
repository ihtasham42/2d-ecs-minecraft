from entity import get_entities_with
from components import Component
from entity import Entity
from constants import (
    CHUNK_WIDTH,
    CHUNK_HEIGHT,
    CHUNK_RANGE,
    TILE_SIZE,
)
from components import (
    Component,
    CollisionComponent,
    PositionComponent,
    SpriteComponent,
    SizeComponent,
    TileComponent,
)

import json
import os
import random
import noise

last_current_chunk_x = -100
last_current_chunk_y = -100
done = False

chunk_index = random.randint(0, 10000000)

CHUNKS_DIR = f"chunks/{chunk_index}"


def run_chunk_system(entities):
    camera_filtered_entities = get_entities_with(
        entities, Component.POSITION, Component.CAMERA
    )

    if len(camera_filtered_entities) == 0:
        return

    camera_entity = camera_filtered_entities[0]
    camera_position = camera_entity.get_component(Component.POSITION)

    current_chunk_x = int((camera_position.x) // (CHUNK_WIDTH * TILE_SIZE))
    current_chunk_y = int((camera_position.y) // (CHUNK_HEIGHT * TILE_SIZE))

    global last_current_chunk_x, last_current_chunk_y

    if (
        current_chunk_x != last_current_chunk_x
        or current_chunk_y != last_current_chunk_y
    ):
        chunks_loaded = set(
            get_chunks_in_range(last_current_chunk_x, last_current_chunk_y)
        )

        chunks_to_load = set(get_chunks_in_range(current_chunk_x, current_chunk_y))

        chunks_to_unload = chunks_loaded - chunks_to_load

        unloaded_chunks_to_load = chunks_to_load - chunks_loaded

        tile_entities = get_entities_with(entities, Component.TILE)

        unload_chunk(entities, tile_entities, chunks_to_unload)
        load_chunk(entities, unloaded_chunks_to_load)

        last_current_chunk_x = current_chunk_x
        last_current_chunk_y = current_chunk_y


def generate_chunk(entities, chunk_filename, chunk_x, chunk_y):
    chunk_data = {}

    for tile_x in range(
        chunk_x * CHUNK_WIDTH * TILE_SIZE,
        (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE,
        TILE_SIZE,
    ):
        for tile_y in range(
            chunk_y * CHUNK_HEIGHT * TILE_SIZE,
            (chunk_y + 1) * CHUNK_HEIGHT * TILE_SIZE,
            TILE_SIZE,
        ):
            height = int(noise.pnoise1(tile_x * 0.003, 2) * TILE_SIZE * 5)
            chance = noise.pnoise2(tile_x * 0.005, tile_y * 0.005)

            if tile_y > height and chance < 0.2:
                entity = create_tile(tile_x, tile_y)
                entities.append(entity)

                tile_key = f"{tile_x}_{tile_y}"

                chunk_data[tile_key] = {"x": tile_x, "y": tile_y}

    with open(chunk_filename, "w") as file:
        json.dump(chunk_data, file)


def load_chunk_from_file(entities, chunk_filename):
    with open(chunk_filename, "r") as file:
        chunk_data = json.load(file)

        for tile_data in chunk_data.values():
            entity = create_tile(tile_data["x"], tile_data["y"])
            entities.append(entity)


def load_chunk(entities, unloaded_chunks_to_load):
    os.makedirs(CHUNKS_DIR, exist_ok=True)

    for chunk_x, chunk_y in unloaded_chunks_to_load:
        chunk_key = f"{chunk_x}_{chunk_y}"
        chunk_filename = f"{CHUNKS_DIR}/{chunk_key}.json"

        if os.path.exists(chunk_filename):  # Check if chunk_key exists
            load_chunk_from_file(entities, chunk_filename)
        else:
            generate_chunk(entities, chunk_filename, chunk_x, chunk_y)


def unload_chunk(entities, tile_entities, chunks_to_unload):
    tile_ids_to_remove = []

    for tile in tile_entities:
        tile_position = tile.get_component(Component.POSITION)

        for chunk_x, chunk_y in chunks_to_unload:
            chunk_key = str(chunk_x) + "_" + str(chunk_y)

            if is_tile_in_chunk(tile_position, chunk_x, chunk_y):
                tile_ids_to_remove.append(tile.id)

    filtered_entities = [
        entity for entity in entities if entity.id not in tile_ids_to_remove
    ]

    entities.clear()
    entities.extend(filtered_entities)


def is_tile_in_chunk(tile_position, chunk_x, chunk_y):
    return (
        chunk_x * CHUNK_WIDTH * TILE_SIZE
        <= tile_position.x
        < (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE
        and chunk_y * CHUNK_HEIGHT * TILE_SIZE
        <= tile_position.y
        < (chunk_y + 1) * CHUNK_HEIGHT * TILE_SIZE
    )


def create_tile(x, y):
    return Entity(
        {
            Component.COLLISION: CollisionComponent(),
            Component.POSITION: PositionComponent(x=x, y=y),
            Component.SIZE: SizeComponent(TILE_SIZE, TILE_SIZE),
            Component.SPRITE: SpriteComponent("sprites/block.png"),
            Component.TILE: TileComponent(),
        }
    )


def get_chunks_in_range(chunk_x, chunk_y):
    chunks_in_range = []

    for x in range(chunk_x - CHUNK_RANGE, chunk_x + CHUNK_RANGE + 1):
        for y in range(chunk_y - CHUNK_RANGE, chunk_y + CHUNK_RANGE + 1):
            chunks_in_range.append((x, y))

    return chunks_in_range
