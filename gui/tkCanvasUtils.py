import tkinter as tk


def bind_box_selection(canvas):
    """
    Usage: 
        canvas = tk.Canvas()
        bind_box_selection(canvas)
        canvas.selection
    """
    canvas.selection = None
    canvas._rect = None
    canvas._dragStart = None

    def on_click(event):
        canvas._dragStart = canvas.canvasx(event.x), canvas.canvasy(event.y)

        canvas.selection = *canvas._dragStart, *canvas._dragStart

        if not canvas._rect:
            canvas._rect = canvas.create_rectangle(*canvas._dragStart, *canvas._dragStart, outline='red', tag='selection')
        else:
            canvas.coords(canvas._rect, canvas.selection)


    def on_drag(event):
        def clamp(n, smallest, largest): 
            return max(smallest, min(n, largest))
        
        # Find the bounding box that encloses everything except the selection rect
        # Using canvas.bbox('all') added unwanted padding
        canvas.addtag_all('bbox')
        canvas.dtag('selection', 'bbox')
        bbox = canvas.bbox('bbox')

        if bbox is None: bbox = 0,0,canvas.winfo_width(), canvas.winfo_height()

        # Clamp drag point to canvas bounding box
        current = clamp(canvas.canvasx(event.x), bbox[0], bbox[2]), clamp(canvas.canvasy(event.y), bbox[1], bbox[3])

        canvas.selection = *canvas._dragStart, *current

        canvas.coords(canvas._rect, canvas.selection)


    def on_release(event):
        print(f"Current selection bounds: {canvas.selection}")

    # Bindings
    canvas.bind("<ButtonPress-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)


def bind_image_preview(canvas):
    """
    Usage:
        canvas = tk.Canvas()
        bind_image_preview(canvas)
        canvas.preview(image)
    """
    def preview(image):
        from PIL import ImageTk
        canvas.image = image
        canvas._photo = ImageTk.PhotoImage(image)
        canvas.config(width=image.width, height=image.height, scrollregion=(0,0,image.width, image.height))
        canvas.itemconfig(canvas.image_on_canvas, image= canvas._photo )

    canvas.image = None
    canvas._photo = None
    canvas.image_on_canvas = canvas.create_image(
        0, 0, anchor=tk.NW, image= canvas._photo )
    canvas.preview = preview


def bind_scrollbars(canvas):
    """
    Usage:
        canvas = tk.Canvas()
        bind_scrollbars(canvas)
    """
    yScrollbar = tk.Scrollbar(canvas.master, command=canvas.yview)
    yScrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NW)

    xScrollbar = tk.Scrollbar(canvas.master, orient=tk.HORIZONTAL, command=canvas.xview)
    xScrollbar.place(relx=0, rely=1, relwidth=1, anchor=tk.NW)

    canvas.config(yscrollcommand=yScrollbar.set,
                  xscrollcommand=xScrollbar.set)


if __name__ == "__main__":
    root = tk.Tk()

    frame = tk.Frame(root, bg='gray')
    frame.pack(expand=True, fill=tk.BOTH)

    canvas = tk.Canvas(frame,
                       width=500,
                       height=300)
    canvas.pack(expand=True)

    bind_scrollbars(canvas)
    bind_box_selection(canvas)
    bind_image_preview(canvas)

    from PIL import Image

    image = Image.open('data/input/ss.png')

    canvas.preview(image)

    root.mainloop()
    