import tkinter
from tkinter import ttk
from magictk import color_tmpl
from magictk.scrollbar import ScrollBar


class Frame(tkinter.Frame):
    color = color_tmpl.default_color

    def __init__(self, master, color=None, *args, **kwargs):
        self.root = master.root
        if ("bg" not in kwargs and "background" not in kwargs):
            kwargs["bg"] = self.color["background"]
        super().__init__(master, *args, **kwargs)
        self.configure()


class Container(Frame):
    color = color_tmpl.default_color

    def scroll_callback(self, obj, pos):
        super().place(x=0, y=-pos, w=self.w-7, h=self.container_h)

    def __init__(self, master, color=None, w=300, h=200, container_h=500, *args, **kwargs):
        self.root = master.root
        self.w = w
        self.h = h
        self.container_h = container_h
        self.root_frame = Frame(master, width=w, height=h)
        super().__init__(self.root_frame, *args, **kwargs)
        super().place(x=0, y=0, w=self.w-7, h=container_h)
        self.scroll = ScrollBar(self.root_frame,
                                h=self.h, allh=self.container_h-self.h, maxh=self.h, callback=self.scroll_callback)
        self.scroll.place(x=self.w-7, y=0, w=8, relheight=1)

    def pack(self, *args, **kwargs):
        self.root_frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.root_frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.root_frame.place(*args, **kwargs)
