from data import *
from board_state import *
from game_state import *
from agent import *
import time

def test1():
    board = BoardState()

    def step():
        board.draw()
        time.sleep(1)

    board.attempt_add_tile((0,0), (3,0,4,6))
    board.attempt_add_tile((0,-1), (7,2,3,0))
    board.attempt_add_tile((1,0), (7,2,3,0))
    step()
    board.attempt_add_tile((1,-1), rotate_tile(rotate_tile((7,2,3,0))))
    step()
    board.attempt_add_token((0,-1), 4)
    step()

def test2():
    game = GameState()

    def step():
        game.draw()
        time.sleep(1)
    
    step()

    print(game)
    moves = get_possible_moves(game)
    for move in moves:
        print(move)

def test3():
    game = GameState()

    def step():
        game.draw()
        time.sleep(0.1)
    
    agent = AgentFirst()

    while game.state == State.LIVE:
        moves = get_possible_moves(game)
        if len(moves) == 0:
            break

        chosen_move = agent.choose_move(moves)
        
        if chosen_move != None:
            chosen_move.attempt(game)

        step()

def test4():
    random.seed(1)
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

    for i in range(30):
        game_history.attempt_undo()
        step()

    for i in range(30):
        game_history.attempt_redo()
        step()

    while True:
        input_result = input()
        if input_result == "undo":
            result = game_history.attempt_undo()
        if input_result == "redo":
            result = game_history.attempt_redo()
        
        print(result)
        
        game.draw()    

def run():
    test3()

run()