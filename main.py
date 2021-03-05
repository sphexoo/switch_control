import tkinter as tk
import serial as ser
from hauptbahnhof import Hauptbahnhof
from schattenbahnhof import Schattenbahnhof
from nebenbahnhof import Nebenbahnhof
from window import Window


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")
    root.update()
    app = Window(root)
    app.mainloop()
