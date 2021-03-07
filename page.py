import tkinter as tk


class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.canvas = None

    def show(self):
        self.canvas.pack()

    def hide(self):
        self.canvas.pack_forget()

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        pass

    def onResize(self, event):
        pass