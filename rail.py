class Rail:
    def __init__(self, x, y, weichen):
        self.x = x
        self.y = y
        self.weichen = weichen
        self.state = True
        self.size = 10

    def checkHit(mX, mY):
        if mX > self.x - self.size and
           mX < self.x + self.size and
           mY > self.y - self.size and
           mY < self.y + self.size:
            self.toggle()
            return True
        return False

    def display():
        pass

    def toggle():
        self.state = not self.state
        for weiche in self.weichen:
            weiche.toggle()
 