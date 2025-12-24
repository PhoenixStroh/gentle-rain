from data import *
from board_state import *
from enum import Enum

class State(Enum):
    LIVE = 0
    WON = 1
    LOST = 2

class GameState:
    deck: list[tuple[tuple[int]]]
    board: BoardState
    state: State
    
    drawn_tiles: tuple
    discarded_tiles: list[tuple[tuple[int]]]

    def __init__(self):
        self.board = BoardState()
        self.state = State.LIVE

        self.deck = init_deck()
        self.draw_new_tiles()
        self.discarded_tiles = []

    def get_score(self) -> int:
        return len(self.deck) + (8 - len(self.board.tokens_left))

    def draw_new_tiles(self):
        self.drawn_tiles = ()
        if len(self.deck) > 0:
            self.drawn_tiles = self.deck.pop()
    
    def rehold_tile(self, tile: tuple[int] = ()):
        if self.drawn_tiles != ():
            self.deck.append(self.drawn_tiles)
        
        self.drawn_tiles = ()
        if tile != ():
            self.drawn_tiles = get_tile_rotations(tile)

    def discard_tile(self):
        if self.drawn_tiles != ():
            self.discarded_tiles.append(self.drawn_tiles)
            
        self.drawn_tiles = ()
    
    def undiscard_tile(self):
        if len(self.discarded_tiles) > 0:
            self.drawn_tiles = self.discarded_tiles.pop()

    def __str__(self):
        return "Game:\n %s\n\n Drawn Tiles: %s\n State: %s\n Drawn Tiles: %s\n Deck: %s" % (self.board, self.drawn_tiles, self.state, self.drawn_tiles, self.deck)

def game_state_compare(a: GameState, b: GameState) -> dict:
    comparison = {}

    comparison["board"] = board_state_compare(a.board, b.board)
    if comparison["board"] == {}:
        comparison.pop("board")

    if not a.deck == b.deck:
        if len(a.deck) == len(b.deck):
            comparison["deck"] = []

            for i in range(len(a.deck)):
                if a.deck[i] != b.deck[i]:
                    comparison["deck"].append((a.deck[i], b.deck[i]))
        else:
            comparison["deck_size"] = "%s / %s" % (len(a.deck), len(b.deck))
    
    if not a.drawn_tiles == b.drawn_tiles:
        comparison["drawn_tiles"] = "%s / %s" % (a.drawn_tiles, b.drawn_tiles)

    if not a.state == b.state:
        comparison["state"] = "%s / %s" % (a.state, b.state)

    return comparison