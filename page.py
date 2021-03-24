import tkinter as tk


class Page():
    def __init__(self, master, parent):
        self.parent = parent
        self.master = master
        self.frame = tk.Frame(master)

        self.lines = {}
        self.weichen = {}
        self.gleise = {}

    def show(self):
        self.master.config(menu=self.menu)
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        pass

    def onResize(self, event):
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new

    def clearCanvas(self):
        # delete current line objects from canvas
        for key in self.lines:
            self.lines[key].delete()
        for key in self.weichen:
            self.weichen[key].delete()
        for key in self.gleise:
            self.gleise[key].delete()
        self.lines = {}
        self.weichen = {}
        self.gleise = {}