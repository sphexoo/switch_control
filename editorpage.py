import tkinter as tk
from tkinter import filedialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page


class EditorPage(Page):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self.master,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="grey",
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.pack()
        self.grid = Grid(self.canvas, 20, 10)

        self.selector1 = Selector(self.canvas, self.grid, color="red")
        self.selector2 = Selector(self.canvas, self.grid, color="green")

        self.lines = []

        self.canvas.addtag_all("all")

    def clearLines(self):
        # delete current line objects from canvas
        for line in self.lines:
            line.delete()
        self.lines = []

    def saveToJson(self):
        # saves line data to json file
        data = {"dimensions": self.grid.getDimensions(), "lines": []}
        for line in self.lines:
            x0, y0, x1, y1 = line.getPositions()
            numX0, numX1 = self.grid.getGridNums(x0, y0)
            numY0, numY1 = self.grid.getGridNums(x1, y1)
            data["lines"].append([numX0, numX1, numY0, numY1])
        directory = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'w') as f:
            json.dump(data, f)

    def loadFromJson(self):
        # load data from file 
        directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'r') as f:
            data = json.load(f)
        self.clearLines()
        # add loaded line objects
        for line in data["lines"]:
            x0, y0 = self.grid.getPositionFromNum(line[0], line[1])
            x1, y1 = self.grid.getPositionFromNum(line[2], line[3])
            self.lines.append(Line(self.canvas, x0, y0, x1, y1))

    def onResize(self, event):
        width_old = self.canvas.winfo_width()
        height_old = self.canvas.winfo_height()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()

        self.grid.onResize(width_new, height_new)

        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / width_old, height_new / height_old)

    def onMousePressed(self, event):
        posX, posY = self.grid.getPosition(event.x, event.y)
        if (event.num == 1):
            if not self.selector1.isActive():
                self.selector1.setPosition(posX, posY)
            elif not self.selector2.isActive():
                self.selector2.setPosition(posX, posY)
            elif self.selector1.isActive() and self.selector2.isActive():
                x0, y0 = self.selector1.getPosition()
                x1, y1 = self.selector2.getPosition()
                self.lines.append(Line(self.canvas, x0, y0, x1, y1))
                self.selector1.hide()
                self.selector2.hide()
        elif (event.num == 3):
            self.selector1.hide()
            self.selector2.hide()
