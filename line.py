import tkinter as tk

class Line():
    def __init__(self, canvas, x0, y0, x1, y1, width=30):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = width

        self.id = self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, width=self.width, capstyle=tk.ROUND)
       
        self.canvas.addtag_withtag("all", self.id)

    def getPositions(self):
        return self.x0, self.y0, self.x1, self.y1

    def getId(self): 
        return self.id

    def delete(self):
        self.canvas.delete(self.id)
        self.id = None
