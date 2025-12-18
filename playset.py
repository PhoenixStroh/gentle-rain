from agent import *
from game_state import *
import statistics

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

class Playset:
    agent: Agent
    rounds: int
    seed: int

    save_condition: SaveCondition
    
    score_results: list[int]
    saved_history: list[GameHistory]

    def __init__(self, agent: Agent, rounds: int = 1, seed: int = None, is_saving_states = False, save_condition: SaveCondition = None):
        self.agent = agent
        self.rounds = rounds
        self.seed = seed

        self.save_condition = save_condition

        self.score_results = []
        self.saved_histories = []
    
    def get_score_mean(self) -> float:
        if len(self.score_results) == 0:
            return 0.0
        return statistics.mean(self.score_results)

    def reset(self):
        self.score_results = []
        self.saved_histories = []

    def run(self):
        self.reset()

        if self.rounds < 1:
            return

        random.seed(self.seed)

        for i in range(self.rounds):
            game = GameState()
            history = GameHistory(game, True, self.is_saving_states)

            self.agent.game = game

            while game.state == State.LIVE:
                moves = get_possible_moves(game)
                if len(moves) == 0:
                    break

                chosen_move = self.agent.choose_move(moves)
                
                if chosen_move == None:
                    print("WARNING: AGENT CHOSEN MOVE IS INVALID. ENDING GAME EARLY")
                    break
                
                result = chosen_move.attempt(game)

                if result:
                    history.add_move(chosen_move)
            
            self.score_results.append(game.get_score())

            if self.save_condition != None:
                if self.save_condition.is_saving(game):
                    self.saved_histories.append(history)
