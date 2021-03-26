import tkinter as tk
from tkinter import filedialog, simpledialog
import json
from grid import Grid
from selector import Selector
from line import Line
from page import Page
from weiche import WeicheEditor


class EditorPage(Page):
    def __init__(self, master, parent):
        super().__init__(master, parent)

        self.lineWidth = 10
        self.current_item = "Linie"

        self.menu = tk.Menu(self.frame)

        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="Neu", command=self.clearCanvas)
        self.menu_file.add_command(label="Öffnen", command=self.loadFromJson)
        self.menu_file.add_command(label="Speichern unter", command=self.saveToJson)
        self.menu_file.add_command(label="Editor beenden", command=self.parent.exitEditor)
        self.menu.add_cascade(label="Datei", menu=self.menu_file)

        self.menu_edit = tk.Menu(self.menu)
        self.menu_edit.add_command(label="Rückgängig", command=self.undo)
        self.menu_edit.add_command(label="Raster X", command=self.setGridX)
        self.menu_edit.add_command(label="Raster Y", command=self.setGridY)
        self.menu_edit.add_command(label="Linienbreite", command=self.setLineWidth)
        self.menu_edit.add_command(label="Autoskalierung", command=self.autoscale)
        self.menu.add_cascade(label="Bearbeiten", menu=self.menu_edit)

        self.menu_insert = tk.Menu(self.menu)
        self.menu_insert.add_command(label="Linie", command=lambda: self.setCurrentItem("Linie"))
        self.menu_insert.add_command(label="Weiche", command=lambda: self.setCurrentItem("Weiche"))
        self.menu_insert.add_command(label="Gleis", command=lambda: self.setCurrentItem("Gleis"))
        self.menu.add_cascade(label="Einfügen", menu=self.menu_insert)

        self.master.config(menu=self.menu)

        self.canvas = tk.Canvas(self.frame,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="gray64",
                                borderwidth=0,
                                highlightthickness=0)
        
        self.canvas.pack()
        self.grid = Grid(self.canvas, isActive=True)

        self.canvas.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.selector1 = Selector(self.canvas, color="red")
        self.selector2 = Selector(self.canvas, color="green")

        self.canvas.addtag_all("all")

    def setCurrentItem(self, item):
        self.selector1.hide()
        self.selector2.hide()
        self.current_item = item

    def saveToJson(self):
        # saves line data to json file
        data = {"dimensions": [self.grid.getGridX(), self.grid.getGridY()], "lines": [], "weichen": []}
        for key in self.lines:
            data["lines"].append([key[0][0], key[0][1], key[1][0], key[1][1]])
        for key in self.weichen:
            dir0, dir1 = self.weichen[key].getDirections()
            sw0, sw1 = self.weichen[key].getSwitches()
            data["weichen"].append([key[0], key[1], dir0, dir1, sw0, sw1])

        directory = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'w') as f:
            json.dump(data, f)

    def loadFromJson(self):
        # load data from file 
        directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not directory:
            return
        with open(directory, 'r') as f:
            data = json.load(f)
        self.clearCanvas()
        # set grid size
        self.setGrid(gridX=data["dimensions"][0], gridY=data["dimensions"][1])
        # add loaded line objects
        if "lines" in data:
            for line in data["lines"]:
                x0, y0 = self.grid.getPosition(line[0], line[1])
                x1, y1 = self.grid.getPosition(line[2], line[3])
                self.lines[((line[0], line[1]), (line[2], line[3]))] = Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
        if "weichen" in data:
            for weiche in data["weichen"]:
                x, y = self.grid.getPosition(weiche[0], weiche[1])
                self.weichen[(weiche[0], weiche[1])] = WeicheEditor(self.canvas, x, y, weiche[2], weiche[3], weiche[4], weiche[5])


    def onMousePressed(self, event):
        if self.current_item == "Linie":
            self.handleLinie(event)
        elif self.current_item == "Weiche":
            self.handleWeiche(event)
        elif self.current_item == "Gleis":
            self.handleGleis(event)
    
    def onKeyPressed(self, event):
        if event.keysym  == "Delete":
            if not self.selector1.isActive():
                return
            self.handleDelete()
            
        
    def handleDelete(self):
        x, y = self.selector1.getPosition()
        self.selector1.hide()
        gridX, gridY = self.grid.getGridPosition(x, y)
        if self.current_item == "Linie":
            keys_to_delete = []
            for key in self.lines:
                if (key[0] == (gridX, gridY) or key[1] == (gridX, gridY)):
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.lines[key].delete()
                del self.lines[key]
        elif self.current_item == "Weiche":
            keys_to_delete = []
            for key in self.weichen:
                if key == (gridX, gridY):
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.weichen[key].delete()
                del self.weichen[key]
        elif self.current_item == "Gleis":
            pass


    def handleLinie(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if event.num == 1:
            if not self.selector1.isActive():
                x, y = self.grid.getPosition(gridX, gridY)
                self.selector1.setPosition(x, y)
            elif not self.selector2.isActive():
                x, y = self.grid.getPosition(gridX, gridY)
                self.selector2.setPosition(x, y)
            elif self.selector1.isActive() and self.selector2.isActive():
                x0, y0 = self.selector1.getPosition()
                x1, y1 = self.selector2.getPosition()
                gx0, gy0 = self.grid.getGridPosition(x0, y0)
                gx1, gy1 = self.grid.getGridPosition(x1, y1)
                if not (((gx0, gy0), (gx1, gy1)) in self.lines or ((gx1, gy1), (gx0, gy0)) in self.lines):
                    self.lines[((gx0, gy0), (gx1, gy1))] = Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
                self.selector1.hide()
                self.selector2.hide()
        elif event.num == 3:
            self.selector1.hide()
            self.selector2.hide()


    def handleWeiche(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if event.num == 1:
            if not self.selector1.isActive():
                x, y = self.grid.getPosition(gridX, gridY)
                self.selector1.setPosition(x, y)
                return
            x, y = self.selector1.getPosition()
            gridX, gridY = self.grid.getGridPosition(x, y)
            if (gridX, gridY) in self.weichen:
                self.weichen[(gridX, gridY)].changeDirections()
                return
            self.weichen[(gridX, gridY)] = WeicheEditor(self.canvas, x, y)
            self.selector1.hide()
        elif event.num == 3:
            if (gridX, gridY) in self.weichen:
                in0 = simpledialog.askstring("Schalter 1 von 2", "Pin 1")
                in1 = simpledialog.askstring("Schalter 1 von 2", "Pin 2")
                in2 = simpledialog.askstring("Schalter 2 von 2", "Pin 1")
                in3 = simpledialog.askstring("Schalter 2 von 2", "Pin 2")
                try:
                    s0 = [int(in0), int(in1)]
                    s1 = [int(in2), int(in3)]
                except:
                    s0 = [22, 23]
                    s1 = [24, 25]
                self.weichen[(gridX, gridY)].updateSwitches(s0, s1)
            self.selector1.hide()

    def handleGleis(self, event):
        pass    

    def undo(self):
        pass
        #if len(self.lines) > 0:
        #    self.canvas.delete(self.lines[-1].getId())
        #    self.lines.pop()
    
    def setGrid(self, gridX=None, gridY=None):
        if not gridX:
            gridX = self.grid.getGridX()
        if not gridY:
            gridY = self.grid.getGridY()
        isActive = self.grid.getIsActive()
        self.grid.delete()
        self.grid = Grid(self.canvas, gridX, gridY, isActive=isActive)

    def setGridX(self):
        user_input = simpledialog.askstring("Bearbeiten", "Raster X")
        if user_input and user_input.isdigit():
            gridX = int(user_input)
            self.setGrid(gridX=gridX)

    def setGridY(self):
        user_input = simpledialog.askstring("Bearbeiten", "Raster Y")
        if user_input and user_input.isdigit():
            gridY = int(user_input)
            self.setGrid(gridY=gridY)

    def setLineWidth(self):
        user_input = simpledialog.askstring("Bearbeiten", "Linienbreite")
        if user_input and user_input.isdigit():
            width = int(user_input)
            self.lineWidth = width
            for key in self.lines:
                self.canvas.itemconfig(self.lines[key].getId(), width=self.lineWidth)

    def autoscale(self):
        """ Resize grid to fit all currently drawn objects. """
        minX = self.grid.getGridX()
        minY = self.grid.getGridY()
        for key in self.lines:
            for (x, y) in key:
                if x < minX:
                    minX = x
                if y < minY:
                    minY = y
        
        tmp = {}
        for key in self.lines:
            #self.lines[key].delete()
            x0, y0 = self.grid.getPosition(key[0][0] - minX + 1, key[0][1]- minY + 1)
            x1, y1 = self.grid.getPosition(key[1][0] - minX + 1, key[1][1]- minY + 1)
            self.lines[key].updatePosition(x0, y0, x1, y1)
            tmp[((key[0][0] - minX + 1, key[0][1] - minY + 1), (key[1][0] - minX + 1, key[1][1] - minY + 1))] = self.lines[key] #Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
        self.lines = tmp
        tmp = {}
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0] - minX + 1, key[1]- minY + 1)
            self.weichen[key].updatePosition(x, y)
            tmp[(key[0] - minX + 1, key[1] - minY + 1)] = self.weichen[key]
            #self.weichen[key].delete()
        self.weichen = tmp

        maxX = 0
        maxY = 0
        for points in self.lines:
            for (x, y) in points:
                if x > maxX:
                    maxX = x
                if y > maxY:
                    maxY = y
        
        self.setGrid(gridX=maxX, gridY = maxY)
        tmp = {}
        for key in self.lines:
            x0, y0 = self.grid.getPosition(key[0][0], key[0][1])
            x1, y1 = self.grid.getPosition(key[1][0], key[1][1])
            self.lines[key].updatePosition(x0, y0, x1, y1)# = Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
            tmp[key] = self.lines[key]
        self.lines = tmp
        tmp = {}
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0], key[1])
            self.weichen[key].updatePosition(x, y)
            tmp[key] = self.weichen[key]
        self.weichen = tmp
        


