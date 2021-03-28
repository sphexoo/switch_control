class Drawable():
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ids = []
        
    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []

    def getPosition(self):
        return self.x, self.y

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.display()