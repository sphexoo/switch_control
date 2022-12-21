import tkinter as tk
from tkinter import filedialog, simpledialog
import json

from drawables import *
from pages import Page


class EditorPage(Page):
    def __init__(self, master):
        super().__init__(master)

        self.lineWidth = 10
        self.current_item = "Linie"

        self.menu = tk.Menu(self)

        self.menu_file = tk.Menu(self.menu, tearoff=False)
        self.menu_file.add_command(label="Neu", command=self.clearCanvas)
        self.menu_file.add_command(label="Öffnen", command=self.loadFromJson)
        self.menu_file.add_command(label="Speichern unter", command=self.saveToJson)
        self.menu_file.add_command(label="Editor beenden", command=self.master.exitEditor)
        self.menu.add_cascade(label="Datei", menu=self.menu_file)

        self.menu_edit = tk.Menu(self.menu, tearoff=False)
        self.menu_edit.add_command(label="Raster X", command=self.setGridX)
        self.menu_edit.add_command(label="Raster Y", command=self.setGridY)
        self.menu_edit.add_command(label="Linienbreite", command=self.setLineWidth)
        self.menu_edit.add_command(label="Autoskalierung (löscht Weichengruppen)", command=self.autoscale)
        self.menu.add_cascade(label="Bearbeiten", menu=self.menu_edit)

        self.menu_insert = tk.Menu(self.menu, tearoff=False)
        self.menu_insert.add_command(label="Linie", command=lambda: self.setCurrentItem("Linie"))
        self.menu_insert.add_command(label="Weiche", command=lambda: self.setCurrentItem("Weiche"))
        self.menu_insert.add_command(label="Weichengruppe", command=lambda: self.setCurrentItem("Weichengruppe"))
        self.menu_insert.add_command(label="Gleis", command=lambda: self.setCurrentItem("Gleis"))
        self.menu_insert.add_command(label="Webcam", command=lambda: self.setCurrentItem("Webcam"))
        self.menu_insert.add_command(label="Button", command=lambda: self.setCurrentItem("Button"))
        self.menu.add_cascade(label="Einfügen (Linie)", menu=self.menu_insert)

        self.master.config(menu=self.menu)

        self.grid.display()

        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.selector1 = Selector(self.canvas, color="blue")
        self.selector2 = Selector(self.canvas, color="green")


    def setCurrentItem(self, item):
        self.selector1.hide()
        self.selector2.hide()
        self.current_item = item
        self.menu.entryconfig(3, label="Einfügen (" + self.current_item + ")")


    def saveToJson(self):
        # saves line data to json file
        data = {"dimensions": [self.grid.getGridX(), self.grid.getGridY()], "lines": [], "weichen": [], "gleise":[], "weichengroups":[], "webcams":[], "buttons":[]}
        for key in self.lines:
            data["lines"].append([key[0][0], key[0][1], key[1][0], key[1][1]])
        for key in self.weichen:
            dir0, dir1 = self.weichen[key].getDirections()
            sw0, sw1 = self.weichen[key].getSwitches()
            data["weichen"].append([key[0], key[1], dir0, dir1, sw0, sw1])
        for key in self.gleise:
            groupId = self.gleise[key].getGroupId()
            data["gleise"].append([key[0], key[1], groupId])
        for key in self.weichengroups:
            gleis = self.weichengroups[key].getGleis()
            weichen_dict = self.weichengroups[key].getWeichen()
            weichen = []
            for key, value in weichen_dict.items():
                weichen.append([key, value])
            data["weichengroups"].append([gleis, weichen])
        for key in self.webcams:
            portId = self.webcams[key].getPortId()
            data["webcams"].append([key[0][0], key[0][1], key[1][0], key[1][1], portId])
        for key in self.buttons:
            pinId = self.buttons[key].getPinId()
            label = self.buttons[key].getLabel()
            data["buttons"].append([key[0], key[1], pinId, label])

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
                self.lines[((line[0], line[1]), (line[2], line[3]))] = Line(self.canvas, x0, y0, x1, y1, width=self.lineWidth)
        if "weichen" in data:
            for weiche in data["weichen"]:
                x, y = self.grid.getPosition(weiche[0], weiche[1])
                self.weichen[(weiche[0], weiche[1])] = WeicheEditor(self.canvas, x, y, weiche[2], weiche[3], weiche[4], weiche[5])
        if "gleise" in data:
            for gleis in data["gleise"]:
                x, y = self.grid.getPosition(gleis[0], gleis[1])
                self.gleise[(gleis[0], gleis[1])] = GleisEditor(self.canvas, x, y, groupId=gleis[2])
        if "weichengroups" in data:
            for wg in data["weichengroups"]:
                self.weichengroups[tuple(wg[0])] = WeichenGroup(self.canvas, self.grid, tuple(wg[0]))
                weichen = {}
                for weiche in wg[1]:
                    weichen[tuple(weiche[0])] = weiche[1]
                self.weichengroups[tuple(wg[0])].setWeichen(weichen)
        if "webcams" in data:
            for webcam in data["webcams"]:
                x0, y0 = self.grid.getPosition(webcam[0], webcam[1])
                x1, y1 = self.grid.getPosition(webcam[2], webcam[3])
                portId = webcam[4]
                self.webcams[((webcam[0], webcam[1]), (webcam[2], webcam[3]))] = WebcamEditor(self.canvas, x0, y0, x1, y1, portId)
        if "buttons" in data:
            for button in data["buttons"]:
                x, y = self.grid.getPosition(button[0], button[1])
                pinId = button[2]
                label = button[3]
                self.buttons[(button[0], button[1])] = ButtonEditor(self.canvas, x, y, pinId, label)


    def onMousePressed(self, event):
        if not self.selector1.isActive():
            gridX, gridY = self.grid.getGridPosition(event.x, event.y)
            x, y = self.grid.getPosition(gridX, gridY)
            self.selector1.setPosition(x, y)
            return
        if self.current_item == "Linie":
            self.handleLinie(event)
        elif self.current_item == "Weiche":
            self.handleWeiche(event)
        elif self.current_item == "Gleis":
            self.handleGleis(event)
        elif self.current_item == "Weichengruppe":
            self.handleWeichengruppe(event)
        elif self.current_item == "Webcam":
            self.handleWebcam(event)
        elif self.current_item == "Button":
            self.handleButton(event)
    

    def onKeyPressed(self, event):
        if event.keysym  == "Delete":
            if not self.selector1.isActive():
                return
            self.handleDelete()
            self.selector2.hide()
        elif event.keysym == "BackSpace":
            self.selector1.hide()
            self.selector2.hide()
            
    
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
            keys_to_delete = []
            for key in self.gleise:
                if key == (gridX, gridY):
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.gleise[key].delete()
                del self.gleise[key]
        elif self.current_item == "Weichengruppe":
            if (gridX, gridY) in self.weichengroups:
                self.weichengroups[(gridX, gridY)].delete()
                del self.weichengroups[(gridX, gridY)]
        elif self.current_item == "Webcam":
            keys_to_delete = []
            for key in self.webcams:
                if (key[0] == (gridX, gridY) or key[1] == (gridX, gridY)):
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.webcams[key].delete()
                del self.webcams[key]
        elif self.current_item == "Button":
            keys_to_delete = []
            for key in self.buttons:
                if key == (gridX, gridY):
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                self.buttons[key].delete()
                del self.buttons[key]


    def handleLinie(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if event.num == 1:
            if not self.selector2.isActive():
                x, y = self.grid.getPosition(gridX, gridY)
                self.selector2.setPosition(x, y)
            elif self.selector1.isActive() and self.selector2.isActive():
                x0, y0 = self.selector1.getPosition()
                x1, y1 = self.selector2.getPosition()
                gx0, gy0 = self.grid.getGridPosition(x0, y0)
                gx1, gy1 = self.grid.getGridPosition(x1, y1)
                if not (((gx0, gy0), (gx1, gy1)) in self.lines or ((gx1, gy1), (gx0, gy0)) in self.lines):
                    self.lines[((gx0, gy0), (gx1, gy1))] = Line(self.canvas, x0, y0, x1, y1, width=self.lineWidth)
                self.selector1.hide()
                self.selector2.hide()
        elif event.num == 3:
            self.selector1.hide()
            self.selector2.hide()


    def handleWeiche(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if event.num == 1:
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
        if event.num == 1:
            x, y = self.selector1.getPosition()
            gridX, gridY = self.grid.getGridPosition(x, y)
            if (gridX, gridY) in self.gleise:
                user_input = simpledialog.askstring("Gruppe", "Gruppen ID")
                try:
                    groupId = int(user_input)
                except:
                    groupId = None
                self.gleise[(gridX, gridY)].setGroupId(groupId)
                self.selector1.hide()
                return
            self.gleise[(gridX, gridY)] = GleisEditor(self.canvas, x, y)
            self.selector1.hide()

        
    def handleWeichengruppe(self, event):
        # check if selector 1 points to a gleis
        x, y = self.selector1.getPosition()
        gridX1, gridY1 = self.grid.getGridPosition(x, y)
        isGleis = False
        for key in self.gleise:
            if key == (gridX1, gridY1):
                isGleis = True
                break
        if not isGleis:
            self.selector1.hide()
            return
        # show only connections for current weichengroup
        for key in self.weichengroups:
            self.weichengroups[key].delete()
        if (gridX1, gridY1) in self.weichengroups:
            self.weichengroups[(gridX1, gridY1)].display()
        
        if event.num == 1:
            gridX2, gridY2 = self.grid.getGridPosition(event.x, event.y)
            # check if selector 2 points to a weiche
            isWeiche = False
            for key in self.weichen:
                if key == (gridX2, gridY2):
                    isWeiche = True
                    break
            if not isWeiche:
                self.selector1.hide()
                return
            
            user_input = simpledialog.askstring("Weiche", "State [0: grün/1: rot]")
            try:
                state = int(user_input)
            except:
                state = 0
            if not (gridX1, gridY1) in self.weichengroups:
                self.weichengroups[(gridX1, gridY1)] = WeichenGroup(self.canvas, self.grid, (gridX1, gridY1))
            self.weichengroups[(gridX1, gridY1)].addWeiche((gridX2, gridY2), state)
            self.selector1.hide()
            self.selector2.hide()
        elif event.num == 3:
            self.selector1.hide()
            self.selector2.hide()
    

    def handleWebcam(self, event):
        gridX, gridY = self.grid.getGridPosition(event.x, event.y)
        if event.num == 1:
            isWebcam = False
            for key1, key2 in self.webcams:
                if key1 == (gridX, gridY):
                    isWebcam = True
                    key = (key1, key2)
                    break
            if isWebcam:
                user_input = simpledialog.askstring("Webcam", "Port [0, 1, 2, ...]")
                try:
                    portId = int(user_input)
                except:
                    portId = 0
                self.webcams[key].setPortId(portId)
                self.selector1.hide()
                self.selector2.hide()
            elif not self.selector2.isActive():
                x, y = self.grid.getPosition(gridX, gridY)
                self.selector2.setPosition(x, y)
            elif self.selector1.isActive() and self.selector2.isActive():
                x0, y0 = self.selector1.getPosition()
                x1, y1 = self.selector2.getPosition()
                gx0, gy0 = self.grid.getGridPosition(x0, y0)
                gx1, gy1 = self.grid.getGridPosition(x1, y1)
                if not (((gx0, gy0), (gx1, gy1)) in self.webcams or ((gx1, gy1), (gx0, gy0)) in self.webcams):
                    self.webcams[((gx0, gy0), (gx1, gy1))] = WebcamEditor(self.canvas, x0, y0, x1, y1)
                self.selector1.hide()
                self.selector2.hide()
        elif event.num == 3:
            self.selector1.hide()
            self.selector2.hide()

    def handleButton(self, event):
            gridX, gridY = self.grid.getGridPosition(event.x, event.y)
            if event.num == 1:
                x, y = self.selector1.getPosition()
                gridX, gridY = self.grid.getGridPosition(x, y)
                if (gridX, gridY) in self.buttons:
                    return
                self.buttons[(gridX, gridY)] = ButtonEditor(self.canvas, x, y)
                self.selector1.hide()
            elif event.num == 3:
                if (gridX, gridY) in self.buttons:
                    in0 = simpledialog.askstring("Arduino pin", "Pin ID")
                    in1 = simpledialog.askstring("Button label", "Label")
                    try:
                        pinId = int(in0)
                        label = in1
                    except:
                        pinId = 1
                        label = "Button"
                    self.buttons[(gridX, gridY)].updatePinId(pinId)
                    self.buttons[(gridX, gridY)].updateLabel(label)
                self.selector1.hide()


    def setGrid(self, gridX=None, gridY=None):
        if not gridX:
            gridX = self.grid.getGridX()
        if not gridY:
            gridY = self.grid.getGridY()
        self.grid.delete()
        self.grid = Grid(self.canvas, gridX, gridY)
        self.grid.display()


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
                self.canvas.itemconfig(self.lines[key].getIds(), width=self.lineWidth)


    def autoscale(self):
        """ Resize grid to fit all currently drawn objects. """
        # find minimum grid indices
        minX = self.grid.getGridX()
        minY = self.grid.getGridY()
        for key in self.lines:
            for (x, y) in key:
                if x < minX:
                    minX = x
                if y < minY:
                    minY = y
        # move objects to top right of grid space
        tmp = {}
        for key in self.lines:
            x0, y0 = self.grid.getPosition(key[0][0] - minX + 1, key[0][1]- minY + 1)
            x1, y1 = self.grid.getPosition(key[1][0] - minX + 1, key[1][1]- minY + 1)
            self.lines[key].setPosition(x0, y0, x1, y1)
            tmp[((key[0][0] - minX + 1, key[0][1] - minY + 1), (key[1][0] - minX + 1, key[1][1] - minY + 1))] = self.lines[key]
        self.lines = tmp
        tmp = {}
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0] - minX + 1, key[1]- minY + 1)
            self.weichen[key].setPosition(x, y)
            tmp[(key[0] - minX + 1, key[1] - minY + 1)] = self.weichen[key]
        self.weichen = tmp
        tmp = {}
        for key in self.gleise:
            x, y = self.grid.getPosition(key[0] - minX + 1, key[1]- minY + 1)
            self.gleise[key].setPosition(x, y)
            tmp[(key[0] - minX + 1, key[1] - minY + 1)] = self.gleise[key]
        self.gleise = tmp
        # find maximum grid indices
        maxX = 0
        maxY = 0
        for points in self.lines:
            for (x, y) in points:
                if x > maxX:
                    maxX = x
                if y > maxY:
                    maxY = y
        # cut empty grid space at bottom right
        self.setGrid(gridX=maxX, gridY = maxY)
        # reposition objects on new grid
        tmp = {}
        for key in self.lines:
            x0, y0 = self.grid.getPosition(key[0][0], key[0][1])
            x1, y1 = self.grid.getPosition(key[1][0], key[1][1])
            self.lines[key].setPosition(x0, y0, x1, y1)
            tmp[key] = self.lines[key]
        self.lines = tmp
        tmp = {}
        for key in self.weichen:
            x, y = self.grid.getPosition(key[0], key[1])
            self.weichen[key].setPosition(x, y)
            tmp[key] = self.weichen[key]
        self.weichen = tmp
        tmp = {}
        for key in self.gleise:
            x, y = self.grid.getPosition(key[0], key[1])
            self.gleise[key].setPosition(x, y)
            tmp[key] = self.gleise[key]
        self.gleise = tmp
        # delete weichengroups (TODO: make weichengroups resize with autoscale)
        for key in self.weichengroups:
            self.weichengroups[key].delete()
        self.weichengroups = {}
        # delete buttons (TODO: make buttons resize with autoscale)
        for key in self.buttons:
            self.buttons[key].delete()
        self.buttons = {}
        