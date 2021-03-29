import tkinter as tk
from editorpage import EditorPage
from controlpage import ControlPage

import serial as ser
from time import sleep
from pseudoserial import PseudoSerial


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Weichensteuerung")
        self.update()
        self.bind("<Configure>", self.onConfigure)
        self.bind("<KeyPress>", self.onKeyPressed)
        self.bind("<Button>", self.onMousePressed)
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.current_page = None
        self.current_control = 0

        try:
            self.serial = ser.Serial(baudrate=9600, port="COM3", timeout=2)
            sleep(2)
        except:
            self.serial = PseudoSerial()
        self.control_page = ControlPage(self, self.serial)
        self.editor_page = EditorPage(self)
        self.current_page = self.control_page
        self.current_page.show()

    def setPage(self, page):
        if not self.current_page == page:
            self.current_page.hide()
            self.current_page = page
            self.current_page.show()
    
    def exitEditor(self):
        self.setPage(self.control_page)
    
    def openEditor(self):
        self.setPage(self.editor_page)

    def onKeyPressed(self, event):
        if event.keysym == "Escape":
            self.attributes('-fullscreen', False)
        if self.current_page:
            self.current_page.onKeyPressed(event)

    def onMousePressed(self, event):
        if self.current_page:
            self.current_page.onMousePressed(event)

    def onConfigure(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        if self.current_page and (self.width != width or self.height != height):
            self.width = width
            self.height = height
            self.current_page.onResize(event)
        