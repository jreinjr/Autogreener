import tkinter as tk
from tkinter import filedialog, LEFT, TOP, RIGHT, BOTTOM, END, YES, HORIZONTAL, BOTH, N, S, E, W, NW, NE, SW, SE, NSEW, X, Y
import glob
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from autogreener.utils import Bbox, EventHook
from pathlib import Path


class FilePickerFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.directory_stringVar = tk.StringVar()

        self.directoryChanged = EventHook()
        self.filePicked = EventHook()

        self.widgets()

    def widgets(self):
        sidebarFrame = tk.Frame(self)
        sidebarFrame.pack(side=LEFT, fill=Y)

        directoryFrame = tk.LabelFrame(
            sidebarFrame, text="Directory:", padx=5, pady=5)
        directoryFrame.pack(side=TOP)

        directoryEntry = tk.Entry(
            directoryFrame,
            textvariable=self.directory_stringVar)
        directoryEntry.pack(side=LEFT)

        directoryBrowseButton = tk.Button(
            directoryFrame,
            text="Browse...",
            command=self.onDirectoryBrowseClicked)
        directoryBrowseButton.pack(side=LEFT)

        fileFrame = tk.LabelFrame(
            sidebarFrame,
            text="Select PNG image file:",
            padx=5,
            pady=5)
        fileFrame.pack(side=TOP, expand=True, fill=BOTH)

        fileListBox = tk.Listbox(fileFrame)
        fileListBox.bind("<Double-Button-1>", self.onFileListDoubleClick)
        fileListBox.pack(expand=True, fill=BOTH)
        self.fileListBox = fileListBox

    def onDirectoryBrowseClicked(self):
        dirPath = self.currentDirectoryPath.get()
        dirPath = filedialog.askdirectory(
            initialdir=dirPath, title="Select directory:")

        self.currentDirectoryPath.set(dirPath)
        self.onDirectoryChanged(dirPath)
        self.directoryChanged.fire(dirPath)

    def onDirectoryChanged(self, path):
        files = self.getPNGFilesAtPath(path)
        self.updateFileListBox(files)

    def onFileListDoubleClick(self, event):
        lb = event.widget
        item = lb.get('active')
        self.currentFileName = item
        filePath = f"{self.currentDirectoryPath.get()}/{item}"
        self.filePicked.fire(filePath)

    def getPNGFilesAtPath(self, path):
        return [os.path.basename(f) for f in glob.glob(path + "/*.png")]

    def updateFileListBox(self, files):
        self.fileListBox.delete(0, END)
        [self.fileListBox.insert(END, f) for f in files]


if __name__ == '__main__':
    root = tk.Tk()

    fpf = FilePickerFrame(root)
    fpf.pack()

    root.mainloop()