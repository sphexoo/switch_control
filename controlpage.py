import tkinter as tk
from tkinter import filedialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page


class ControlPage(Page):
    def __init__(self, master, parent):
        super().__init__(master, parent)
        
        self.menu = tk.Menu(self.frame)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="Load", command=self.loadFromJson)
        self.menu_file.add_command(label="Open editor", command=self.parent.openEditor)
        self.menu.add_cascade(label="File", menu=self.menu_file)
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

        self.lines = []



    def loadFromJson(self):
        # load data from file 
        directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'r') as f:
            data = json.load(f)
        # delete current line objects from canvas
        for line in self.lines:
            line.delete()
        self.lines = []
        # add loaded line objects
        dim = data["dimensions"]
        for line in data["lines"]:
            startX = line[0] / dim[0] * self.master.winfo_width()
            startY = line[1] / dim[1] * self.master.winfo_height()
            endX = line[2] / dim[0] * self.master.winfo_width()
            endY = line[3] / dim[1] * self.master.winfo_height()
            self.lines.append(Line(self.canvas, startX, startY, endX, endY))

    def onResize(self, event):
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new

    def onMousePressed(self, event):
        if (event.num == 1):
            print(event.x, event.y)