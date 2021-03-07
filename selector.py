class Selector():
    def __init__(self, canvas, grid, color="black"):
        self.canvas = canvas
        self.grid = grid
        self.posX = 0
        self.posY = 0
        self.size = 25
        self.color = color

        self.id = None
        self.active = False
        self.hide()
                        
    def show(self):
        self.active = True
        self.canvas.itemconfigure(self.id, state="normal")
        self.canvas.tag_raise(self.id)
    
    def hide(self):
        self.active = False
        self.canvas.itemconfigure(self.id, state="hidden")
    
    def setPosition(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(posX - self.size / 2,
                                            posY - self.size / 2,
                                            posX + self.size / 2,
                                            posY + self.size / 2,
                                            width=2,
                                            outline=self.color)
        self.canvas.addtag_withtag("all", self.id)
        self.show()
    
    def isActive(self):
        return self.active
    
    def getPosition(self):
        return self.posX, self.posY

    
