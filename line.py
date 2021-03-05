class Line():
    def __init__(self, canvas, startX, startY, endX, endY):
        self.canvas = canvas
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.width = 30
        self.ids = [ self.canvas.create_line(startX, startY, endX, endY, width=self.width),
                    self.canvas.create_oval(startX - self.width / 2, startY - self.width / 2, startX + self.width / 2, startY + self.width / 2, fill="black"),
                    self.canvas.create_oval(endX - self.width / 2, endY - self.width / 2, endX + self.width / 2, endY + self.width / 2, fill="black") ]

    def getPoints(self):
        return [self.startX, self.startY, self.endX, self.endY]

    def delete(self):
        for id in self.ids:
            self.canvas.delete(id)
        self.ids = []