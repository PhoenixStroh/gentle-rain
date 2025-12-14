from data import *
from board_state import *
from game_state import *
from agent import *
import time

#random.seed(0)
speed = 0.5

stepthrough = False

game = GameState()
game_history = GameHistory(game)

def step():
    game.draw()
    time.sleep(speed)

agent = AgentFirst(game)

while game.state == State.LIVE:
    moves = get_possible_moves(game)
    if len(moves) == 0:
        break

    chosen_move = agent.choose_move(moves)
    
    if chosen_move != None:
        result = chosen_move.attempt(game)

        if result:
            game_history.add_move(chosen_move)

    if stepthrough:
        step()

game.draw()

print(game_history)

while True:
    input_result = input()
    if input_result == "undo":
        result = game_history.attempt_undo()
    if input_result == "redo":
        result = game_history.attempt_redo()
    
    game.draw()