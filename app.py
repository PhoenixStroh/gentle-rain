from data import *
import tkinter as tk
import threading
import time

tile_size = (50, 50)
available_space_size_ratio = (0.2, 0.2)

class App:
    root : tk.Tk

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gentle Rain")
        self.root.geometry('700x700')
    
    def get_width(self) -> int:
        return self.root.winfo_width()

    def get_height(self) -> int:
        return self.root.winfo_height()

    def start(self):
        self.root.mainloop()

class GameApp:
    app: App
    canvas: tk.Canvas

    def __init__(self, app: App):
        self.app = app
        self.canvas = tk.Canvas(self.app.root)

        self.canvas.pack(fill=tk.BOTH, expand=1)

    def clear(self):
        self.canvas.delete("all")

    def draw_center_rectangle(self, pos: tuple[int], size: tuple[int], kwargs = {}):
        half_size = (size[0] * 0.5, size[1] * 0.5)
        self.canvas.create_rectangle(pos[0] - half_size[0], pos[1] - half_size[1], pos[0] + half_size[0], pos[1] + half_size[1], **kwargs)

    def draw_center_circle(self, pos: tuple[int], size: int, kwargs = {}):
        half_size = size * 0.5
        self.canvas.create_oval(pos[0] - half_size, pos[1] - half_size, pos[0] + half_size, pos[1] + half_size, **kwargs)

    def draw_tile(self, coord: tuple[int], tile: tuple[int]):
        pos = (coord[0] * tile_size[0] + self.app.get_width() * 0.5, coord[1] * tile_size[1] + self.app.get_height() * 0.5)
        
        color_offset = (tile_size[0] * .5 * 0.8, tile_size[1] * .5 * 0.8)
        color_size = tile_size[0] * 0.3
        
        self.draw_center_rectangle(pos, tile_size, {"outline":"black", "fill":"gray", "width":1})
        
        for i in range(4):
            vector = dir_to_vector(i)
            offset = (color_offset[0] * vector[0], color_offset[1] * vector[1])
            
            self.draw_center_circle( (pos[0] + offset[0], pos[1] + offset[1]), color_size, {"outline":"black", "fill":get_color_name(tile[i])})

    def draw_available_space(self, coord: tuple[int]):
        pos = (
            coord[0] * tile_size[0] + self.app.get_width() * 0.5, 
            coord[1] * tile_size[1] + self.app.get_height() * 0.5
        )

        self.draw_center_rectangle(pos, (tile_size[0] * available_space_size_ratio[0], tile_size[1] * available_space_size_ratio[1]), {"outline":"black", "fill":"lightGray", "width":1})

    def draw_token_slot(self, coord: tuple[int]):
        size = 25
        pos = ((coord[0] + 0.5) * tile_size[0] + self.app.get_width() * 0.5, (coord[1] + 0.5) * tile_size[1] + self.app.get_height() * 0.5)
        
        self.draw_center_circle(pos, size, {"outline":"red", "fill":"white"})

# app = App()
# game_app = GameApp(app)

# def draw_test():
#     game_app.draw_tile((0,0), (1,3,5,6))
#     game_app.draw_available_space((0,1))
#     game_app.draw_available_space((0,-1))
#     game_app.draw_available_space((1,0))
#     game_app.draw_available_space((-1,0))
#     game_app.draw_token_slot((0,0))

# app.root.after(1, lambda:
#     draw_test()
# )

# app.start()