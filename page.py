import tkinter as tk


class Page():
    def __init__(self, master, parent):
        self.parent = parent
        self.master = master
        self.frame = tk.Frame(master)

    def show(self):
        print(len(self.canvas.find_all()))
        self.master.config(menu=self.menu)
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        pass

    def onResize(self, event):
        pass