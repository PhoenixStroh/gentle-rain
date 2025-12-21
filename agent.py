from game_state import *
from moves import *

class Agent:
    game: GameState

    def __init__(self, game: GameState = None):
        self.game = game

    def choose_move(self, moves: list[Move]) -> Move:
        return None

class AgentFirst(Agent):
    def choose_move(self, moves: list[Move]) -> Move:
        return moves[0]

class AgentRandom(Agent):
    def choose_move(self, moves: list[Move]) -> Move:
        return moves[random.randint(0, len(moves) - 1)]