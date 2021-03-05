class Selector():
    def __init__(self, canvas, color="black"):
        self.canvas = canvas
        self.posX = 0
        self.posY = 0
        self.size = 25
        self.id = self.canvas.create_oval(self.posX - self.size / 2,
                                            self.posY - self.size / 2,
                                            self.posX + self.size / 2,
                                            self.posY + self.size / 2,
                                            width=2,
                                            outline=color)
        self.active = False
        self.hide()
                        
    def show(self):
        self.active = True
        self.canvas.itemconfigure(self.id, state="normal")
        self.canvas.tag_raise(self.id)
    
    def hide(self):
        self.active = False
        self.canvas.itemconfigure(self.id, state="hidden")
    
    def moveTo(self, posX, posY):
        dX = posX - self.posX
        dY = posY - self.posY
        if self.active and dX == 0 and dY == 0:
            self.hide()
            return
        self.canvas.move(self.id, dX , dY)
        self.posX = posX
        self.posY = posY
        print(self.posX, self.posY)
        self.show()
    
    def isActive(self):
        return self.active
    
    def getPosition(self):
        return self.posX, self.posY

    
