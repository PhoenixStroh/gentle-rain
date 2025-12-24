from data import *
import tkinter as tk
from board_state import *
from game_state import *
from game_history import *
import threading
import time

tile_size = (50, 50)
available_space_size_ratio = (0.2, 0.2)

class Visuals:
    root: tk.Tk
    canvas: tk.Canvas

    def __init__(self, root: tk.Tk, dimensions = "700x700"):
        self.root = root
        self.root.geometry(dimensions)
        self.canvas = tk.Canvas(root)

        self.canvas.pack(fill=tk.BOTH, expand=1)

    def get_width(self) -> int:
        return self.root.winfo_width()

    def get_height(self) -> int:
        return self.root.winfo_height()

    def clear(self):
        self.canvas.delete("all")

    def draw_center_rectangle(self, pos: tuple[int], size: tuple[int], kwargs = {}):
        half_size = (size[0] * 0.5, size[1] * 0.5)
        self.canvas.create_rectangle(pos[0] - half_size[0], pos[1] - half_size[1], pos[0] + half_size[0], pos[1] + half_size[1], **kwargs)

    def draw_center_circle(self, pos: tuple[int], size: int, kwargs = {}):
        half_size = size * 0.5
        self.canvas.create_oval(pos[0] - half_size, pos[1] - half_size, pos[0] + half_size, pos[1] + half_size, **kwargs)

    def draw_tile(self, coord: tuple[int], tile: tuple[int]):
        pos = (coord[0] * tile_size[0] + self.get_width() * 0.5, coord[1] * tile_size[1] + self.get_height() * 0.5)
        
        color_offset = (tile_size[0] * .5 * 0.8, tile_size[1] * .5 * 0.8)
        color_size = tile_size[0] * 0.3
        
        self.draw_center_rectangle(pos, tile_size, {"outline":"black", "fill":"gray", "width":1})
        
        for i in range(4):
            vector = dir_to_vector(i)
            offset = (color_offset[0] * vector[0], color_offset[1] * vector[1])
            
            self.draw_center_circle( (pos[0] + offset[0], pos[1] + offset[1]), color_size, {"outline":"black", "fill":get_color_name(tile[i])})

    def draw_available_space(self, coord: tuple[int]):
        pos = (
            coord[0] * tile_size[0] + self.get_width() * 0.5, 
            coord[1] * tile_size[1] + self.get_height() * 0.5
        )

        self.draw_center_rectangle(pos, (tile_size[0] * available_space_size_ratio[0], tile_size[1] * available_space_size_ratio[1]), {"outline":"black", "fill":"lightGray", "width":1})

    def draw_token_slot(self, coord: tuple[int]):
        size = 25
        pos = ((coord[0] + 0.5) * tile_size[0] + self.get_width() * 0.5, (coord[1] + 0.5) * tile_size[1] + self.get_height() * 0.5)
        
        self.draw_center_circle(pos, size, {"outline":"red", "fill":"white"})
    
    def draw_board_state(self, board_state: BoardState):
        self.clear()

        space = 10
        margin = 10
        size = 20
        for i in range(len(board_state.tokens_left)):
            token = list(board_state.tokens_left)[i]
            self.draw_center_circle((margin + size * 0.5 + (space + size) * i, margin + size * 0.5), size, {"outline":"black", "fill":get_color_name(token)})

        for coord in board_state.tiles.keys():
            self.draw_tile(coord, board_state.tiles[coord])
        
        for coord in board_state.available_spaces:
            self.draw_available_space(coord)
        
        for token_slot in board_state.pending_token_slots:
            self.draw_token_slot(token_slot)

    def draw_game_state(self, game_state: GameState):
        self.clear()
        self.draw_board_state(game_state.board)

        drawn_tile = "None"

        if len(game_state.drawn_tiles) > 0:
            drawn_tile = game_state.drawn_tiles[0]

        content = "Deck: %s\nDrawn Tile: %s\n%s\nScore: %s" % (len(game_state.deck), drawn_tile, game_state.state, game_state.get_score())

        self.canvas.create_text(self.get_width() - 50, self.get_height() - 50, text=content, font=("Arial", 12), fill="black", anchor="e")

class App:
    root : tk.Tk
    visuals: Visuals

    game: GameState
    history: GameHistory

    input_callbacks: list[callable]

    def __init__(self, game: GameState):
        self.root = tk.Tk()
        self.root.title("Gentle Rain")
        
        self.game = game
        self.history = GameHistory(game)

        self.input_callbacks = []

        self.visuals = Visuals(self.root)

    def undo(self):
        self.history.attempt_undo()
        self.draw()

    def redo(self):
        self.history.attempt_redo()
        self.draw()

    def add_input_callback(self, callback: callable):
        self.input_callbacks.append(callback)

    def callback_undo_redo(self, event):
        if event.keysym in ("a", "left"):
            self.undo()
            
        if event.keysym in ("d", "right"):
            self.redo()

    def key_handler(self, event):
        if event.keysym in ("esc"):
            self.end()
        
        for callback in self.input_callbacks:
            callback(event)

    def start(self, start_fn: callable = None):
        self.root.bind("<Key>", self.key_handler)
        
        if start_fn != None:
            self.root.after(1, start_fn)
        self.root.after(2, self.draw)
        self.root.mainloop()
    
    def end(self):
        self.root.quit()
        print("HERE?")
    
    def draw(self):
        self.visuals.draw_game_state(self.game)