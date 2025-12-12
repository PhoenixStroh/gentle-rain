from data import *
from board_state import *
from game_state import *
from agent import *
import time

speed = 0.5

game = GameState()

def step():
    game.draw()
    time.sleep(speed)

agent = AgentFirst()

while game.state == State.LIVE:
    moves = get_possible_moves(game)
    if len(moves) == 0:
        break

    chosen_move = agent.choose_move(moves)
    
    if chosen_move != None:
        chosen_move.attempt(game)

    step()