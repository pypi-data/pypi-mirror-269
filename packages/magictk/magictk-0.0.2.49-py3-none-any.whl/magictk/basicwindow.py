import time
import tkinter
import os
from tkinter import ttk
from magictk import color_tmpl
from magictk import _window_ctl
from magictk import _window_size
from magictk import workspace
from magictk import photoload
import sys

WIN_INF = -10000


class Tk(ttk.Frame):
    x = 200
    y = 200
    w = 500
    h = 350
    color = color_tmpl.default_color
    anim = []
    FRAME_INFO = "Normal"
    __break_win = True

    def __load_color(self) -> None:
        self.main_tk.configure(bg=self.color["background"])
        self.style.configure(
            'Test1.TFrame', background="#FF0000")
        self.style.configure(
            'Test2.TFrame', background="#00FF00")
        self.style.configure(
            'Test3.TFrame', background="#0000FF")
        self.style.configure(
            'Main.TFrame', background=self.color["background"])
        self.style.configure(
            'Root.TFrame', background=self.color["background"])
        self.style.configure(
            'Splitline.TFrame', background=self.color["border_light"])
        self.style.configure(
            'BarExitButton.TFrame', background=self.color["background"])
        self.style.configure(
            'LabBarZoomButton.TLabel', background=self.color["background"])
        self.style.configure(
            'LabBarIcon.TLabel', background=self.color["background"])
        self.style.configure(
            'LabTitle.TLabel', background=self.color["background"], fg=self.color["primary_text"])
        self.style.configure(
            'BarIconicButton.TFrame', background=self.color["background"])
        self.style.configure(
            'Size.TFrame', background=self.color["background"])
        self.style.configure(
            'LabelTitle.TFrame', background=self.color["background"])

    def __init__(self, w=500, h=350, title="MagicTk", color_list: dict = None) -> None:
        self.root = self
        self.title = title
        self.w = w
        self.h = h
        if (color_list is not None):
            self.color = color_list
        self.main_tk = tkinter.Tk()
        self.style = ttk.Style()
        self.__load_color()
        ttk.Widget.__init__(self, self.main_tk, "ttk::frame", {
                            "style": "Main.TFrame"})
        self.main_tk.title(title)
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_tk.geometry(
            f"{self.w}x{self.h}+{self.x}+{self.y}")

    def mainloop(self) -> None:
        t_start = time.time()
        while (self.__break_win):
            delta_t = time.time()-t_start
            if (delta_t > 0.02):  # flash animation
                t_start = time.time()
                n = 0
                for i in self.anim:
                    if (i is not None):
                        retn = i()
                        if (retn == -1):
                            self.anim[n] = None
                    n += 1
                self.anim = [i for i in self.anim if i is not None]
            else:
                pass
            self.main_tk.update()
        self.main_tk.destroy()
        self.__break_win = None

    def quit(self) -> None:
        self.__break_win = False
