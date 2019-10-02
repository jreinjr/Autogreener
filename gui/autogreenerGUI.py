import tkinter as tk
import glob
import os
import tempfile
import io
import cv2
import numpy as np
from copy import deepcopy
from PIL import Image, ImageTk

from autogreener.gui.tkCanvasUtils import *
from autogreener.gui import FilePickerFrame, ActionButtonFrame, AutogreenCanvas
from autogreener.utils import Bbox, EventHook


class AutogreenerGUI(tk.Tk):
    """
    Switchboard controller for widgets that provide the following functionality:
        filePickerFrame:    Select an image from a directory
        imagePreviewFrame:  Display the image on a canvas
        boxSelection:       TODO: Box select and return a portion of that image 
        TODO: Draw Autogreen Trees on a canvas
    """
    def __init__(self):
        tk.Tk.__init__(self)

        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH)

        # State
        self.current_image = None

        # Events
        self.imagePicked = EventHook()
        self.autogreenClicked = EventHook()
        self.saveClicked = EventHook()

        # Configure UI
        self.widgets(frame)

        # Switchboard bindings
        self.filePickerFrame.filePicked += self.onFilePicked


    def widgets(self, master):
        # File picker frame
        self.filePickerFrame = FilePickerFrame(master)
        self.filePickerFrame.grid(sticky=tk.NS + tk.W)

        # Action button frame
        self.actionButtonFrame = ActionButtonFrame(master,
                                 Autogreen  = lambda: self.autogreenClicked.fire(self.current_image),
                                 Save       = lambda: self.saveClicked.fire()
                                 )
        self.actionButtonFrame.grid(sticky=tk.EW)


        # Preview frame
        self.previewFrame = tk.Frame(master, bg='grey', padx=15, pady=15)
        self.previewFrame.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        self.previewCanvas = AutogreenCanvas(self.previewFrame, width=800, height=600)
        self.previewCanvas.pack(expand=True)

        master.rowconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)


    def preview(self, image):
        self.previewCanvas.preview(image)


    def draw_autogreen_items(self, tree):
        [self.previewCanvas.create_autogreen_item(i) for i in tree.items]


    def onFilePicked(self, filePath):
        self.current_image = Image.open(filePath)
        self.previewCanvas.preview(self.current_image)
        self.imagePicked.fire(self.current_image)


    def onAutogreenClicked(self):
        self.autogreenClicked.fire(self.current_image)



if __name__ == '__main__':
    
    root = AutogreenerGUI()

    root.mainloop()