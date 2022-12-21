import tkinter as tk
from drawables import Grid


class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.update()

        self.canvas = tk.Canvas(self,
                        width=self.master.winfo_width(),
                        height=self.master.winfo_height(),
                        bg="gray64",
                        borderwidth=0,
                        highlightthickness=0)
        self.canvas.pack()
        self.canvas.update()

        self.grid = Grid(self.canvas)

        self.lines = {}
        self.weichen = {}
        self.gleise = {}
        self.weichengroups = {}
        self.webcams = {}
        self.buttons = {}
        
    def show(self):
        self.master.config(menu=self.menu)
        self.pack()
        self.update()

    def hide(self):
        self.pack_forget()

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        pass

    def updateControls(self):
        pass

    def onResize(self, event):
        self.master.update()
        width_new = self.master.winfo_width()
        height_new = self.master.winfo_height()
        self.canvas.config(width=width_new, height=height_new)
        self.canvas.scale("all", 0, 0, width_new / self.width, height_new / self.height)
        self.width = width_new
        self.height = height_new
        self.grid.onResize()
        self.updateControls()

    def clearCanvas(self):
        # delete current line objects from canvas
        for key in self.lines:
            self.lines[key].delete()
        for key in self.weichen:
            self.weichen[key].delete()
        for key in self.gleise:
            self.gleise[key].delete()
        for key in self.weichengroups:
            self.weichengroups[key].delete()
        for key in self.webcams:
            self.webcams[key].delete()
        for key in self.buttons:
            self.buttons[key].delete()
        self.lines = {}
        self.weichen = {}
        self.gleise = {}
        self.weichengroups = {}
        self.webcams = {}
        self.buttons = {}
    
        self.master.update()
        self.canvas.update()