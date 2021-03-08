import math

class Grid:
    def __init__(self, canvas, numX, numY):
        self.canvas = canvas
        self.numX = numX
        self.numY = numY
        self.canvas.update()
        self.offsetX = self.canvas.winfo_width() / (numX + 1)
        self.offsetY = self.canvas.winfo_height() / (numY + 1)
        self.ids = []
        self.create()

    def create(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for x in range(self.numX):
            pos_x = x * self.offsetX + self.offsetX
            self.ids.append(self.canvas.create_line(pos_x, 0, pos_x, height, fill="gray50"))
        for y in range(self.numY):
            pos_y= y * self.offsetY + self.offsetY
            self.ids.append(self.canvas.create_line(0, pos_y, width, pos_y, fill="gray50"))
        for id in self.ids:
            self.canvas.addtag_withtag("all", id)
    
    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
            
    def getGridCoords(self, mX, mY):
        self.offsetX = self.canvas.winfo_width() / (self.numX + 1)
        self.offsetY = self.canvas.winfo_height() / (self.numY + 1)
        stepsX = round(mX / self.offsetX)
        stepsY = round(mY / self.offsetY)
        return stepsX * self.offsetX, stepsY * self.offsetY

    def getGridNums(self, mX, mY):
        self.offsetX = self.canvas.winfo_width() / (self.numX + 1)
        self.offsetY = self.canvas.winfo_height() / (self.numY + 1)
        numX = round(mX / self.offsetX)
        numY = round(mY / self.offsetY)
        return numX, numY

    def getDimensions(self):
        return [self.numX + 1, self.numY + 1]

    def getPosition(self, mX, mY):
        numX, numY = self.getGridNums(mX, mY)
        return self.offsetX * numX, self.offsetY * numY
    
    def getPositionFromNum(self, numX, numY):
        return self.offsetX * numX, self.offsetY * numY

    def onResize(self, width, height):
        self.offsetX = width / (self.numX + 1)
        self.offsetY = height / (self.numY + 1)

    def setGridX(self, gridX):
        self.numX = gridX
        self.offsetX = self.canvas.winfo_width() / (self.numX + 1)

    def setGridY(self, gridY):
        self.numY = gridY
        self.offsetY = self.canvas.winfo_height() / (self.numY + 1)
