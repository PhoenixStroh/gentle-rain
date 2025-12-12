from data import *
from graphics import *

class BoardState:
    tiles = {} #[coord: tile]
    available_spaces = set([(0,0)]) #coord
    pending_token_slots = set([]) #coord (offset half)
    tokens_left = set([0, 1, 2, 3, 4, 5, 6, 7]) #0-7 color index

    def get_opposing_color(self, coord: tuple[int], dir: int) -> int:
        if coord in self.tiles.keys():
            return self.tiles[coord][dir_to_opposite_dir(dir)]
        return -1

    # does not validate quad, only assumes (0,0) and (1,1) are valid
    def get_colors_in_quad(self, corner_coord: tuple[int]) -> tuple[int]:
        result = []

        if corner_coord in self.tiles.keys():
            tile = self.tiles[corner_coord]
            result.append(tile[1])
            result.append(tile[2])
        
        opposing_coord = add_vectors(corner_coord, (1,1))
        if opposing_coord in self.tiles.keys():
            tile = self.tiles[opposing_coord]
            result.append(tile[0])
            result.append(tile[3])

        return tuple(result)  

    def get_valid_colors_in_quad(self, corner_coord: tuple[int]) -> tuple[int]:
        result = []

        colors = self.get_colors_in_quad(corner_coord)

        for color in colors:
            if color in self.tokens_left:
                result.append(color)
        return result

    def is_coord_quad(self, corner_coord: tuple[int]) -> bool:
        for offset in quad_coords:
            coord = add_vectors(corner_coord, offset)
            if coord not in self.tiles.keys():
                return False
        return True

    def is_token_placement_legal(self, corner_coord: tuple[int], token: int) -> bool:
        if not self.is_coord_quad(corner_coord):
            return False
        
        available_colors = self.get_colors_in_quad(corner_coord)

        return token in available_colors

    def attempt_add_token(self, corner_coord: tuple[int], token: int) -> bool:
        fail_message = "FAILED TO ADD TOKEN"
        if corner_coord not in self.pending_token_slots:
            print(fail_message)
            return False
        
        if token not in self.tokens_left:
            print(fail_message)
            return False

        if not self.is_token_placement_legal(corner_coord, token):
            print(fail_message)
            return False

        self.pending_token_slots.remove(corner_coord)
        self.tokens_left.remove(token)

        

        return True

    def is_tile_placement_legal(self, coord: tuple[int], tile: tuple[int]) -> bool:
        for i in range(4):
            neighbor_coord = add_vectors(coord, dir_to_vector(i))
            color = tile[i]
            opposing_color = self.get_opposing_color(neighbor_coord, i)
            if opposing_color == -1:
                continue
            
            if color != opposing_color:
                return False

        return True

    def add_neighboring_spaces(self, coord: tuple[int]):
        for i in range(4):
            neighbor_coord = add_vectors(coord, dir_to_vector(i))
            if neighbor_coord not in self.tiles.keys():
                self.available_spaces.add(neighbor_coord)

    def add_pending_token_slots(self, coord: tuple[int]):
        for offset in quad_coords:
            test_coord = add_vectors(add_vectors(coord, (-1, -1)), offset)

            if self.is_coord_quad(test_coord):
                self.pending_token_slots.add(test_coord)
            

    def attempt_add_tile(self, coord: tuple[int], tile: tuple[int]) -> bool:
        fail_message = "FAILED TO ADD TILE"
        # check if available space
        if coord not in self.available_spaces:
            print(fail_message)
            return False
        
        # check if legal placement
        if not self.is_tile_placement_legal(coord, tile):
            print(fail_message)
            return False

        # check if tile is already occupied (SHOULDN'T EVER TRIGGER)
        if coord in self.tiles.keys():
            print(fail_message)
            print("WARNING: TILE ATTEMPTED PLACE ON ALREADY EXISTING TILE")
            return False

        # remove space and add new ones
        self.available_spaces.remove(coord)
        self.add_neighboring_spaces(coord)

        self.tiles[coord] = tile

        # attempt to add pending token slots if creating a quad
        self.add_pending_token_slots(coord)

        return True

    def draw(self):
        clear()

        space = 10
        margin = 10
        size = 20
        for i in range(len(self.tokens_left)):
            token = list(self.tokens_left)[i]
            setFill(get_color_name(token))
            circle( margin + size * 0.5 + (space + size) * i, margin + size * 0.5, size)

        for coord in self.tiles.keys():
            draw_tile(coord, self.tiles[coord])
        
        for token_slot in self.pending_token_slots:
            draw_token_slot(token_slot)

    def __str__(self):
        return "Board:\n Tiles:%s\n Spaces:%s\n Token Slots:%s\n Tokens Left:%s" % (self.tiles, self.available_spaces, self.pending_token_slots, self.tokens_left)
