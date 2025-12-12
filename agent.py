from game_state import *

class Agent:
    game: GameState

    def __init__(self, game: GameState):
        self.game = game

    def choose_move(self, moves: list[Move]) -> Move:
        return None

class AgentFirst(Agent):
    def choose_move(self, moves: list[Move]) -> Move:
        return moves[0]