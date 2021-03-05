import tkinter as tk


class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

    def show(self):
        self.lift()
