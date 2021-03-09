class Weiche:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = 0
        self.size = 18
        self.directions = []
        self.switches = []

        self.id = self.canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill="orange")


    def checkHit(mX, mY):
        if mX > self.x - self.size and mX < self.x + self.size and mY > self.y - self.size and mY < self.y + self.size:
            self.toggle()
            return True
        return False

    def display():
        pass

    def toggle():
        self.switches[self.state].toggle()
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
        
    def setDirections(self, dirs):
        self.dirsections = dirs

    def setSwitches(self, sw):
        self.switches = sw