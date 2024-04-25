import tkinter
from tkinter import ttk
from magictk import color_tmpl
from magictk.scrollbar import ScrollBar
import sys


class Frame(tkinter.Frame):
    color = color_tmpl.default_color

    def __init__(self, master, color=None, *args, **kwargs):
        self.root = master.root
        self.p_event_list = ()
        if ("bg" not in kwargs and "background" not in kwargs):
            kwargs["bg"] = self.color["background"]
        super().__init__(master, *args, **kwargs)
        self.configure()

        for event, eventfunc in master.p_event_list:
            self.bind(event, eventfunc)


class Container(Frame):
    color = color_tmpl.default_color

    def scroll_callback(self, obj, pos):
        super().place(x=0, y=-pos, w=self.w-7, h=self.container_h)

    def update_frame(self, *args, **kwargs):
        self.w = self.root_frame.winfo_width()
        self.h = self.root_frame.winfo_height()
        super().place(x=0, y=-self.scroll.get(), w=self.w-7, h=self.container_h)
        self.scroll._r_allh = self.container_h
        self.scroll._r_maxh = self.h
        self.scroll.place(x=self.w-7, y=0, w=8, relheight=1)
        self.scroll.h = self.h
        scrolltmp = self.scroll.scroll_y*self.scroll.y_size
        self.scroll.cal_bar()
        self.scroll.update_pos()
        if (self.scroll.y_size == 0):
            self.scroll.scroll_y = 0
        else:
            self.scroll.scroll_y = min(self.scroll.h-self.scroll.bar_len,
                                       max(0, scrolltmp/self.scroll.y_size))
        self.scroll_callback(self.scroll, self.scroll.get())

    def scrollwheel(self, event: tkinter.Event, setdelta=None):
        if (setdelta is None):
            delta = event.delta
        else:
            delta = setdelta
        if sys.platform.startswith('win'):
            delta //= 20
        self.scroll.scroll_y = max(
            0, min(self.scroll._r_maxh-self.scroll.bar_len, self.scroll.scroll_y+delta))
        self.scroll.update_pos()
        self.scroll_callback(self.scroll, self.scroll.get())

    def __init__(self, master, color=None, w=300, h=200, container_h=500, *args, **kwargs):
        self.root = master.root
        self.w = w
        self.h = h
        self.container_h = container_h
        self.root_frame = Frame(master, width=w, height=self.container_h)
        super().__init__(self.root_frame, *args, **kwargs)
        super().place(x=0, y=0, w=self.w-7, h=container_h)
        self.scroll = ScrollBar(self.root_frame,
                                h=self.h, allh=self.container_h, maxh=self.h, callback=self.scroll_callback)
        self.scroll.place(x=self.w-7, y=0, w=8, relheight=1)
        self.root_frame.bind("<Configure>", self.update_frame)

        if sys.platform.startswith('win'):
            self.bind("<MouseWheel>", self.scrollwheel)
            self.p_event_list = (("<MouseWheel>", self.scrollwheel),)
        elif sys.platform.startswith('darwin'):
            self.bind("<MouseWheel>", self.scrollwheel)
            self.p_event_list = (("<MouseWheel>", self.scrollwheel),)
        else:
            self.bind(
                "<Button-4>", lambda event: self.scrollwheel(event, -10))
            self.bind(
                "<Button-5>", lambda event: self.scrollwheel(event, 10))
            self.p_event_list = (
                ("<Button-4>", lambda event: self.scrollwheel(event, -10)), ("<Button-5>", lambda event: self.scrollwheel(event, 10)))
        # self.configure

    def pack(self, *args, **kwargs):
        self.root_frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.root_frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.root_frame.place(*args, **kwargs)
