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

        self.gridX = 20
        self.gridY = 10
        self.lineWidth = 10
        self.current_item = "Linie"

        self.lines = {}
        self.weichen = {}
        self.gleise = {}

        self.menu = tk.Menu(self.frame)

        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="New", command=self.clearCanvas)
        self.menu_file.add_command(label="Load", command=self.loadFromJson)
        self.menu_file.add_command(label="Save as", command=self.saveToJson)
        self.menu_file.add_command(label="Exit editor", command=self.parent.exitEditor)
        self.menu.add_cascade(label="File", menu=self.menu_file)

        self.menu_edit = tk.Menu(self.menu)
        self.menu_edit.add_command(label="Undo", command=self.undo)
        self.menu.add_cascade(label="Edit", menu=self.menu_edit)

        self.menu_customize = tk.Menu(self.menu)
        self.menu_customize.add_command(label="Grid X", command=self.setGridX)
        self.menu_customize.add_command(label="Grid Y", command=self.setGridY)
        self.menu_customize.add_command(label="Line width", command=self.setLineWidth)
        self.menu.add_cascade(label="Customize", menu=self.menu_customize)

        self.menu_insert = tk.Menu(self.menu)
        self.menu_insert.add_command(label="Linie", command=lambda: self.setCurrentItem("Linie"))
        self.menu_insert.add_command(label="Weiche", command=lambda: self.setCurrentItem("Weiche"))
        self.menu_insert.add_command(label="Gleis", command=lambda: self.setCurrentItem("Gleis"))
        self.menu.add_cascade(label="Insert", menu=self.menu_insert)

        self.master.config(menu=self.menu)

        self.canvas = tk.Canvas(self.frame,
                                width=self.master.winfo_width(),
                                height=self.master.winfo_height(),
                                bg="gray64",
                                borderwidth=0,
                                highlightthickness=0)
        
        self.canvas.pack()
        self.grid = Grid(self.canvas, self.gridX, self.gridY)

        self.canvas.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.selector1 = Selector(self.canvas, self.grid, color="red")
        self.selector2 = Selector(self.canvas, self.grid, color="green")

        self.canvas.addtag_all("all")

    def clearCanvas(self):
        # delete current line objects from canvas
        for key in self.lines:
            self.lines[key].delete()
        for key in self.weichen:
            self.weichen[key].delete()
        self.lines = {}
        self.weichen = {}

    def setCurrentItem(self, item):
        self.selector1.hide()
        self.selector2.hide()
        self.current_item = item

    def saveToJson(self):
        # saves line data to json file
        data = {"dimensions": self.grid.getDimensions(), "lines": [], "weichen": []}
        for key in self.lines:
            x0, y0, x1, y1 = self.lines[key].getPositions()
            numX0, numY0 = self.grid.getGridNums(x0, y0)
            numX1, numY1 = self.grid.getGridNums(x1, y1)
            data["lines"].append([numX0, numY0, numX1, numY1])
        for key in self.weichen:
            x, y = self.weichen[key].getPosition()
            numX, numY = self.grid.getGridNums(x, y)
            dir0, dir1 = self.weichen[key].getDirections()
            data["weichen"].append([numX, numY, dir0, dir1])

        directory = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'w') as f:
            json.dump(data, f)

    def loadFromJson(self):
        # load data from file 
        directory = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        with open(directory, 'r') as f:
            data = json.load(f)
        self.clearCanvas()
        # set grid size
        self.setGrid(gridX=data["dimensions"][0], gridY=data["dimensions"][1])
        # add loaded line objects
        if "lines" in data:
            for line in data["lines"]:
                x0, y0 = self.grid.getPositionFromNum(line[0], line[1])
                x1, y1 = self.grid.getPositionFromNum(line[2], line[3])
                self.lines[((x0, y0), (x1, y1))] = Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
        if "weichen" in data:
            for weiche in data["weichen"]:
                x, y = self.grid.getPositionFromNum(weiche[0], weiche[1])
                self.weichen[(x, y)] = WeicheEditor(self.canvas, x, y, weiche[2], weiche[3])



    def onResize(self, event):
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new

    def onMousePressed(self, event):
        if self.current_item == "Linie":
            self.placeLinie(event)
        elif self.current_item == "Weiche":
            self.placeWeiche(event)
        elif self.current_item == "Gleis":
            self.placeGleis(event)
        

    def placeLinie(self, event):
        posX, posY = self.grid.getPosition(event.x, event.y)
        if (event.num == 1):
            if not self.selector1.isActive():
                self.selector1.setPosition(posX, posY)
            elif not self.selector2.isActive():
                self.selector2.setPosition(posX, posY)
            elif self.selector1.isActive() and self.selector2.isActive():
                x0, y0 = self.selector1.getPosition()
                x1, y1 = self.selector2.getPosition()
                if not (((x0, y0), (x1, y1)) in self.lines or ((x1, y1), (x0, y0)) in self.lines):
                    self.lines[((x0, y0), (x1, y1))] = Line(self.canvas, x0, y0, x1, y1, self.lineWidth)
                self.selector1.hide()
                self.selector2.hide()
        elif (event.num == 3):
            self.selector1.hide()
            self.selector2.hide()

    def placeWeiche(self, event):
        posX, posY = self.grid.getPosition(event.x, event.y)
        if (event.num == 1):
            if not self.selector1.isActive():
                self.selector1.setPosition(posX, posY)
            elif self.selector1.isActive():
                x, y = self.selector1.getPosition()
                if not (x, y) in self.weichen:
                    self.weichen[(x, y)] = WeicheEditor(self.canvas, x, y)
                else:
                    self.weichen[(x, y)].changeDirections()
                self.selector1.hide()
        elif (event.num == 3):
            self.selector1.hide()

    def placeGleis(self, event):
        pass    

    def undo(self):
        pass
        #if len(self.lines) > 0:
        #    self.canvas.delete(self.lines[-1].getId())
        #    self.lines.pop()
    
    def setGrid(self, gridX=None, gridY=None):
        if gridX:
            self.gridX = gridX
        if gridY:
            self.gridY = gridY
        self.grid.delete()
        self.grid = Grid(self.canvas, self.gridX, self.gridY)

    def setGridX(self):
        user_input = simpledialog.askstring("Customize", "Grid X")
        if user_input and user_input.isdigit():
            gridX = int(user_input)
            self.setGrid(gridX=gridX)

    def setGridY(self):
        user_input = simpledialog.askstring("Customize", "Grid Y")
        if user_input and user_input.isdigit():
            gridY = int(user_input)
            self.setGrid(gridY=gridY)

    def setLineWidth(self):
        user_input = simpledialog.askstring("Customize", "Line width")
        if user_input and user_input.isdigit():
            width = int(user_input)
            self.lineWidth = width
            for key in self.lines:
                self.canvas.itemconfig(self.lines[key].getId(), width=self.lineWidth)