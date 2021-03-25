import tkinter as tk
from tkinter import filedialog, simpledialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page
from weiche import Weiche


class ControlPage(Page):
    def __init__(self, master, parent):
        super().__init__(master, parent)
        
        self.lineWidth = 30
        
        self.menu = tk.Menu(self.frame)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="Load", command=self.loadFromJson)
        self.menu_file.add_command(label="Open editor", command=self.parent.openEditor)
        self.menu.add_cascade(label="File", menu=self.menu_file)
        self.menu_customize = tk.Menu(self.menu)
        self.menu_customize.add_command(label="Set line width", command=self.setLineWidth)
        self.menu_customize.add_command(label="Update controls", command=self.updateControls)
        self.menu.add_cascade(label="Customize", menu=self.menu_customize)
        self.master.config(menu=self.menu)

        self.canvas = tk.Canvas(self.frame,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="gray64",
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.pack()

        self.canvas.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.grid = Grid(self.canvas)


    def loadFromJson(self):
        # load data from file 
        directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'r') as f:
            data = json.load(f)
        self.clearCanvas()
        self.setGrid(gridX=data["dimensions"][0], gridY=data["dimensions"][1])
        if "lines" in data:
            for line in data["lines"]:

                x0, y0 = self.grid.getPosition(line[0], line[1])
                x1, y1 = self.grid.getPosition(line[2], line[3])
                self.lines[((line[0], line[1]), (line[2], line[3]))] = Line(self.canvas, x0, y0, x1, y1, width=self.lineWidth)
        if "weichen" in data:
            for weiche in data["weichen"]:
                x, y = self.grid.getPosition(weiche[0], weiche[1])
                dir0 = weiche[2]
                dir1 = weiche[3]
                # TODO: create switches
                self.weichen[(weiche[0], weiche[1])] = Weiche(self.canvas, x, y, dir0, dir1, None)


    def onMousePressed(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if (gridX, gridY) in self.weichen:
            self.weichen[(gridX, gridY)].toggle()


    def setLineWidth(self):
        user_input = simpledialog.askstring("Customize", "Line width")
        if user_input and user_input.isdigit():
            width = int(user_input)
            self.lineWidth = width
            for key in self.lines:
                self.canvas.itemconfig(self.lines[key].getId(), width=self.lineWidth)

    def setGrid(self, gridX=None, gridY=None):
        if not gridX:
            gridX = self.grid.getGridX()
        if not gridY:
            gridY = self.grid.getGridY()
        isActive = self.grid.getIsActive()
        self.grid.delete()
        self.grid = Grid(self.canvas, gridX, gridY, isActive=isActive)

    def updateControls(self):
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0], key[1])
            self.weichen[key].updatePosition(x, y)
        for key in self.gleise:
            pass