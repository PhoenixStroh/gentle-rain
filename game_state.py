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

class Move:
    def attempt(self, game_state: GameState) -> bool:
        return False
    
    def attempt_undo(self, game_state: GameState) -> bool:
        return False

    def __str__(self):
        return "MoveEmpty"

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
            if len(game_state.deck) == 0 and game_state.drawn_tiles == ():
                game_state.state = State.LOST

        return result

    def attempt_undo(self, game_state: GameState) -> bool:
        is_quad = game_state.board.is_coord_any_quad(self.position)

        result = game_state.board.attempt_remove_tile(self.position)

        if result:
            if not is_quad:
                game_state.rehold_tile(self.tile)

            if len(game_state.deck) != 0:
                game_state.state = State.LIVE

        return result

    def __str__(self):
        return "MoveTile: %s -> %s" % (self.tile, self.position)

class MoveToken(Move):
    position: tuple[int]
    token: int

    def __init__(self, token: int, position: tuple[int]):
        super().__init__()

        self.position = position
        self.token = token

    def attempt(self, game_state: GameState) -> bool:
        # attempt to add token to specific quad
        result = game_state.board.attempt_add_token(self.position, self.token)

        if result:
            # if no more tokens left, set game to win
            if len(game_state.board.tokens_left) == 0:
                game_state.state = State.WON
                return result
        
        # if placing last pending token, draw new tiles
        if len(game_state.board.pending_token_slots) == 0:
            game_state.draw_new_tiles()

        return result

    def attempt_undo(self, game_state: GameState) -> bool:
        result = game_state.board.attempt_remove_token(self.position, self.token)

        if result:
            if len(game_state.board.pending_token_slots) == 1:
                game_state.rehold_tile()

            if len(game_state.board.tokens_left) != 0:
                game_state.state = State.LIVE

        return result

    def __str__(self):
        return "MoveToken: %s -> %s" % (self.token, self.position)

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
        if len(result) != 0:
            return result
        else:
            game_state.board.pending_token_slots.clear()

    for drawn_tile in game_state.drawn_tiles:
        for space in game_state.board.available_spaces:
            if game_state.board.is_tile_placement_legal(space, drawn_tile):
                result.append(
                    MoveTile(drawn_tile, space)
                )

    return result

class GameHistory:
    game_state: GameState
    move_history: list[Move]
    state_history: list[GameState]
    header: int = -1 # index of last acted move

    is_record_moves: bool
    is_record_states: bool

    def __init__(self, game_state: GameState, is_record_moves: bool = True, is_record_states: bool = False):
        self.game_state = game_state
        self.is_record_moves = is_record_moves
        self.is_record_states = is_record_states
        
        self.move_history = []
        self.state_history = []

    def get_move(self, index: int) -> Move:
        if index < 0:
            return None
        if index >= len(self.move_history):
            return None
        return self.move_history[index]

    def get_last_move(self) -> Move:
        return self.get_move(self.header)

    def get_next_move(self) -> Move:
        return self.get_move(self.header + 1)

    def add_move(self, move: Move = None, state: GameState = None):
        if self.header >= 0:
            self.move_history = self.move_history[:self.header + 1] # cutoff all history after header
        
        if move != None and self.is_record_moves:
            self.move_history.append(move)
        if state != None and self.is_record_states:
            self.state_history.append(state)
        self.header += 1

    def attempt_undo(self) -> bool:
        last_move = self.get_last_move()
        if last_move == None:
            return False

        result = last_move.attempt_undo(self.game_state)

        if result:
            self.header -= 1

        return result

    def attempt_redo(self) -> bool:
        next_move = self.get_next_move()
        if next_move == None:
            return False

        result = next_move.attempt(self.game_state)

        if result:
            self.header += 1

        return result

    def __str__(self):
        result = "GameHistory:\n"

        for move in self.move_history:
            result += " " + str(move) + "\n"

        return result