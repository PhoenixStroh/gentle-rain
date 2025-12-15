from data import *
from board_state import *
from game_state import *
from agent import *
import time
from test import *
import asyncio

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

def test5():
    test = Test(AgentFirst(), 100, 1, SaveConditionPointThreshold(5))
    test.run()
    print(test.score_results)
    print(test.saved_games)
    print(test.get_score_mean())

    for game in test.saved_games:
        game.draw()
        input()

def test6():
    random.seed(1)
    speed = 1.0

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

        for move in moves:
            result = move.attempt(game)

            step()

            if result:
                result_undo = move.attempt_undo(game)

                if not result_undo:
                    print("WARNING: AGENT FERN MOVED BUT DID NOT UNDO")

        chosen_move = agent.choose_move(moves)
        
        if chosen_move != None:
            result = chosen_move.attempt(game)

            if result:
                game_history.add_move(chosen_move)

        if stepthrough:
            step()

    game.draw()

    print(game_history)

    # while True:
    #     input_result = input()
    #     if input_result == "undo":
    #         result = game_history.attempt_undo()
    #     if input_result == "redo":
    #         result = game_history.attempt_redo()
        
    #     print(result)
        
    #     game.draw()    

def test7():
    while True:
        clear()
        circle(50, 50, 50)
        if getKeys() != ():
            print(getKeys())
        sleep(1.0)

def run():
    test7()

run()