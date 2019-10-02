import os, tempfile, tkinter as tk
import numpy as np
from skimage import io
import cv2
from PIL import Image

from autogreener.logic import HOCRParser, AGItemList, AGItem
from autogreener.gui import AutogreenerGUI
from autogreener.utils import EventHook

class Autogreener():
    def __init__(self):
        self.tree = None
        self.autogreeningComplete = EventHook()

    def autogreen_image(self, img):

        hocr = HOCRParser()

        hocr.load_image(img)

        hocr_results = hocr.get_all_with_tag('line')

        boxes, text, images = list(zip(*hocr_results))

        self.tree = AGItemList()

        for b, t, im in zip(boxes, text, images):
            # Palette is sorted most dominant colors first
            palette = self.get_palette(im, 2)

            self.tree.add_child(AGItem(bbox=b, text=t, fg=palette[1], bg=palette[0]))

        self.tree.prune_empty()

        # Repeated function call is a 'temporary' hack
        [self.tree.cluster_overlapping(dilate=(20,-4)) for _ in range(50)]

        self.autogreeningComplete.fire(self.tree)
        
        return self.tree

    def get_palette(self, img, n_colors=5):

        img = np.array(img)
        pixels = np.float32(img.reshape(-1, 3))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)

        return [c for _,c in reversed(sorted(zip(counts, palette)))]
    