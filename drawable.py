class Drawable():
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.ids = []

    def display(self):
        pass

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []

    def getPosition(self):
        return self.x, self.y

    def getIds(self): 
        return self.ids

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.display()
    
    def setColor(self, color):
        self.color = color
        self.display()