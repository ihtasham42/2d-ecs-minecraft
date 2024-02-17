from constants import TILE_SIZE


def get_tile_position(x, y):
    return x // TILE_SIZE, y // TILE_SIZE
