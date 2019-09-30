import tkinter as tk
from tkinter import filedialog, LEFT, TOP, RIGHT, BOTTOM, END, YES, HORIZONTAL, BOTH, N, S, E, W, NW, NE, SW, SE, NSEW, X, Y
import glob
import os
import tempfile
import io
import cv2
import numpy as np
from copy import deepcopy
from PIL import Image, ImageTk

from autogreener.gui.tkinterUtils import *
from autogreener.utils import Bbox


class AutogreenerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        frame = tk.Frame(self)
        frame.pack()

        # Events
        self.autogreenClicked = EventHook()

        # Configure UI
        self.widgets(frame)

        # Switchboard bindings
        self.filePickerFrame.filePicked += self.onFilePicked

    def widgets(self, master):
        # Top level windows
        actionWindow = tk.Toplevel(master)
        previewWindow = tk.Toplevel(master)

        # File picker frame
        self.filePickerFrame = FilePickerFrame(actionWindow)
        self.filePickerFrame.pack(expand=True, fill=BOTH)

        # Action button frame
        self.actionButtonFrame = ActionButtonFrame(
            actionWindow,
            Autogreen=self.onAutogreenClicked)
        self.actionButtonFrame.pack(side=BOTTOM, expand=True, fill=X)

        # Preview frame
        self.previewFrame = AutogreenPreviewFrame(previewWindow)
        self.previewFrame.pack(expand=True, fill=BOTH)

    def onFilePicked(self, filePath):
        self.previewFrame.load_image(filePath)

    def onAutogreenClicked(self):
        self.autogreenClicked.fire(self.previewFrame.img_original)



if __name__ == '__main__':
    pass