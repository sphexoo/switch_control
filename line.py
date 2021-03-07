import tkinter as tk

class Line():
    def __init__(self, canvas, x0, y0, x1, y1):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = 30

        self.ids = [ self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, width=self.width, capstyle=tk.ROUND),
                    #self.canvas.create_oval(self.x0 - self.width / 2, self.y0 - self.width / 2, self.x0 + self.width / 2, self.y0 + self.width / 2, fill="black"),
                    #self.canvas.create_oval(self.x1 - self.width / 2, self.y1 - self.width / 2, self.x1 + self.width / 2, self.y1 + self.width / 2, fill="black") 
                    ]
        
        for id in self.ids:
            self.canvas.addtag_withtag("all", id)

    def getPositions(self):
        return self.x0, self.y0, self.x1, self.y1

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []