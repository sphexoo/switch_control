import tkinter as tk
import serial as ser
from window import Window


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Weichensteuerung")
    root.update()
    app = Window(root)
    app.mainloop()
