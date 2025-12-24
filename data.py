# definitions:
# coords: (int, int) / (x, y)
# color: int / read "get_color_name", -1 is no color
# direction: int / 0: up, 1: right, 2: down, 3: left
# tile: (int, int, int, int) / (up color, right color, down color, left color)
# tile_set / tile_with_rotation: (tile, tile, tile, tile) / (tile, tile rotated 1, tile rotated 2, tile rotated 3)
# quad: four tiles in a square, with the top left as the origin coord

import random
from copy import deepcopy

base_deck  = (
    (3,0,4,6),
    (4,2,5,7),
    (7,6,0,3),
    (7,2,3,0),
    (2,4,5,0),
    (7,4,3,5),
    (2,0,7,1),
    (2,7,6,5),
    (3,1,0,5),
    (5,1,2,4),
    (4,2,5,3),
    (5,6,2,7),
    (0,5,6,2),
    (3,7,0,4),
    (0,6,1,4),
    (6,1,3,2),
    (0,2,1,5),
    (7,2,1,6),
    (1,4,7,0),
    (4,0,1,6),
    (6,7,3,4),
    (5,4,7,1),
    (0,3,2,6),
    (1,7,3,5),
    (5,4,1,7),
    (6,4,1,3),
    (2,3,6,5),
    (6,3,1,0)
)

base_deck_with_rotation = (
    ((0, 4, 6, 3), (3, 0, 4, 6), (4, 6, 3, 0), (6, 3, 0, 4)),
    ((2, 5, 7, 4), (4, 2, 5, 7), (5, 7, 4, 2), (7, 4, 2, 5)),
    ((0, 3, 7, 6), (3, 7, 6, 0), (6, 0, 3, 7), (7, 6, 0, 3)),
    ((0, 7, 2, 3), (2, 3, 0, 7), (3, 0, 7, 2), (7, 2, 3, 0)),
    ((0, 2, 4, 5), (2, 4, 5, 0), (4, 5, 0, 2), (5, 0, 2, 4)),
    ((3, 5, 7, 4), (4, 3, 5, 7), (5, 7, 4, 3), (7, 4, 3, 5)),
    ((0, 7, 1, 2), (1, 2, 0, 7), (2, 0, 7, 1), (7, 1, 2, 0)),
    ((2, 7, 6, 5), (5, 2, 7, 6), (6, 5, 2, 7), (7, 6, 5, 2)),
    ((0, 5, 3, 1), (1, 0, 5, 3), (3, 1, 0, 5), (5, 3, 1, 0)),
    ((1, 2, 4, 5), (2, 4, 5, 1), (4, 5, 1, 2), (5, 1, 2, 4)),
    ((2, 5, 3, 4), (3, 4, 2, 5), (4, 2, 5, 3), (5, 3, 4, 2)),
    ((2, 7, 5, 6), (5, 6, 2, 7), (6, 2, 7, 5), (7, 5, 6, 2)),
    ((0, 5, 6, 2), (2, 0, 5, 6), (5, 6, 2, 0), (6, 2, 0, 5)),
    ((0, 4, 3, 7), (3, 7, 0, 4), (4, 3, 7, 0), (7, 0, 4, 3)),
    ((0, 6, 1, 4), (1, 4, 0, 6), (4, 0, 6, 1), (6, 1, 4, 0)),
    ((1, 3, 2, 6), (2, 6, 1, 3), (3, 2, 6, 1), (6, 1, 3, 2)),
    ((0, 2, 1, 5), (1, 5, 0, 2), (2, 1, 5, 0), (5, 0, 2, 1)),
    ((1, 6, 7, 2), (2, 1, 6, 7), (6, 7, 2, 1), (7, 2, 1, 6)),
    ((0, 1, 4, 7), (1, 4, 7, 0), (4, 7, 0, 1), (7, 0, 1, 4)),
    ((0, 1, 6, 4), (1, 6, 4, 0), (4, 0, 1, 6), (6, 4, 0, 1)),
    ((3, 4, 6, 7), (4, 6, 7, 3), (6, 7, 3, 4), (7, 3, 4, 6)),
    ((1, 5, 4, 7), (4, 7, 1, 5), (5, 4, 7, 1), (7, 1, 5, 4)),
    ((0, 3, 2, 6), (2, 6, 0, 3), (3, 2, 6, 0), (6, 0, 3, 2)),
    ((1, 7, 3, 5), (3, 5, 1, 7), (5, 1, 7, 3), (7, 3, 5, 1)),
    ((1, 7, 5, 4), (4, 1, 7, 5), (5, 4, 1, 7), (7, 5, 4, 1)),
    ((1, 3, 6, 4), (3, 6, 4, 1), (4, 1, 3, 6), (6, 4, 1, 3)),
    ((2, 3, 6, 5), (3, 6, 5, 2), (5, 2, 3, 6), (6, 5, 2, 3)),
    ((0, 6, 3, 1), (1, 0, 6, 3), (3, 1, 0, 6), (6, 3, 1, 0))
)

quad_coords = (
    (0,0),
    (1,0),
    (0,1),
    (1,1)
)

def init_deck() -> list[tuple[tuple[int]]]:
    new_deck = list(deepcopy(base_deck_with_rotation))
    random.shuffle(new_deck)
    return new_deck

def dir_to_opposite_dir(dir: int) -> int:
    dict = {
        0: 2,
        1: 3,
        2: 0,
        3: 1
    }

    return dict[dir]

# +y is down, +x is right
def dir_to_vector(dir: int) -> tuple[int]:
    dict = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0)
    }

    return dict[dir]

def add_vectors(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return (a[0] + b[0], a[1] + b[1])

def get_color_name(color_index: int) -> str:
    index_to_name = {
        0: "white",
        1: "yellow",
        2: "orange",
        3: "pink",
        4: "red",
        5: "blue",
        6: "purple",
        7: "black"
    }

    if color_index not in index_to_name:
        return "null"

    return index_to_name[color_index]

def correct_tile_rotations(rotations: tuple[tuple[int]]) -> tuple[tuple[int]]:
    def weight(a: tuple[int]) -> int:
        return a[0] * 1000 + a[1] * 100 + a[2] * 10 + a[3]
    
    def compare(a: tuple[int], b: tuple[int]) -> int:
        return weight(a) - weight(b)

    from functools import cmp_to_key
    return tuple(sorted(rotations, key=cmp_to_key(compare)))

def get_tile_rotations(tile: tuple[int]) -> tuple[tuple[int]]:
    result = [tile]
    
    for i in range(3):
        result.append( rotate_tile(result[i]) )

    return correct_tile_rotations(tuple(result))

def rotate_tile(tile: tuple[int]) -> tuple[int]:
    return (tile[1], tile[2], tile[3], tile[0])