from logic import Autogreener
from gui import AutogreenerApp

import tkinter as tk
import argparse

if __name__ == '__main__':


    ag = Autogreener()
    app = AutogreenerApp()

    app.autogreenClicked += ag.autogreen_image

    from PIL import Image

    img = Image.open('data/input/ss.png')
    img.show()

    tree = ag.autogreen_image(img)

    print(tree)

    app.previewFrame.draw_agItemList(tree)

    app.mainloop()
