import tkinter as tk
from window import Window


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Weichensteuerung")
    root.update()
    app = Window(root)
    app.mainloop()

