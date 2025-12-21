from data import *
from board_state import BoardState
from enum import Enum

class State(Enum):
    LIVE = 0
    WON = 1
    LOST = 2

class GameState:
    deck: list[tuple[tuple[int]]]
    board: BoardState
    state: State

    def __init__(self):
        self.board = BoardState()
        self.state = State.LIVE

        self.deck = init_deck()
        self.draw_new_tiles()

    def get_score(self) -> int:
        return len(self.deck) + (8 - len(self.board.tokens_left))

    def draw_new_tiles(self):
        from moves import has_any_move

        self.drawn_tiles = ()
        if len(self.deck) > 0:
            self.drawn_tiles = list(self.deck.pop())
            
            if not has_any_move(self):
                print("NO VALID MOVES, DISCARDING DRAWN TILES")
                self.draw_new_tiles()
    
    def rehold_tile(self, tile: tuple[int] = ()):
        if self.drawn_tiles != ():
            self.deck.append(self.drawn_tiles)
        
        self.drawn_tiles = ()
        if tile != ():
            self.drawn_tiles = get_tile_rotations(tile)

    def __str__(self):
        return "Game:\n %s\n\n Drawn Tiles: %s\n State: %s" % (self.board, self.drawn_tiles, self.state)