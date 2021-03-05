class Button:
    def __init__(self, master, x, y):
        self.master = master
        self.x = x
        self.y = y
        self.size = 10
        self.on = False

        self.rect = self.master.create_rectangle(self.x - self.size,
                                                 self.y - self.size,
                                                 self.x + self.size,
                                                 self.y + self.size, fill="red")

    def checkClick(self, mX, mY):
        if (mX > self.x - self.size and
            mX < self.x + self.size and
            mY > self.y - self.size and
            mY < self.y + self.size):
            self.onClick()

    def onClick(self):
        self.on = not self.on
        if self.on:
            self.master.itemconfig(self.rect, fill='green')
        else:
            self.master.itemconfig(self.rect, fill='red')
        print("Clicked")