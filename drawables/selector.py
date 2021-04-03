from drawables import Drawable

class Selector(Drawable):
    def __init__(self, canvas, color="black"):
        super().__init__(canvas, 0, 0, color)
        self.canvas = canvas
        self.size = 15

        self.active = False
        self.hide()
                        
    def show(self):
        self.active = True
        if len(self.ids) > 0:
            self.canvas.itemconfigure(self.ids[0], state="normal")
            self.canvas.tag_raise(self.ids[0])
    
    def hide(self):
        self.active = False
        if len(self.ids) > 0:
            self.canvas.itemconfigure(self.ids[0], state="hidden")
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        if len(self.ids) > 0:
            self.canvas.delete(self.ids[0])
        self.delete()
        self.ids.append(self.canvas.create_oval(self.x - self.size / 2,
                                                self.y - self.size / 2,
                                                self.x + self.size / 2,
                                                self.y + self.size / 2,
                                                width=2,
                                                outline=self.color))
        self.show()
    
    def isActive(self):
        return self.active
    
    def getPosition(self):
        return self.x, self.y

    
