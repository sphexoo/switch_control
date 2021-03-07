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

        self.current_page = None
        self.pages = {"c1": ControlPage(self.master, self), "c2": ControlPage(self.master, self), "editor": None}
        self.current_page = self.pages["c1"]
        self.current_page.show()

        #self.serial = ser.Serial(baudrate=9600, port="COM1", timeout=2)
        #print(self.serial)
        #self.serial.write_timeout(3.0)

    def setPage(self, name):
        if not self.current_page == self.pages[name]:
            self.current_page.hide()
            self.current_page = self.pages[name]
            self.current_page.show()
    
    def exitEditor(self):
        del self.pages["editor"]
        self.pages["editor"] = None
        self.setPage("c1")
    
    def openEditor(self):
        self.pages["editor"] = EditorPage(self.master, self)
        self.setPage("editor")
    
    def loadFromJson(self):
        self.current_page.loadFromJson()

    def onKeyPressed(self, event):
        if self.current_page:
            self.current_page.onKeyPressed(event)

    def onMousePressed(self, event):
        if self.current_page:
            self.current_page.onMousePressed(event)

    def onConfigure(self, event):
        if self.current_page and (self.width != self.master.winfo_width() or self.height != self.master.winfo_height()):
            self.width = self.master.winfo_width()
            self.height = self.master.winfo_height()
            self.current_page.onResize(event)
        