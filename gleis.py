class Gleis:
    def __init__(self, canvas, x, y, gleisId, groupId):
        self.canvas = canvas
        self.gleisId = gleisId
        self.groupId = groupId
        self.x = x
        self.y = y
        self.weichen = []
        self.states = []
        self.others = []
        self.state = True
        self.size = 10
        self.ids = []
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_rectangle(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill='red'))

    def activate(self):
        self.state = True
        self.canvas.itemconfig(self.ids[0], fill="green")
        for weiche in self.weichen:
            weiche.toggle()
        for gleis in self.others:
            gleis.deactivate()
    
    def deactivate(self):
        self.state = False
        self.canvas.itemconfig(self.ids[0], fill="red")
    
    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []
    
    def updatePosition(self, x, y):
        self.delete()
        self.x = x
        self.y = y
        self.display()
    
    def getGroupId(self):
        return self.groupId


class GleisEditor:
    def __init__(self, canvas, x, y, gleisId=None, groupId=None):
        self.gleisId = gleisId
        self.groupId = groupId
        self.canvas = canvas
        self.x = x
        self.y = y
        self.weichen = []
        self.states = []
        self.others = []
        self.state = True
        self.size = 7
        self.ids = []
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_rectangle(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill='red'))
        self.ids.append(self.canvas.create_text(self.x + 5, self.y - 15, text=str(self.groupId), fill="brown"))
        self.ids.append(self.canvas.create_text(self.x + 5, self.y + 15, text=str(self.gleisId), fill="purple"))

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
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []
    
    def setGroupId(self, groupId):
        self.groupId = groupId
        self.display()
    
    def getGroupId(self):
        return self.groupId
    
    def setGleisId(self, gleisId):
        self.gleisId = gleisId
        self.display()
    
    def getGleisId(self):
        return self.gleisId