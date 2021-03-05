import tkinter as tk
from tkinter import filedialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page


class ControlPage(Page):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self.master,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="grey",
                                borderwidth=0,
                                highlightthickness=0)
        self.canvas.grid()

        self.lines = []

        self.canvas.addtag_all("all")


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
        width_old = self.canvas.winfo_width()
        height_old = self.canvas.winfo_height()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / width_old, height_new / height_old)

    def onMousePressed(self, event):
        posX, posY = self.grid.getGridCoords(event.x, event.y)
        if (event.num == 1):
            if not self.selector1.isActive():
                self.selector1.moveTo(posX, posY)
            elif not self.selector2.isActive():
                self.selector2.moveTo(posX, posY)
            elif self.selector1.isActive() and self.selector2.isActive():
                startX, startY = self.selector1.getPosition()
                endX, endY = self.selector2.getPosition()
                self.lines.append(Line(self.canvas, startX, startY, endX, endY))
                self.selector1.hide()
                self.selector2.hide()
        elif (event.num == 3):
            self.selector1.hide()
            self.selector2.hide()