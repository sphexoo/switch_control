import tkinter as tk
from editorpage import EditorPage
from controlpage import ControlPage


class Window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.bind("<Configure>", self.onConfigure)
        self.master.bind("<KeyPress>", self.onKeyPressed)
        self.master.bind("<Button>", self.onMousePressed)

        self.width = master.winfo_width()
        self.height = master.winfo_height()

        self.editor = None

        self.pages = {"editor": EditorPage(self.master), "control": ControlPage(self.master)}
        self.current_page = self.pages["editor"]
        #self.current_page.show()
        
        self.menu = tk.Menu(self.master)
        self.menu_file = tk.Menu(self.menu)
        self.menu_file.add_command(label="New", command=self.pages["editor"].clearLines)
        self.menu_file.add_command(label="Load", command=self.loadFromJson)
        self.menu_file.add_command(label="Save as", command=self.pages["editor"].saveToJson)
        self.menu_file.add_command(label="Close")
        self.menu.add_cascade(label="File", menu=self.menu_file)
        self.menu_view = tk.Menu(self.menu)
        for name, page in self.pages.items():
            make_command = lambda n: lambda: self.setPage(n)
            command = make_command(name)
            self.menu_view.add_command(label=name, command=command)
        self.menu.add_cascade(label="Views", menu=self.menu_view)
        self.master.config(menu=self.menu)

        #self.serial = ser.Serial(baudrate=9600, port="COM1", timeout=2)
        #print(self.serial)
        #self.serial.write_timeout(3.0)

    def setPage(self, name):
        self.current_page.hide()
        self.current_page = self.pages[name]
        self.current_page.show()
    
    def loadFromJson(self):
        self.current_page.loadFromJson()

    def onKeyPressed(self, event):
        self.current_page.onKeyPressed(event)

    def onMousePressed(self, event):
        self.current_page.onMousePressed(event)

    def onConfigure(self, event):
        if self.width != self.master.winfo_width() or self.height != self.master.winfo_height():
            self.width = self.master.winfo_width()
            self.height = self.master.winfo_height()
            self.current_page.onResize(event)
        