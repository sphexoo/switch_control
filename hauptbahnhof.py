import tkinter as tk
from button import Button
from grid import Grid

class Hauptbahnhof():
    def __init__(self, master, width, height):
        super().__init__(master, width, height)
        
        self.grid = Grid(self, 5, 5, 50, 75)
        self.grid.draw()

