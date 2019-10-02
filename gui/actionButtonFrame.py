import tkinter as tk
from tkinter import filedialog, LEFT, TOP, RIGHT, BOTTOM, END, YES, HORIZONTAL, BOTH, N, S, E, W, NW, NE, SW, SE, NSEW, X, Y
import glob
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from autogreener.utils import Bbox, EventHook
from pathlib import Path

class ActionButtonFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master)
        for kwarg in kwargs.items():
            newButton = tk.Button(
                self,
                text=kwarg[0].replace('_', ' '),
                command=kwarg[1],
                pady=5,
                padx=30)
            newButton.pack(fill=X, pady=5, padx=5)


if __name__ == '__main__':
    root = tk.Tk()

    abf = ActionButtonFrame(root, 
            Test                = ( lambda: print('Testing')),
            Underscore_Space    = ( lambda: print('Testing too'))
            )
    abf.pack()

    root.mainloop()