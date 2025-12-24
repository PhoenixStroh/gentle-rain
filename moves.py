from game_state import *

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

        if result:
            game_state.drawn_tiles = ()

            if len(game_state.board.pending_token_slots) == 0:
                game_state.draw_new_tiles()
        
            if len(game_state.deck) == 0 and game_state.drawn_tiles == ():
                game_state.state = State.LOST

        return result

    def attempt_undo(self, game_state: GameState) -> bool:
        result = game_state.board.attempt_remove_tile(self.position)

        if result:
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

class MoveDiscard(Move):
    def __init__(self):
        super().__init__()

    def attempt(self, game_state: GameState):
        game_state.discard_tile()
        game_state.draw_new_tiles()

    def attempt_undo(self, game_state: GameState):
        game_state.undiscard_tile()

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

    if game_state.state != State.LIVE:
        return result

    if len(game_state.board.pending_token_slots) > 0:
        for slot in game_state.board.pending_token_slots:
            colors = game_state.board.get_valid_colors_in_quad(slot)
            for color in colors:
                result.append(
                    MoveToken(color, slot)
                )
        if len(result) != 0:
            return result

    for drawn_tile in game_state.drawn_tiles:
        for space in game_state.board.available_spaces:
            if game_state.board.is_tile_placement_legal(space, drawn_tile):
                result.append(
                    MoveTile(drawn_tile, space)
                )

    if len(result) == 0:
        result.append(MoveDiscard())

    return result

def get_random_move(game_state: GameState) -> Move:
    moves = get_possible_moves(game_state)
    if len(moves) > 0:
        return random.choice(moves)
    return None