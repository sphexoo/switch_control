import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import colorchooser
from threading import Thread, active_count
from time import sleep
import json

from drawables import *
from pages import Page


class ControlPage(Page):
    def __init__(self, master, serial):
        super().__init__(master)
        self.cfg = {}
        self.loadView() # defaults to default view if cfg.json is not found

        self.serial = serial
        self.fullscreen = True

        if self.cfg["enableGrid"]:
            self.grid.display()
        
        self.menu = tk.Menu(self)

        self.menu_file = tk.Menu(self.menu, tearoff=False)
        self.menu_file.add_command(label="Öffnen", command=self.loadFromJson)
        self.menu_file.add_command(label="Editor starten", command=self.master.openEditor)
        self.menu.add_cascade(label="Datei", menu=self.menu_file)

        self.menu_customize = tk.Menu(self.menu, tearoff=False)
        self.menu_customize.add_command(label="Ansicht neu laden", command=self.updateControls)
        self.menu_customize.add_command(label="Weichen initialisieren", command=self.asyncInitWeichen)
        self.menu.add_cascade(label="Bearbeiten", menu=self.menu_customize)

        self.menu_view = tk.Menu(self.menu, tearoff=False)

        self.menu_view.add_command(label="Vollbild", command=self.setFullscreen)
        self.menu_view.insert_separator(1)
        self.menu_view.add_command(label="Ansicht speichern", command=self.saveView)

        self.menu_view.add_command(label="Raster EIN/AUS", command=self.toggleGrid)

        self.menu_view_line = tk.Menu(self.menu_view, tearoff=False)
        self.menu_view_line.add_command(label="Breite", command=self.setLineWidth)
        self.menu_view_line.add_command(label="Farbe", command=self.setLineColor)
        self.menu_view.add_cascade(label="Linien", menu=self.menu_view_line)

        self.menu_view_weiche = tk.Menu(self.menu_view, tearoff=False)
        self.menu_view_weiche.add_command(label="Breite", command=self.setWeicheWidth)
        self.menu_view_weiche.add_command(label="Länge", command=self.setWeicheLength)
        self.menu_view_weiche.add_command(label="Farbe", command=self.setWeicheColor)
        self.menu_view.add_cascade(label="Weichen", menu=self.menu_view_weiche)
        
        self.menu_view_gleis = tk.Menu(self.menu_view, tearoff=False)
        self.menu_view_gleis.add_command(label="Größe", command=self.setGleisSize)
        self.menu_view_gleis.add_command(label="Farbe aktiv", command=self.setGleisColorOn)
        self.menu_view_gleis.add_command(label="Farbe inaktiv", command=self.setGleisColorOff)
        self.menu_view.add_cascade(label="Gleise", menu=self.menu_view_gleis)

        self.menu_view_background = tk.Menu(self.menu_view, tearoff=False)
        self.menu_view_background.add_command(label="Farbe", command=self.setBackgroundColor)
        self.menu_view.add_cascade(label="Hintergrund", menu=self.menu_view_background)

        self.menu.add_cascade(label="Ansicht", menu=self.menu_view)

        self.master.config(menu=self.menu)

        self.canvas.configure(bg=self.cfg["backgroundColor"])

        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        if self.cfg["standardDir"]:
            try:
                self.loadFromJson(self.cfg["standardDir"])
            except FileNotFoundError:
                pass


    def setDefaultView(self):
        self.cfg["lineWidth"] = 20
        self.cfg["lineColor"] = "#000000"
        self.cfg["weicheWidth"] = 2
        self.cfg["weicheLength"] = 20
        self.cfg["weicheColor"] = "#ff0000"
        self.cfg["gleisSize"] = 10
        self.cfg["gleisColor"] = ["#00ff00", "#ff0000"]
        self.cfg["backgroundColor"] = "#ffffff"
        self.cfg["standardDir"] = None
        self.cfg["enableGrid"] = False


    def saveView(self):
        with open("cfg.json", "w") as f:
            json.dump(self.cfg, f)

    def loadView(self):
        try:
            with open("cfg.json", "r") as f:
                data = json.load(f)
            self.cfg["lineWidth"] = data["lineWidth"]
            self.cfg["lineColor"] = data["lineColor"]
            self.cfg["weicheWidth"] = data["weicheWidth"]
            self.cfg["weicheLength"] = data["weicheLength"]
            self.cfg["weicheColor"] = data["weicheColor"]
            self.cfg["gleisSize"] = data["gleisSize"]
            self.cfg["gleisColor"] = data["gleisColor"]
            self.cfg["backgroundColor"] = data["backgroundColor"]
            self.cfg["standardDir"] = data["standardDir"]
            self.cfg["enableGrid"] = data["enableGrid"]
        except:
            self.setDefaultView()


    def loadFromJson(self, directory=None):
        # load data from file 
        if not directory:
            directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not directory:
            return
        with open(directory, 'r') as f:
            data = json.load(f)
        self.cfg["standardDir"] = directory
        self.clearCanvas()
        self.setGrid(gridX=data["dimensions"][0], gridY=data["dimensions"][1])
        if self.cfg["enableGrid"]:
            self.grid.display()
        if "lines" in data:
            for line in data["lines"]:
                x0, y0 = self.grid.getPosition(line[0], line[1])
                x1, y1 = self.grid.getPosition(line[2], line[3])
                self.lines[((line[0], line[1]), (line[2], line[3]))] = Line(self.canvas, x0, y0, x1, y1, color=self.cfg["lineColor"], width=self.cfg["lineWidth"])
        if "weichen" in data:
            for weiche in data["weichen"]:
                x, y = self.grid.getPosition(weiche[0], weiche[1])
                dir0 = weiche[2]
                dir1 = weiche[3]
                switches = [weiche[4], weiche[5]]
                self.weichen[(weiche[0], weiche[1])] = Weiche(self.canvas, x, y, self.cfg["weicheColor"], dir0, dir1, switches, self.serial, self.cfg["weicheLength"], self.cfg["weicheWidth"])
        if "gleise" in data:
            for gleis in data["gleise"]:
                x, y = self.grid.getPosition(gleis[0], gleis[1])
                self.gleise[(gleis[0], gleis[1])] = Gleis(self.canvas, x, y, self.cfg["gleisColor"],  gleis[2], self.cfg["gleisSize"])
        if "weichengroups" in data:
            for wg in data["weichengroups"]:
                self.weichengroups[tuple(wg[0])] = WeichenGroup(self.canvas, self.grid, tuple(wg[0]))
                weichen = {}
                for weiche in wg[1]:
                    weichen[tuple(weiche[0])] = weiche[1]
                self.weichengroups[tuple(wg[0])].setWeichen(weichen)
        self.updateControls()

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

    def setGrid(self, gridX=None, gridY=None):
        if not gridX:
            gridX = self.grid.getGridX()
        if not gridY:
            gridY = self.grid.getGridY()
        self.grid.delete()
        self.grid = Grid(self.canvas, gridX, gridY)

    def updateControls(self):
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0], key[1])
            self.weichen[key].setPosition(x, y)
        for key in self.gleise:
            x, y = self.grid.getPosition(key[0], key[1])
            self.gleise[key].setPosition(x, y)


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


    def setLineWidth(self):
        ui = simpledialog.askstring("Ansicht", "Linienbreite")
        if ui and ui.isdigit():
            print("test")
            self.cfg["lineWidth"] = int(ui)
            for key in self.lines:
                self.canvas.itemconfig(self.lines[key].getIds(), width=self.cfg["lineWidth"])

    def setLineColor(self):
        color = colorchooser.askcolor(title ="Farbe auswähen")
        if color[1]:
            self.cfg["lineColor"] = color[1]
            for key in self.lines:
                self.canvas.itemconfig(self.lines[key].getIds(), fill=self.cfg["lineColor"])

    def setWeicheWidth(self):
        ui = simpledialog.askstring("Ansicht", "Weichenbreite")
        if ui and ui.isdigit():
            self.cfg["weicheWidth"] = int(ui)
            for key in self.weichen:
                self.weichen[key].setWidth(self.cfg["weicheWidth"])
    
    def setWeicheLength(self):
        ui = simpledialog.askstring("Ansicht", "Weichenlänge")
        if ui and ui.isdigit():
            self.cfg["weicheLength"] = int(ui)
            for key in self.weichen:
                self.weichen[key].setLength(self.cfg["weicheLength"])

    
    def setWeicheColor(self):
        color = colorchooser.askcolor(title ="Farbe auswähen")
        if color[1]:
            self.cfg["weicheColor"] = color[1]
            for key in self.weichen:
                self.weichen[key].setColor(self.cfg["weicheColor"])
                self.canvas.itemconfig(self.weichen[key].getIds(), fill=self.cfg["weicheColor"])

    
    def setGleisSize(self):
        ui = simpledialog.askstring("Ansicht", "Gleisgröße")
        if ui and ui.isdigit():
            self.cfg["gleisSize"] = int(ui)
            for key in self.gleise:
                self.gleise[key].setSize(self.cfg["gleisSize"])

    def setGleisColorOn(self):
        color = colorchooser.askcolor(title ="Farbe auswähen")
        if color[1]:
            self.cfg["gleisColorOn"] = color[1]
            for key in self.gleise:
                self.gleise[key].setColor(colorOn=self.cfg["gleisColorOn"])

    def setGleisColorOff(self):
        color = colorchooser.askcolor(title ="Farbe auswähen")
        if color[1]:
            self.cfg["gleisColorOff"] = color[1]
            for key in self.gleise:
                self.gleise[key].setColor(colorOff=self.cfg["gleisColorOff"])

    def setBackgroundColor(self):
        color = colorchooser.askcolor(title ="Farbe auswähen")
        if color[1]:
            self.cfg["backgroundColor"] = color[1]
            self.canvas.configure(bg=self.cfg["backgroundColor"])

    def setFullscreen(self):
        self.master.attributes('-fullscreen', self.fullscreen)
        self.fullscreen = not self.fullscreen

    def toggleGrid(self):
        if self.cfg["enableGrid"]:
            self.grid.delete()
        else:
            self.grid.display()
        self.cfg["enableGrid"] = not self.cfg["enableGrid"]