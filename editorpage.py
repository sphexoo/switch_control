import tkinter as tk
from tkinter import filedialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page


class EditorPage(Page):
    def __init__(self, master, parent):
        super().__init__(master, parent)

        self.menu = tk.Menu(self.frame)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="New", command=self.clearLines)
        self.menu_file.add_command(label="Load", command=self.loadFromJson)
        self.menu_file.add_command(label="Save as", command=self.saveToJson)
        self.menu_file.add_command(label="Exit editor", command=self.parent.exitEditor)
        self.menu.add_cascade(label="File", menu=self.menu_file)
        self.menu_edit = tk.Menu(self.menu)
        self.menu_edit.add_command(label="Undo", command=self.undo)
        self.menu.add_cascade(label="Edit", menu=self.menu_edit)

        self.master.config(menu=self.menu)

        self.canvas = tk.Canvas(self.frame,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="gray64",
                                borderwidth=0,
                                highlightthickness=0)
        
        self.canvas.pack()
        self.grid = Grid(self.canvas, 20, 10)

        self.canvas.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

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
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new

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

    def undo(self):
        if len(self.lines) > 0:
            self.canvas.delete(self.lines[-1].getId())
            self.lines.pop()