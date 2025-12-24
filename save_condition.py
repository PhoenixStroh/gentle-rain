from game_state import *

class SaveCondition:
    def is_saving(self, game_state: GameState):
        return True

class SaveConditionPointThreshold:
    threshold: int

    def __init__(self, threshold: int = 1):
        self.threshold = threshold

    def is_saving(self, game_state: GameState):
        if game_state.get_score() >= self.threshold:
            return True
        return False