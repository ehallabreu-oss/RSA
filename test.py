import numpy as np
import tkinter as tk
import random

def rectangle_coords(
    height: float=30.0,
    length: float=80.0,
    vertical_pos: float=20.0,
    horizontal_pos: float=10.0
    ):

    x1 = horizontal_pos
    x2 = x1 + length
    y1 = 400 - vertical_pos 
    y2 = y1 - height

    return x1, y1, x2, y2

print(*rectangle_coords())


class Rectangle_test:
    def __init__(self, root):
        self.root = root
        coords = rectangle_coords()
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.canvas.create_rectangle(*coords, fill='black')


root = tk.Tk()
root.title("Rectangle Tester")
Rectangle_test(root)
root.mainloop()