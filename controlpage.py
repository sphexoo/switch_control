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
        self.menu.add_cascade(label="Customize", menu=self.menu_customize)
        self.master.config(menu=self.menu)

        self.canvas = tk.Canvas(self.frame,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="grey",
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
        # add loaded line objects
        dim = data["dimensions"]
        self.gridX = dim[0]
        self.gridY = dim[1]
        if "lines" in data:
            for line in data["lines"]:
                x0 = line[0] / dim[0] * self.master.winfo_width()
                y0 = line[1] / dim[1] * self.master.winfo_height()
                x1 = line[2] / dim[0] * self.master.winfo_width()
                y1 = line[3] / dim[1] * self.master.winfo_height()
                self.lines[((x0, y0), (x1, y1))] = Line(self.canvas, x0, y0, x1, y1, width=self.lineWidth)
        if "weichen" in data:
            for weiche in data["weichen"]:
                x = weiche[0]
                y = weiche[1]
                posX = x / dim[0] * self.master.winfo_width()
                posY = y / dim[1] * self.master.winfo_height()
                dir0 = weiche[2]
                dir1 = weiche[3]
                self.weichen[(x, y)] = Weiche(self.canvas, posX, posY, dir0, dir1)



    def onResize(self, event):
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new

        for x, y in self.weichen:
            posX = x / self.gridX * self.master.winfo_width()
            posY = y / self.gridY * self.master.winfo_height()
            self.weichen[(x, y)].updatePosition(posX, posY)


    def onMousePressed(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if (gridX, gridY) in self.weichen:
            self.weichen[(gridX, gridY)].toggle()


    def setLineWidth(self):
        user_input = simpledialog.askstring("Customize", "Line width")
        if user_input and user_input.isdigit():
            width = int(user_input)
            self.lineWidth = width
            for line in self.lines:
                self.canvas.itemconfig(line.getId(), width=self.lineWidth)