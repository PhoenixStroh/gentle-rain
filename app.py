from data import *
import tkinter as tk
from board_state import *
from game_state import *
from game_history import *
from visuals import *
import threading
import time

class App:
    root : tk.Tk
    visuals: Visuals

    game: GameState
    history: GameHistory

    input_callbacks: list[callable]

    def __init__(self, game: GameState = None, history: GameHistory = None):
        self.root = tk.Tk()
        self.root.title("Gentle Rain")
        
        self.game = game
        if history == None:
            if game != None:
                self.history = GameHistory(game)
        else:
            self.history = history

        self.input_callbacks = []

        self.visuals = Visuals(self.root)

    def undo(self):
        if self.history != None:
            self.history.attempt_undo()
            self.draw()

    def redo(self):
        if self.history != None:
            self.history.attempt_redo()
            self.draw()

    def add_input_callback(self, callback: callable):
        self.input_callbacks.append(callback)

    def callback_undo_redo(self, event):
        if event.keysym in ("a", "Left"):
            self.undo()
            
        if event.keysym in ("d", "Right"):
            self.redo()

    def key_handler(self, event):
        if event.keysym in ("q", "Escape"):
            self.end()
            return
        
        for callback in self.input_callbacks:
            callback(event)

    def start(self, start_fn: callable = None):
        self.root.bind("<Key>", self.key_handler)
        
        if start_fn != None:
            self.root.after(1, start_fn)
        self.root.after(2, self.draw)
        self.root.mainloop()
    
    def end(self):
        self.root.destroy()
    
    def draw(self):
        self.visuals.draw_game_state(self.game)

class AppPlayset(App):
    history_set: list[GameHistory]
    history_set_index: int

    def __init__(self, history_set: list[GameHistory]):
        self.history_set = history_set

        self.history_set_index = 0

        game: GameState = None
        history: GameHistory = None

        if len(history_set) > 0:
            game = history_set[0].game_state
            history = history_set[0]

        super().__init__(game, history)

        self.add_input_callback(self.callback_next_back_set)
    
    def update_history_set_index(self, value):
        if len(self.history_set) == 0:
            return
        
        self.history_set_index = max(0, min(len(self.history_set) - 1, self.history_set_index + value))

        self.history = self.history_set[self.history_set_index]
        self.game = self.history.game_state

        self.draw()

    def callback_next_back_set(self, event):
        if event.keysym == "comma":
            self.update_history_set_index(-1)
            
        if event.keysym == "period":
            self.update_history_set_index(1)