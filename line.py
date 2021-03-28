import tkinter as tk
from drawable import Drawable

class Line(Drawable):
    def __init__(self, canvas, x0, y0, x1, y1, color, width=30):
        super().__init__(canvas, x0, y0, color)
        self.x1 = x1
        self.y1 = y1
        self.width = width    
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x1, self.y1, width=self.width, capstyle=tk.ROUND, fill=self.color))

    def setPosition(self, x0, y0, x1, y1):
        self.x = x0
        self.y = y0
        self.x1 = x1
        self.y1 = y1
        self.display()