class Gleis:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.weichen = []
        self.states = []
        self.others = []
        self.state = True
        self.size = 10
        self.id = None
        self.display()

    def display(self):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_rectangle(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill='red')

    def activate(self):
        self.state = True
        self.canvas.itemconfig(self.id, fill="green")
        for weiche in self.weichen:
            weiche.toggle()
        for gleis in self.others:
            gleis.deactivate()
    
    def deactivate(self):
        self.state = False
        self.canvas.itemconfig(self.id, fill="red")
    
    def delete(self):
        self.canvas.delete(self.id)
        self.id = None
    
    def updatePosition(self, x, y):
        self.delete()
        self.x = x
        self.y = y
        self.display()


class GleisEditor:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.weichen = []
        self.states = []
        self.others = []
        self.state = True
        self.size = 10
        self.id = None
        self.display()

    def display(self):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_rectangle(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill='red')

    def activate(self):
        self.state = True
        self.canvas.itemconfig(self.id, fill="green")
        for weiche in self.weichen:
            weiche.toggle()
        for gleis in self.others:
            gleis.deactivate()
    
    def deactivate(self):
        self.state = False
        self.canvas.itemconfig(self.id, fill="red")
    
    def delete(self):
        self.canvas.delete(self.id)
        self.id = None

class GleisGroup:
    def __init__(self):
        pass

class GleisGroupEditor:
    def __init__(self):
        pass