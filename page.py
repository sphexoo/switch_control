import tkinter as tk


class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

    def show(self):
        self.pack()

    def hide(self):
        self.pack_forget()

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        pass

    def onResize(self, event):
        pass