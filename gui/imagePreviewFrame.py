import tkinter as tk
from tkinter import filedialog, LEFT, TOP, RIGHT, BOTTOM, END, YES, HORIZONTAL, BOTH, N, S, E, W, NW, NE, SW, SE, NSEW, X, Y
import glob
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from autogreener.utils import Bbox, EventHook
from pathlib import Path



class ImagePreviewFrame(tk.Frame):
    def __init__(self, master, default):
        tk.Frame.__init__(self, master)

        # Image variables
        self.displayedPhoto = None
        
        # Set up UI widgets
        self.widgets(default)

    def widgets(self, default):
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.image_on_canvas = self.canvas.create_image(
            0, 0, anchor=NW, image= ImageTk.PhotoImage(default) )

    @property
    def image(self):
        return self.__image
    @image.setter
    def image(self, img):
        self.canvas.config(width = img.width, height = img.height)
        self.canvas.itemconfig(self.image_on_canvas, image= ImageTk.PhotoImage(img) )
    




if __name__ == '__main__':

    from PIL import Image

    img = Image.open('data/input/ss.png')

    root = tk.Tk()

    frame = ImagePreviewFrame(root, img)
    frame.pack()

    frame.image = img

    root.mainloop()