from game_state import *
from moves import *

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