import tkinter as tk
from tkinter import filedialog, LEFT, TOP, RIGHT, BOTTOM, END, YES, HORIZONTAL, BOTH, N, S, E, W, NW, NE, SW, SE, NSEW, X, Y
import glob
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from autogreener.utils import Bbox, EventHook


class ContextMenu(tk.Menu):
    """
    Generic context for executing user commands.

    TODO: Encapsulate popup functionality?
    """
    def __init__(self, master, **kwargs):
        tk.Menu.__init__(self, master, tearoff=0)
        for kwarg in kwargs.items():
            self.add_command(label=kwarg[0], command=kwarg[1])

if __name__ == '__main__':
    root = tk.Tk()

    