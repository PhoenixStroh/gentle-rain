from game_state import *

class Agent:
    def choose_move(self, moves: list[Move]) -> Move:
        return None

class AgentFirst(Agent):
    def choose_move(self, moves: list[Move]) -> Move:
        return moves[0]