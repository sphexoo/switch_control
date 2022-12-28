import tkinter as tk
from drawables import Drawable

class Button(Drawable):
    def __init__(self, canvas, x, y, color, size, pinId, label, serial):
        super().__init__(canvas, x, y, color)
        self.label = label
        self.pinId = pinId
        self.state = 0
        self.size = size
        self.serial = serial
        self.display()

    def display(self):
        self.delete()
        if self.state:
            color = self.color[0]
        else:
            color = self.color[1]
        self.ids.append(self.canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill=color))
        self.ids.append(self.canvas.create_text(self.x + 15, self.y, text=self.label, anchor=tk.W))

    def toggle(self):
        if self.state == 0:
            self.state = 1
            self.canvas.itemconfig(self.ids[0], fill=self.color[0])
        else:
            self.state = 0
            self.canvas.itemconfig(self.ids[0], fill=self.color[1])
        self.sendSerial()
        self.display()

    def setSize(self, size):
        self.size = size
        self.display()
    
    def setColor(self, colorOn=None, colorOff=None):
        if colorOn:
            self.color[0] = colorOn
        if colorOff:
            self.color[1] = colorOff
        self.display()

    def sendSerial(self):
        data = 99 * 100 + self.state * 10 + self.pinId
        out = bytes(str(data), 'ascii')
        print(f"{data}")
        self.serial.write(out)


class ButtonEditor(Drawable):
    def __init__(self, canvas, x, y, pinId = 1, label = "Button"):
        super().__init__(canvas, x, y, None)
        self.state = True
        self.size = 7
        self.pinId = pinId
        self.label = label
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size, fill="green"))
        self.ids.append(self.canvas.create_text(self.x + 15, self.y, text=self.label, anchor=tk.W))
        self.ids.append(self.canvas.create_text(self.x + 15, self.y + 12, text=f"Pin ID: {self.pinId}", anchor=tk.W))

    def activate(self):
        self.state = True
        self.canvas.itemconfig(self.id, fill="green")
        for weiche in self.weichen:
            weiche.toggle()
        for gleis in self.others:
            gleis.deactivate()
    
    def deactivate(self):
        self.state = False
        self.canvas.itemconfig(self.id, fill="red")

    def getPinId(self):
        return self.pinId

    def getLabel(self):
        return self.label

    def updatePinId(self, pinId):
        self.pinId = pinId
        self.display()

    def updateLabel(self, label):
        self.label = label
        self.display()