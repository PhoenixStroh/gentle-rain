from data import *
from board_state import *
from graphics import *
from enum import Enum

class State(Enum):
    LIVE = 0
    WON = 1
    LOST = 2

class GameState:
    deck: list[tuple[tuple[int]]] = init_deck()
    board: BoardState = BoardState()
    drawn_tiles = ()
    state: State = State.LIVE

    def __init__(self):
        self.draw_new_tiles()

    def draw_new_tiles(self):
        self.drawn_tiles = ()
        if len(self.deck) > 0:
            self.drawn_tiles = list(self.deck.pop())
            
            if not has_any_move(self):
                print("NO VALID MOVES, DISCARDING DRAWN TILES")
                self.draw_new_tiles()
    
    def draw(self):
        clear()
        self.board.draw()

        drawn_tile = "None"

        if len(self.drawn_tiles) > 0:
            drawn_tile = self.drawn_tiles[0]

        content = "Deck: %s\nDrawn Tile: %s\n%s" % (len(self.deck), drawn_tile, self.state)

        setColor("black")
        setFont("Arial", 14)
        text(getWidth() - 50, getHeight() - 50, content, align="e", ang=0)

    def __str__(self):
        return "Game:\n %s\n\n Drawn Tiles: %s\n State: %s" % (self.board, self.drawn_tiles, self.state)

class Move:
    def attempt(self, game_state: GameState) -> bool:
        return False
    
    def __str__(self):
        return "Move()"

class MoveTile(Move):
    position: tuple[int]
    tile: tuple[int]

    def __init__(self, tile, position: tuple[int]):
        super().__init__()

        self.position = position
        self.tile = tile

    def attempt(self, game_state: GameState) -> bool:
        result = game_state.board.attempt_add_tile(self.position, self.tile)

        if len(game_state.board.pending_token_slots) == 0:
            game_state.draw_new_tiles()

        if result:
            if len(game_state.deck) == 0:
                game_state.state = State.LOST

        return result
    
    def __str__(self):
        return "MoveTile(%s, %s)" % (self.position, self.tile)

class MoveToken(Move):
    position: tuple[int]
    token: int

    def __init__(self, token: int, position: tuple[int]):
        super().__init__()

        self.position = position
        self.token = token

    def attempt(self, game_state: GameState) -> bool:
        result = game_state.board.attempt_add_token(self.position, self.token)

        if result:
            if len(game_state.board.tokens_left) == 0:
                game_state.state = State.WON
                return result
        
        if len(game_state.board.pending_token_slots) == 0:
            game_state.draw_new_tiles()

        return result

    def __str__(self):
        return "MoveToken(%s, %s)" % (self.position, self.token)

def has_any_move(game_state: GameState) -> bool:
    if len(game_state.board.pending_token_slots) > 0:
        return True

    for drawn_tile in game_state.drawn_tiles:
        for space in game_state.board.available_spaces:
            if game_state.board.is_tile_placement_legal(space, drawn_tile):
                return True

    return False    

def get_possible_moves(game_state: GameState) -> list[Move]:
    result = []

    if len(game_state.board.pending_token_slots) > 0:
        for slot in game_state.board.pending_token_slots:
            colors = game_state.board.get_valid_colors_in_quad(slot)
            for color in colors:
                result.append(
                    MoveToken(color, slot)
                )
        return result

    for drawn_tile in game_state.drawn_tiles:
        for space in game_state.board.available_spaces:
            if game_state.board.is_tile_placement_legal(space, drawn_tile):
                result.append(
                    MoveTile(drawn_tile, space)
                )

    return result