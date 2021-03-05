class Selector():
    def __init__(self, canvas, grid, color="black"):
        self.canvas = canvas
        self.grid = grid
        self.numX = 0
        self.numY = 0
        self.size = 25

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.offsetX = self.grid.getDimX() * width
        self.offsetY = self.grid.getDimY() * height

        posX = self.numX * self.offsetX
        posY = self.numY * self.offsetY

        self.id = self.canvas.create_oval(posX - self.size / 2,
                                            posY - self.size / 2,
                                            posX + self.size / 2,
                                            posY + self.size / 2,
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
    
    def moveTo(self, numX, numY):
        dX = numX - self.numX
        dY = numY - self.numY
        if self.active and dX == 0 and dY == 0:
            self.hide()
            return
        self.canvas.move(self.id, dX * self.offsetX , dY * self.offsetY)
        self.numX = numX
        self.numY = numY
        self.show()
    
    def isActive(self):
        return self.active
    
    def getPosition(self):
        return self.numX, self.numY

    
