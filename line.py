class Line():
    def __init__(self, canvas, grid, numX0, numY0, numX1, numY1):
        self.canvas = canvas
        self.grid = grid
        self.numX0 = numX0
        self.numY0 = numY0
        self.numX1 = numX1
        self.numY1 = numY1
        self.width = 30

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x0 = numX0 / self.grid.getDimX() * width
        y0 = numY0 / self.grid.getDimY() * height
        x1 = numX1 / self.grid.getDimX() * width
        y1 = numY1 / self.grid.getDimY() * height

        self.ids = [ self.canvas.create_line(x0, y0, x1, y1, width=self.width),
                    self.canvas.create_oval(x0 - self.width / 2, y0 - self.width / 2, x0 + self.width / 2, y0 + self.width / 2, fill="black"),
                    self.canvas.create_oval(x1 - self.width / 2, y1 - self.width / 2, x1 + self.width / 2, y1 + self.width / 2, fill="black") ]

    def getPoints(self):
        return [self.numX0, self.numY0, self.numX1, self.numY1]

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []