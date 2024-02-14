from entity import get_entities_with
from components import Component
from entity import Entity
from constants import (
    CHUNK_WIDTH,
    CHUNK_HEIGHT,
    CHUNK_RANGE,
    TILE_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from components import (
    Component,
    CollisionComponent,
    PositionComponent,
    SpriteComponent,
    SizeComponent,
    TileComponent,
)

last_current_chunk_x = -100
last_current_chunk_y = -100
done = False


def run_chunk_system(entities):
    # global done
    # if done:
    #     return
    # for i in range(0, 800, TILE_SIZE):
    #     tile = create_tile(i, 400)
    #     entities.append(tile)

    # for i in range(320, 1200, TILE_SIZE):
    #     tile = create_tile(i, 400 - TILE_SIZE)
    #     entities.append(tile)

    # done = True
    # return

    camera_filtered_entities = get_entities_with(
        entities, Component.POSITION, Component.CAMERA
    )

    if len(camera_filtered_entities) == 0:
        return

    camera_entity = camera_filtered_entities[0]
    camera_position = camera_entity.get_component(Component.POSITION)

    current_chunk_x = int(
        (camera_position.x + (CHUNK_WIDTH * TILE_SIZE) // 2)
        // (CHUNK_WIDTH * TILE_SIZE)
    )
    current_chunk_y = int(
        (camera_position.y + (CHUNK_HEIGHT * TILE_SIZE) // 2)
        // (CHUNK_HEIGHT * TILE_SIZE)
    )

    global last_current_chunk_x, last_current_chunk_y

    if (
        current_chunk_x != last_current_chunk_x
        or current_chunk_y != last_current_chunk_y
    ):
        print(current_chunk_x, current_chunk_y)
        chunks_loaded = set(
            get_chunks_in_range(last_current_chunk_x, last_current_chunk_y)
        )

        chunks_to_load = set(get_chunks_in_range(current_chunk_x, current_chunk_y))

        chunks_to_unload = chunks_loaded - chunks_to_load

        unloaded_chunks_to_load = chunks_to_load - chunks_loaded

        # print("chunks to load", unloaded_chunks_to_load)
        # print("chunks to unload", chunks_to_unload)

        tile_entities = get_entities_with(entities, Component.TILE)
        # print(len(tile_entities))
        unload_chunk(entities, tile_entities, chunks_to_unload)

        load_chunk(entities, unloaded_chunks_to_load)

        last_current_chunk_x = current_chunk_x
        last_current_chunk_y = current_chunk_y


def load_chunk(entities, unloaded_chunks_to_load):
    for chunk_x, chunk_y in unloaded_chunks_to_load:
        chunk_key = str(chunk_x) + "_" + str(chunk_y)

        if False:  # Check if chunk_key exists
            # load chunk from file
            pass
        else:
            # tile_y = (chunk_y + 1) * (CHUNK_HEIGHT * TILE_SIZE)
            # for tile_x in range(
            #     chunk_x * CHUNK_WIDTH * TILE_SIZE,
            #     (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE,
            #     TILE_SIZE,
            # ):
            #     entity = create_tile(tile_x, tile_y)
            #     entities.append(entity)

            for tile_x in range(
                chunk_x * CHUNK_WIDTH * TILE_SIZE,
                (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE,
                TILE_SIZE,
            ):
                entity = create_tile(tile_x, (chunk_y) * (CHUNK_HEIGHT * TILE_SIZE))
                entities.append(entity)
            for tile_x in range(
                chunk_x * CHUNK_WIDTH * TILE_SIZE,
                (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE,
                TILE_SIZE,
            ):
                entity = create_tile(tile_x, (chunk_y + 1) * (CHUNK_HEIGHT * TILE_SIZE))
                entities.append(entity)

            for tile_y in range(
                chunk_y * CHUNK_HEIGHT * TILE_SIZE,
                (chunk_y + 1) * CHUNK_HEIGHT * TILE_SIZE,
                TILE_SIZE,
            ):
                entity = create_tile((chunk_x) * (CHUNK_WIDTH * TILE_SIZE), tile_y)
                entities.append(entity)

            for tile_y in range(
                chunk_y * CHUNK_HEIGHT * TILE_SIZE,
                (chunk_y + 1) * CHUNK_HEIGHT * TILE_SIZE,
                TILE_SIZE,
            ):
                entity = create_tile((chunk_x + 1) * (CHUNK_WIDTH * TILE_SIZE), tile_y)
                entities.append(entity)


def unload_chunk(entities, tile_entities, chunks_to_unload):
    tile_ids_to_remove = []
    # print(chunks_to_unload)
    for tile in tile_entities:
        tile_position = tile.get_component(Component.POSITION)

        for chunk_x, chunk_y in chunks_to_unload:
            chunk_key = str(chunk_x) + "_" + str(chunk_y)

            if is_tile_in_chunk(tile_position, chunk_x, chunk_y):
                # save this tile in the associated chunk file
                tile_ids_to_remove.append(tile.id)
    print(len(entities))

    entities = [entity for entity in entities if entity.id not in tile_ids_to_remove]
    print(len(entities))


def is_tile_in_chunk(tile_position, chunk_x, chunk_y):
    return (
        chunk_x * CHUNK_WIDTH * TILE_SIZE
        <= tile_position.x
        <= (chunk_x + 1) * CHUNK_WIDTH * TILE_SIZE
        and chunk_y * CHUNK_HEIGHT * TILE_SIZE
        <= tile_position.y
        <= (chunk_y + 1) * CHUNK_HEIGHT * TILE_SIZE
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
