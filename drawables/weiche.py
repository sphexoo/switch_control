import tkinter as tk

from math import cos, sin, pi, radians
from time import sleep

from drawables import Drawable


class Weiche(Drawable):
    def __init__(self, canvas, x, y, color, dir0, dir1, switches, serial, length, width):
        super().__init__(canvas, x, y, color)
        self.serial = serial
        self.state = 0
        self.length = length
        self.width = width
        self.color = color
        self.directions = [dir1, dir0] 
        self.switches = switches
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.length * cos(radians(self.directions[self.state])), self.y + self.length * sin(radians(self.directions[self.state])), fill=self.color, width=self.width, capstyle=tk.ROUND))

    def toggle(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
        self.sendSerial()
        self.display()

    def setState(self, state):
        """returns True if state has changed, returns False otherwise"""
        if self.state != state:
            self.state = state
            self.sendSerial()
            self.display()
            sleep(0.2)
            return True
        return False
    
    def setWidth(self, width):
        self.width = width
        self.display()
    
    def setLength(self, length):
        self.length = length
        self.display()

    def init(self):
        self.state = 1
        self.sendSerial()
        self.display()
        sleep(0.2)
    
    def sendSerial(self):
        data = self.switches[self.state][0] * 100 + self.switches[self.state][1]
        out = bytes(str(data), 'ascii')
        print(f"{data}")
        self.serial.write(out)

    def setSwitches(self, sw):
        self.switches = sw
    
    def getDirections(self):
        return self.directions[0], self.directions[1]


class WeicheEditor(Drawable):
    def __init__(self, canvas, x, y, dir0=0, dir1=45, sw0=[22, 23], sw1=[24, 25]):
        super().__init__(canvas, x, y, None)
        self.length = 20
        self.directions = [dir0, dir1]
        self.switches = [sw0, sw1]
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.length * cos(radians(self.directions[0])), self.y + self.length * sin(radians(self.directions[0])), fill="red", width=2))
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.length * cos(radians(self.directions[1])), self.y + self.length * sin(radians(self.directions[1])), fill="green", width=2))
        self.ids.append(self.canvas.create_text(self.x + 10, self.y + 10, text=str(self.switches[0]), fill="white"))
        self.ids.append(self.canvas.create_text(self.x + 10, self.y + 20, text=str(self.switches[1]), fill="white"))

    def changeDirections(self):
        self.directions[0] = (self.directions[0] + 45) % 360
        self.directions[1] = (self.directions[1] + 45) % 360
        self.display()
    
    def getDirections(self):
        return self.directions[0], self.directions[1]
    
    def getSwitches(self):
        return self.switches[0], self.switches[1]

    def updateSwitches(self, s1, s2):
        self.switches = [s1, s2]
        self.display()


class WeichenGroup(Drawable):
    def __init__(self, canvas, grid, gleis):
        super().__init__(canvas, None, None, None)
        self.grid = grid
        self.gleis = gleis
        self.weichen = {}

    def display(self):
        self.delete()
        x0, y0 = self.grid.getPosition(self.gleis[0], self.gleis[1])
        for key in self.weichen:
            x1, y1 = self.grid.getPosition(key[0], key[1])
            self.ids.append(self.canvas.create_line(x0, y0, x1, y1, fill="orange", dash=(5,)))
            self.ids.append(self.canvas.create_text(x1, y1 - 10, fill="orange", text=self.weichen[key]))

    def addWeiche(self, key, state):
        self.weichen[key] = state
        self.display()
    
    def deleteWeiche(self, key):
        del self.weichen[key]
        self.display()
    
    def getWeichen(self):
        return self.weichen
    
    def setWeichen(self, weichen):
        self.weichen = weichen
    
    def getGleis(self):
        return self.gleis

    def setGleis(self, gleis):
        self.gleis = gleis
