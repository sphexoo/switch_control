import tkinter as tk
from editorpage import EditorPage
from controlpage import ControlPage

import serial as ser
from time import sleep


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
        self.current_control = 0

        self.serial = ser.Serial(baudrate=9600, port="COM3", timeout=2)
        sleep(2)
        
        self.pages = [ControlPage(self.master, self, self.serial), ControlPage(self.master, self, self.serial)]
        self.editor_page = EditorPage(self.master, self)
        for page in self.pages:
            page.show()
            page.hide()
        self.editor_page.show()
        self.editor_page.hide()
        self.current_page = self.pages[self.current_control]
        self.current_page.show()

    def setPage(self, page):
        if not self.current_page == page:
            self.current_page.hide()
            self.current_page = page
            self.current_page.show()
    
    def exitEditor(self):
        self.setPage(self.pages[self.current_control])
    
    def openEditor(self):
        self.setPage(self.editor_page)
    
    def loadFromJson(self):
        self.current_page.loadFromJson()

    def onKeyPressed(self, event):
        if self.current_page:
            self.current_page.onKeyPressed(event)

    def onMousePressed(self, event):
        if self.current_page:
            self.current_page.onMousePressed(event)

    def onConfigure(self, event):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        if self.current_page and (self.width != width or self.height != height):
            self.width = width
            self.height = height
            self.current_page.onResize(event)
        