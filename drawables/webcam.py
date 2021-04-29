from drawables import Drawable
from threading import Thread
from time import sleep

# pip install Image
import PIL
from PIL import Image,ImageTk
# pip install opencv-python
import cv2
import tkinter as tk

class Webcam(Drawable):
    def __init__(self, canvas, x0, y0, x1, y1, portId):
        super().__init__(canvas, x0, y0, None)
        self.portId = portId
        self.x1 = x1
        self.y1 = y1
        self.width = int(self.x1 - self.x)
        self.height = int(self.y1 - self.y)
        self.label = tk.Label(self.canvas)
        self.init()
        self.display()
        self.isActive = True
        self.asyncUpdate()
    
    def __del__(self):
        self.isActive = False
        self.cam.release()

    def init(self):
        self.cam = cv2.VideoCapture(self.portId, cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_window(self.x, self.y, window=self.label, anchor='nw'))

    def update(self):
        while self.isActive:
            _, frame = self.cam.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.resize(frame, dsize=(self.width, self.height), interpolation = cv2.INTER_LINEAR)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            self.label.configure(image=imgtk)
            self.label.imgtk = imgtk

    def asyncUpdate(self):
        thread = Thread(target=self.update, daemon=True)
        thread.start()

    
    def setPosition(self, x0, y0, x1, y1):
        self.x = x0
        self.y = y0
        self.x1 = x1
        self.y1 = y1
        self.width = int(self.x1 - self.x)
        self.height = int(self.y1 - self.y)



class WebcamEditor(Drawable):
    def __init__(self, canvas, x0, y0, x1, y1, portId=0):
        super().__init__(canvas, x0, y0, None)
        self.portId = portId
        self.x1 = x1
        self.y1 = y1
        self.display()

    def display(self):
        self.delete()
        self.ids.append(self.canvas.create_rectangle(self.x, self.y, self.x1, self.y1, width=2, fill=self.color))
        self.ids.append(self.canvas.create_text(self.x + 10, self.y + 10, text=str(self.portId), fill="black"))

    def setPosition(self, x0, y0, x1, y1):
        self.x = x0
        self.y = y0
        self.x1 = x1
        self.y1 = y1
        self.display()

    def getPortId(self):
        return self.portId
    
    def setPortId(self, portId):
        self.portId = portId
        self.display()

