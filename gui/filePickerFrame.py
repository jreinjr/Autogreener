import tkinter as tk
from tkinter import filedialog, ttk
import glob
import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from autogreener.utils import Bbox, EventHook
from pathlib import Path


class FilePickerFrame(tk.Frame):
    """
    Generic GUI solution for selecting a directory and the files within.
    """

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.dir_path = Path.cwd()

        self.directory_stringVar = tk.StringVar()

        self.directoryChanged = EventHook()
        self.filePicked = EventHook()

        self.widgets()

    def widgets(self):
        sidebarFrame = tk.Frame(self)
        sidebarFrame.pack(side=tk.LEFT, fill=tk.Y)

        directoryFrame = tk.LabelFrame(
            sidebarFrame, text="Directory:", padx=5, pady=5)
        directoryFrame.pack(side=tk.TOP)

        directoryEntry = tk.Entry(
            directoryFrame,
            textvariable=self.directory_stringVar)
        directoryEntry.pack(side=tk.LEFT)

        directoryBrowseButton = tk.Button(
            directoryFrame,
            text="Browse...",
            command=self.onDirectoryBrowseClicked)
        directoryBrowseButton.pack(side=tk.LEFT)

        fileFrame = tk.LabelFrame(
            sidebarFrame,
            text="Select PNG image file:",
            padx=5,
            pady=5)
        fileFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.fileListBox = tk.ttk.Treeview(fileFrame)
        self.fileListBox.bind("<Double-Button-1>", self.onFileListDoubleClick)
        self.fileListBox.pack(expand=True, fill=tk.BOTH)

    def onDirectoryBrowseClicked(self):

        dirPath = filedialog.askdirectory(
            initialdir= self.dir_path, title="Select directory:")

        self.dir_path = Path(dirPath)

        files = [Path(f).name for f in self.dir_path.glob("*.png")]

        # Update file listbox
        [self.fileListBox.delete(i) for i in self.fileListBox.get_children()]
        [print(f) for f in files]
        [self.fileListBox.insert('', 0, text=f) for f in files]

        self.directoryChanged.fire(self.dir_path)


    def onFileListDoubleClick(self, event):
        focus = event.widget.focus()
        clicked_item = event.widget.item(focus)['text']
        if clicked_item is not '':
            filePath = self.dir_path / clicked_item
            self.filePicked.fire(filePath)


   


if __name__ == '__main__':
    root = tk.Tk()

    fpf = FilePickerFrame(root)
    fpf.pack()

    root.mainloop()