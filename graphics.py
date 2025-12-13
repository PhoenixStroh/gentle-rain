from data import *
from SimpleGraphics import *

tile_size = (50, 50)
available_space_size_ratio = (0.2, 0.2)

def draw_tile(coord: tuple[int], tile: tuple[int]):
    pos = (coord[0] * tile_size[0] + getWidth() * 0.5, coord[1] * tile_size[1] + getHeight() * 0.5)
    
    color_offset = (tile_size[0] * .5 * 0.8, tile_size[1] * .5 * 0.8)
    color_size = tile_size[0] * 0.3
    
    setFill("gray")
    rect(pos[0], pos[1], tile_size[0], tile_size[1])
    
    for i in range(4):
        vector = dir_to_vector(i)
        offset = (color_offset[0] * vector[0] + tile_size[0] * 0.5, color_offset[1] * vector[1] + tile_size[1] * 0.5)
        setFill(get_color_name(tile[i]))
        circle(pos[0] + offset[0], pos[1] + offset[1], color_size)

def draw_available_space(coord: tuple[int]):
    pos = (
        coord[0] * tile_size[0] + getWidth() * 0.5 + tile_size[0] * 0.5, 
        coord[1] * tile_size[1] + getHeight() * 0.5 + tile_size[1] * 0.5
    )

    setFill("lightGray")
    rect(
        pos[0] - tile_size[0] * available_space_size_ratio[0] * 0.5,
        pos[1] - tile_size[1] * available_space_size_ratio[1] * 0.5,
        tile_size[0] * available_space_size_ratio[0],
        tile_size[1] * available_space_size_ratio[1]
    )

def draw_token_slot(coord: tuple[int]):
    size = 30
    pos = ((coord[0] + 1) * tile_size[0] + getWidth() * 0.5, (coord[1] + 1) * tile_size[1] + getHeight() * 0.5)
    
    setOutline("red")
    setFill("white")
    circle(pos[0], pos[1], size)
    setOutline("black")