import math

class Grid:
    def __init__(self, master, numX, numY):
        self.master = master
        self.numX = numX
        self.numY = numY
        self.master.update()
        self.offsetX = self.master.winfo_width() / (numX + 1)
        self.offsetY = self.master.winfo_height() / (numY + 1)
        self.len_line = 7
        self.draw()


    def draw(self):
        for x in range(self.numX):
            for y in range(self.numY):
                pos_x = x * self.offsetX + self.offsetX
                pos_y = y * self.offsetY + self.offsetY
                self.master.create_line(pos_x - self.len_line / 2, pos_y, pos_x + self.len_line / 2, pos_y, width=1, fill="black")
                self.master.create_line(pos_x, pos_y - self.len_line /  2, pos_x, pos_y + self.len_line /  2, width=1, fill="black")

    def getGridCoords(self, mX, mY):
        self.offsetX = self.master.winfo_width() / (self.numX + 1)
        self.offsetY = self.master.winfo_height() / (self.numY + 1)

        stepsX = round(mX / self.offsetX)
        stepsY = round(mY / self.offsetY)
        return (stepsX * self.offsetX, stepsY * self.offsetY)
