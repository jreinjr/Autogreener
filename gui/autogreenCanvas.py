import tkinter as tk
import cv2
import numpy as np

from autogreener.gui.tkCanvasUtils import *
from autogreener.utils import Bbox

class AutogreenCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        tk.Canvas.__init__(self, master, kwargs)

        bind_scrollbars(self)
        bind_box_selection(self)
        bind_image_preview(self)

    def create_autogreen_item(self, agItem):

        def from_rgb(rgb_np):
            rgb = tuple([int(f) for f in rgb_np])
            return "#%02x%02x%02x" % rgb

        bbox = agItem.bbox
        self.border_fill_bbox(bbox)
        self.create_line((bbox.E, bbox.W), \
                fill=from_rgb(agItem.fg), width=bbox.height * 0.3, tags="line", capstyle=tk.ROUND)

    def create_debug_rect(self, agItem, color='green'):
        x, y, w, h = agItem.bbox.as_xywh()
        self.create_rectangle((x, y, x + w, y + h), outline=color)


    def border_fill_bbox(self, bbox):

        def most_frequent(list_): 
            return max(set(list_), key = list_.count)

        np_img = np.asarray(self.image)

        px = list(map(tuple, Bbox.to_border_pixels(bbox)))
        cols = list(map(lambda c: tuple(np_img[c[0]-1, c[1]-1]), px))
        col = tuple(map(int, most_frequent(cols)))

        cv2.rectangle(np_img, bbox.NW, bbox.SE, color=col, thickness=cv2.FILLED)
