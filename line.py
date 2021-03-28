import tkinter as tk

class Line():
    def __init__(self, canvas, x0, y0, x1, y1, width=30):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.ids = []     
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, width=self.width, capstyle=tk.ROUND))

    def getPositions(self):
        return self.x0, self.y0, self.x1, self.y1

    def getId(self): 
        return self.ids[0]

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []

    def updatePosition(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.display()