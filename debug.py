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
    app = App()
    game_app = GameApp(app)
    
    game_state = GameState()
    game_history = GameHistory(game_state)

    agent = AgentFirst()

    def step():
        game_state.draw(game_app)
        time.sleep(.1)

    def undo():
        game_history.attempt_undo()
        game_state.draw(game_app)

    def redo():
        game_history.attempt_redo()
        game_state.draw(game_app)

    def progress():
        moves = get_possible_moves(game_state)
        if len(moves) == 0:
            return

        chosen_move = agent.choose_move(moves)
        
        if chosen_move != None:
            result = chosen_move.attempt(game_state)
        
            if result:
                game_history.add_move(chosen_move)

        step()

    def key_handler(event):
        if event.keysym == "space":
            progress()
        
        if event.keysym in ("a", "left"):
            undo()
            
        if event.keysym in ("d", "right"):
            redo()

        # print(event.char, event.keysym, event.keycode)

    app.root.bind("<Key>", key_handler)

    # def game_loop():
    #     def step():
    #         game_state.draw(game_app)
    #         time.sleep(.1)

    #     while game_state.state == State.LIVE:
    #         moves = get_possible_moves(game_state)
    #         if len(moves) == 0:
    #             break

    #         chosen_move = agent.choose_move(moves)
            
    #         if chosen_move != None:
    #             chosen_move.attempt(game_state)

    #         app.root.after(0, step())

    # thread = threading.Thread(target=game_loop, daemon=True)
    # thread.start()

    app.root.after(1, step)
    app.start()

def test8():
    app = App()
    game_app = GameApp(app)
    
    game_state = GameState()
    game_history = GameHistory(game_state)

    agent = AgentFirst()

    selected_move = 0
    possible_moves: list[Move]

    def step():
        game_state.draw(game_app)
        time.sleep(.1)

    def undo(is_draw = True):
        game_history.attempt_undo()
        if is_draw:
            game_state.draw(game_app)

    def redo():
        game_history.attempt_redo()
        game_state.draw(game_app)

    def cycle_move(increment: int):
        nonlocal selected_move

        selected_move += increment
        print("selected: %s" % selected_move)
        progress()
        undo(False)

    def progress():
        nonlocal selected_move, possible_moves

        moves = possible_moves
        print("Moves:")
        for move in moves:
            print(move)
        if len(moves) == 0:
            return

        chosen_move = moves[selected_move % len(moves)]
        print("actual selected: %s" % (selected_move % len(moves)))
        
        if chosen_move != None:
            result = chosen_move.attempt(game_state)
        
            if result:
                game_history.add_move(chosen_move)

        step()

    def key_handler(event):
        nonlocal possible_moves

        if event.keysym == "space":
            print("Possible Moves:")
            for move in possible_moves:
                print(" ", move)
            progress()
            
            possible_moves = get_possible_moves(game_state)
            selected_move = 0
        
        if event.keysym in ("a", "left"):
            undo()
            
        if event.keysym in ("d", "right"):
            redo()
        
        if event.keysym in ("w", "up"):
            cycle_move(1)
            
        if event.keysym in ("s", "down"):
            cycle_move(-1)

        # print(event.char, event.keysym, event.keycode)

    app.root.bind("<Key>", key_handler)

    # def game_loop():
    #     def step():
    #         game_state.draw(game_app)
    #         time.sleep(.1)

    #     while game_state.state == State.LIVE:
    #         moves = get_possible_moves(game_state)
    #         if len(moves) == 0:
    #             break

    #         chosen_move = agent.choose_move(moves)
            
    #         if chosen_move != None:
    #             chosen_move.attempt(game_state)

    #         app.root.after(0, step())

    # thread = threading.Thread(target=game_loop, daemon=True)
    # thread.start()

    def start():
        nonlocal possible_moves
        possible_moves = get_possible_moves(game_state)

    app.root.after(1, step)
    app.root.after(2, start)
    app.start()

def run():
    test8()

run()