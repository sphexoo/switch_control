import tkinter as tk
from button import Button

class Nebenbahnhof():
    def __init__(self, master, width, height):
        super().__init__(master, width, height)
        
        self.img = tk.PhotoImage(file="images/nebenbahnhof.png")

        self.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.addButton(Button(self, 100, 110))
        self.addButton(Button(self, 100, 150))
        self.addButton(Button(self, 100, 200))
