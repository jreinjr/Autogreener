from logic import Autogreener
from gui import AutogreenerGUI

import tkinter as tk
import argparse

if __name__ == '__main__':
    ag = Autogreener()
    gui = AutogreenerGUI()

    gui.autogreenClicked += ag.autogreen_image

    ag.autogreeningComplete += gui.draw_autogreen_items

    gui.mainloop()
