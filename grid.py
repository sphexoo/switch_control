import math

class Grid:
    def __init__(self, canvas, gridX=20, gridY=10, isActive=False):
        self.canvas = canvas
        self.gridX = gridX
        self.gridY = gridY
        self.isActive = isActive
        self.canvas.update()
        self.offsetX = self.canvas.winfo_width() / (self.gridX + 1)
        self.offsetY = self.canvas.winfo_height() / (self.gridY + 1)
        self.ids = []
        if self.isActive:
            self.create()

    def create(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for x in range(self.gridX):
            pos_x = x * self.offsetX + self.offsetX
            self.ids.append(self.canvas.create_line(pos_x, 0, pos_x, height, fill="gray50"))
        for y in range(self.gridY):
            pos_y= y * self.offsetY + self.offsetY
            self.ids.append(self.canvas.create_line(0, pos_y, width, pos_y, fill="gray50"))
        for id in self.ids:
            self.canvas.addtag_withtag("all", id)
    
    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)

    def getGridPosition(self, mX, mY):
        self.canvas.update()
        self.offsetX = self.canvas.winfo_width() / (self.gridX + 1)
        self.offsetY = self.canvas.winfo_height() / (self.gridY + 1)
        gridX = round(mX / self.offsetX)
        gridY = round(mY / self.offsetY)
        return gridX, gridY
    
    def getPosition(self, gridX, gridY):
        return self.offsetX * gridX, self.offsetY * gridY

    def onResize(self, width, height):
        self.offsetX = width / (self.gridX + 1)
        self.offsetY = height / (self.gridY + 1)

    def setGridX(self, gridX):
        self.gridX = gridX
        self.offsetX = self.canvas.winfo_width() / (self.gridX + 1)

    def setGridY(self, gridY):
        self.gridY = gridY
        self.offsetY = self.canvas.winfo_height() / (self.gridY + 1)

    def getIsActive(self):
        return self.isActive
    
    def getGridX(self):
        return self.gridX
    
    def getGridY(self):
        return self.gridY

    def update(self):
        self.canvas.update()