import tkinter as tk
from editorpage import EditorPage


class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.bind("<Configure>", self.onConfigure)
        self.master.bind("<KeyPress>", self.onKeyPressed)
        self.master.bind("<Button>", self.onMousePressed)


        self.width = master.winfo_width()
        self.height = master.winfo_height()

        self.pages = {"editor": EditorPage(self.master)}
        self.current_page = self.pages["editor"]
        self.current_page.show()
        
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="Open", command=self.pages["editor"].loadFromJson)
        self.menu_file.add_command(label="Save as", command=self.pages["editor"].saveToJson)
        self.menu_file.add_command(label="Close")
        self.menu.add_cascade(label="File", menu=self.menu_file)
        self.master.config(menu=self.menu)


        #self.serial = ser.Serial(baudrate=9600, port="COM1", timeout=2)
        #print(self.serial)
        #self.serial.write_timeout(3.0)

        #self.sbhf = Schattenbahnhof(self, self.master.winfo_width(), self.master.winfo_height())
        #self.hbhf = Hauptbahnhof(self, self.master.winfo_width(), self.master.winfo_height())
        #self.nbhf = Nebenbahnhof(self, self.master.winfo_width(), self.master.winfo_height())

    def onKeyPressed(self, event):
        pass

    def onMousePressed(self, event):
        self.current_page.onMousePressed(event)

    def onConfigure(self, event):
        if self.width != self.master.winfo_width() or self.height != self.master.winfo_height():
            self.width = self.master.winfo_width()
            self.height = self.master.winfo_height()
            self.current_page.onResize(event)
        