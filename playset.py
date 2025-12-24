from agent import *
from game_state import *
from game_history import *
import statistics
from save_condition import *

class Playset:
    agent: Agent
    rounds: int
    seed: int

    save_condition: SaveCondition
    
    score_results: list[int]
    saved_history: list[GameHistory]

    def __init__(self, agent: Agent, rounds: int = 1, seed: int = None, save_condition: SaveCondition = None):
        self.agent = agent
        self.rounds = rounds
        self.seed = seed

        self.save_condition = save_condition

        self.score_results = []
        self.saved_history = []
    
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
            history = GameHistory(game, True, False)

            self.agent.game = game

            while game.state == State.LIVE:
                moves = get_possible_moves(game)
                if len(moves) == 0:
                    print("WARNING: NO MOVES FOUND. ENDING GAME EARLY.")
                    break

                chosen_move = self.agent.choose_move(moves)
                
                if chosen_move == None:
                    print("WARNING: AGENT CHOSEN MOVE IS EMPTY. ENDING GAME EARLY")
                    break
                
                result = chosen_move.attempt(game)

                if result:
                    history.add_move(chosen_move)
                else:
                    print("WARNING: AGENT CHOSEN MOVE FAILED. ENDING GAME EARLY")
                    break
            
            self.score_results.append(game.get_score())

            if self.save_condition != None:
                if self.save_condition.is_saving(game):
                    self.saved_history.append(history)
    
    def __str__(self):
        return "Playset:\n Agent: %s\n Rounds: %s\n Seed: %s\n Save Condition: %s\n Score Mean: %s\n Score Results: %s\n" % (type(self.agent).__name__, self.rounds, self.seed, self.save_condition, self.get_score_mean(), self.score_results)
