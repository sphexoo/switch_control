from math import cos, sin, pi, radians

class Weiche:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = 0
        self.size = 20
        self.directions = [0, 45] 
        self.switches = []

        self.ids = []
        self.display()

    def checkHit(mX, mY):
        if mX > self.x - self.size and mX < self.x + self.size and mY > self.y - self.size and mY < self.y + self.size:
            self.toggle()
            return True
        return False

    def display(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.size * cos(radians(self.directions[0])), self.y + self.size * sin(radians(self.directions[0])), fill="red"))
        self.ids.append(self.canvas.create_line(self.x, self.y, self.x + self.size * cos(radians(self.directions[1])), self.y + self.size * sin(radians(self.directions[1])), fill="red"))

    def toggle():
        self.switches[self.state].toggle()
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
        
    def changeDirections(self):
        self.directions[0] = (self.directions[0] + 45) % 360
        self.directions[1] = (self.directions[1] + 45) % 360
        self.display()
        
    def setSwitches(self, sw):
        self.switches = sw
