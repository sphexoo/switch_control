import tkinter as tk
from tkinter import filedialog, simpledialog
from threading import Thread, active_count
from time import sleep
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page
from weiche import Weiche, WeichenGroup
from gleis import Gleis


class ControlPage(Page):
    def __init__(self, master, parent, serial):
        super().__init__(master, parent)
        
        self.lineWidth = 30

        self.serial = serial
        
        self.menu = tk.Menu(self.frame)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="Öffnen", command=self.loadFromJson)
        self.menu_file.add_command(label="Editor starten", command=self.parent.openEditor)
        self.menu.add_cascade(label="Datei", menu=self.menu_file)
        self.menu_customize = tk.Menu(self.menu)
        self.menu_customize.add_command(label="Linienbreite", command=self.setLineWidth)
        self.menu_customize.add_command(label="Ansicht neu laden", command=self.updateControls)
        self.menu_customize.add_command(label="Weichen initialisieren", command=self.asyncInitWeichen)
        self.menu.add_cascade(label="Bearbeiten", menu=self.menu_customize)
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
        if not directory:
            return
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
                switches = [weiche[4], weiche[5]]
                self.weichen[(weiche[0], weiche[1])] = Weiche(self.canvas, x, y, dir0, dir1, switches, self.serial)
        if "gleise" in data:
            for gleis in data["gleise"]:
                x, y = self.grid.getPosition(gleis[0], gleis[1])
                self.gleise[(gleis[0], gleis[1])] = Gleis(self.canvas, x, y, gleis[2], gleis[3])
        if "weichengroups" in data:
            for wg in data["weichengroups"]:
                self.weichengroups[tuple(wg[0])] = WeichenGroup(self.canvas, self.grid, tuple(wg[0]))
                weichen = {}
                for weiche in wg[1]:
                    weichen[tuple(weiche[0])] = weiche[1]
                self.weichengroups[tuple(wg[0])].setWeichen(weichen)

    def onMousePressed(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if (gridX, gridY) in self.weichen:
            self.weichen[(gridX, gridY)].toggle()
        elif (gridX, gridY) in self.gleise:
            groupId = self.gleise[(gridX, gridY)].getGroupId()
            for key in self.gleise:
                if key == (gridX, gridY):
                    self.gleise[key].activate()
                    if key in self.weichengroups:
                        weichen = self.weichengroups[key].getWeichen()
                        self.asyncSetWeichen(weichen)
                elif self.gleise[key].getGroupId() == groupId:
                    self.gleise[key].deactivate()

    def setLineWidth(self):
        user_input = simpledialog.askstring("Bearbeiten", "Linienbreite")
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
            x, y = self.grid.getPosition(key[0], key[1])
            self.gleise[key].updatePosition(x, y)

    def asyncInitWeichen(self):
        thread = Thread(target=self.initWeichen, daemon=True)
        thread.start()

    def initWeichen(self):
        for key in self.weichen:
            self.weichen[key].init()
            sleep(0.1)

    def asyncSetWeichen(self, keys_and_states):
        thread = Thread(target=self.setWeichen, daemon=True, args=(keys_and_states,))
        thread.start()

    def setWeichen(self, keys_and_states):
        for key in keys_and_states:
            self.weichen[key].setState(keys_and_states[key])
            sleep(0.1)