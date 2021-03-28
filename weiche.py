from math import cos, sin, pi, radians
from time import sleep

directions = {}

class Weiche:
    def __init__(self, canvas, x, y, dir0, dir1, switches, serial):
        self.canvas = canvas
        self.serial = serial
        self.x = x
        self.y = y
        self.state = 0
        self.size = 20
        self.directions = [dir1, dir0] 
        self.switches = switches

        self.ids = []
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.size * cos(radians(self.directions[self.state])), self.y + self.size * sin(radians(self.directions[self.state])), fill="red", width=2))

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []

    def toggle(self):
        data = self.switches[self.state][0] * 100 + self.switches[self.state][1]
        out = bytes(str(data), 'ascii')
        self.serial.write(out)
        
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
        self.display()

    def setState(self, state):
        if self.state != state:
            self.state = state
            data = self.switches[self.state][0] * 100 + self.switches[self.state][1]
            out = bytes(str(data), 'ascii')
            self.serial.write(out)
            self.display()

    
    def init(self):
        self.state = 1
        data = self.switches[self.state][0] * 100 + self.switches[self.state][1]
        out = bytes(str(data), 'ascii')
        self.serial.write(out)
        self.display()

    def setSwitches(self, sw):
        self.switches = sw

    def getPosition(self):
        return self.x, self.y
    
    def getDirections(self):
        return self.directions[0], self.directions[1]
    
    def updatePosition(self, x, y):
        self.x = x
        self.y = y
        self.display()


class WeicheEditor:
    def __init__(self, canvas, x, y, dir0=0, dir1=45, sw0=[22, 23], sw1=[24, 25]):
        self.canvas = canvas
        
        self.x = x
        self.y = y
        self.size = 20
        self.directions = [dir0, dir1] 
        self.switches = [sw0, sw1]

        self.ids = []
        self.display()

    def display(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.size * cos(radians(self.directions[0])), self.y + self.size * sin(radians(self.directions[0])), fill="red", width=2))
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.size * cos(radians(self.directions[1])), self.y + self.size * sin(radians(self.directions[1])), fill="green", width=2))
        self.ids.append(self.canvas.create_text(self.x + 10, self.y + 10, text=str(self.switches[0]), fill="white"))
        self.ids.append(self.canvas.create_text(self.x + 10, self.y + 20, text=str(self.switches[1]), fill="white"))

    def changeDirections(self):
        self.directions[0] = (self.directions[0] + 45) % 360
        self.directions[1] = (self.directions[1] + 45) % 360
        self.display()

    def getPosition(self):
        return self.x, self.y
    
    def getDirections(self):
        return self.directions[0], self.directions[1]
    
    def getSwitches(self):
        return self.switches[0], self.switches[1]

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []

    def updatePosition(self, x, y):
        self.x = x
        self.y = y
        self.display()

    def updateSwitches(self, s1, s2):
        self.switches = [s1, s2]
        self.display()

class WeichenGroup:
    def __init__(self, canvas, grid, gleis):
        self.canvas = canvas
        self.grid = grid
        self.gleis = gleis
        self.weichen = {}
        self.ids = []

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

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []
    
    def getWeichen(self):
        return self.weichen
    
    def setWeichen(self, weichen):
        self.weichen = weichen
    
    def getGleis(self):
        return self.gleis

    def setGleis(self, gleis):
        self.gleis = gleis
