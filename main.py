import tkinter as tk
import serial as ser
from window import Window


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    root.title("Weichensteuerung")
    root.update()
    app = Window(root)
    app.mainloop()
