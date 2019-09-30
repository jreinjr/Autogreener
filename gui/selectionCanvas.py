import tkinter as tk
from autogreener.utils import Bbox

class SelectionCanvas(tk.Canvas):
    
    def __init__(self, master, **kwargs):
        tk.Canvas.__init__(self, master, kwargs)

        # Box selection variables
        self.bbox = None
        self._rect = None
        self._dragStart = None
        
        # Scrollbars packed into master
        self.widgets(master)

        # Bindings
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        # Event hooks
        # Add event hooks here to listen for click, drag, release


    def widgets(self, master):
        yScrollbar = tk.Scrollbar(master, command=self.yview)
        yScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        xScrollbar = tk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.xview)
        xScrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.config(yscrollcommand=yScrollbar.set,
                    xscrollcommand=xScrollbar.set)


    def on_click(self, event):
        self._dragStart = self.canvasx(event.x), self.canvasy(event.y)

        if not self._rect:
            self._rect = self.create_rectangle(*self._dragStart, *self._dragStart, outline='red')

        self.bbox = *self._dragStart, *self._dragStart


    def on_drag(self, event):
        current = self.canvasx(event.x), self.canvasy(event.y)

        self.bbox = *self._dragStart, *current

        self.coords(self._rect, self.bbox)


    def on_release(self, event):
        print(f"Current selection: {self.bbox}")


if __name__ == "__main__":
    root = tk.Tk()

    canvas = SelectionCanvas(root, 
            scrollregion=(0,0,1529,956), 
            width=500, 
            height=300)
    canvas.pack(expand=True, fill=tk.BOTH)

    root.mainloop()