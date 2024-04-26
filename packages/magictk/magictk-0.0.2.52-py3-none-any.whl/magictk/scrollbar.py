import json
import tkinter
from tkinter import ttk
from magictk import color_tmpl
from magictk import photoload


class ScrollBar:
    color = color_tmpl.default_color
    __fill_obj = {}
    progress = 0.0
    __progress_pixel = 0
    __move_progress_pixel = 0
    max_flash = 4
    scroll_y = 0
    y_size = 1.0
    bar_len = 100
    _dis_event = False

    def cal_bar(self):
        self.bar_len = self._r_maxh*self.h//self._r_allh
        if (self.h-self.bar_len == 0):
            self.y_size = 0
        else:
            self.bar_len = max(20, self.bar_len)
            self.y_size = (self._r_allh-self._r_maxh)/(self.h-self.bar_len)

    def __draw_corner(self, r_x, r_y, x, y, colors="#000000", rid="", bgcolor=None, **kwargs):
        if bgcolor is None:
            bgcolor = self.color["border_light"]
        self.__fill_obj[rid] = []
        self.__fill_obj[rid+"_pos"] = []
        self.__fill_obj[rid+"_pos2"] = []
        self.border_info = json.loads(photoload.loadres("scrollbarborder"))
        y_n = 0
        for i in self.border_info:
            x_n = 0
            for j in i:
                if (r_x == 0):
                    px = x+x_n+1
                    zpx = x_n+1
                else:
                    px = x+6-x_n
                    zpx = 6-x_n
                if (r_y == 0):
                    py = y+y_n+1
                    zpy = y_n+1
                else:
                    py = y+3-y_n-1
                    zpy = 3-y_n-1
                if (j < 0):
                    lcolor = -j
                else:
                    lcolor = j
                # if(lcolor==255):
                #     continue
                g_color = color_tmpl.mix_color(
                    bgcolor, colors, int((1-lcolor/255)*1000)/1000)

                obj = self.canvas.create_rectangle(
                    px, py, px, py, width=0, fill=g_color)

                self.__fill_obj[rid].append(obj)
                self.__fill_obj[rid+"_pos"].append([zpx, zpy])
                self.__fill_obj[rid+"_pos2"].append([y_n, x_n])

                x_n += 1
            y_n += 1

    def __init__(self, master=None, root_anim=None, w=None, h=8, colors="primary", color_list: dict = None, allh=100,
                 maxh=50, callback=lambda obj, val: None):
        self._r_allh = allh
        self._r_maxh = maxh
        self.callback = callback
        self.w = 8
        self.h = h
        self.__master = master
        self.colors = colors
        if (color_list is not None):
            self.color = color_list
        if (root_anim == None):
            self.__root = master.root
        else:
            self.__root = root_anim

        self.canvas = tkinter.Canvas(
            master, bg=self.color["background"], width=self.w, height=self.h, borderwidth=0, bd=0, highlightcolor=self.color["background"], highlightthickness=0)

        self.cal_bar()

        self.__draw()
        self.bind_event()
        self.update_pos()

    def pack(self, *args, **kwargs):
        self.canvas.pack(*args, **kwargs)

    def pack_forget(self, *args, **kwargs):
        self.canvas.pack_forget(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.canvas.grid(*args, **kwargs)

    def grid_forget(self, *args, **kwargs):
        self.canvas.grid_forget(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.canvas.place(*args, **kwargs)

    def place_forget(self, *args, **kwargs):
        self.canvas.place_forget(*args, **kwargs)

    def update_pos(self):
        for i in range(len(self.__fill_obj["upside"])):
            self.canvas.coords(
                self.__fill_obj["upside"][i], int(self.__fill_obj["upside_pos"][i][0]), self.__fill_obj["upside_pos"][i][1]+self.scroll_y, int(self.__fill_obj["upside_pos"][i][0]), self.__fill_obj["upside_pos"][i][1]+self.scroll_y)
        self.canvas.coords(
            self.__fill_obj["fgbar"][0], 1, 4+self.scroll_y, self.w-1, self.scroll_y+self.bar_len-4+1)
        for i in range(len(self.__fill_obj["bottomside"])):
            self.canvas.coords(
                self.__fill_obj["bottomside"][i], int(self.__fill_obj["bottomside_pos"][i][0]), self.__fill_obj["bottomside_pos"][i][1]+self.scroll_y+self.bar_len-5, int(self.__fill_obj["bottomside_pos"][i][0]), self.__fill_obj["bottomside_pos"][i][1]+self.scroll_y+self.bar_len-5)

    def bind_event(self):
        def mouse_move(event: tkinter.Event):
            if (not self._dis_event):
                delta_y = event.y-self.scroll_y
                self.scroll_y = min(self.h-self.bar_len,
                                    max(0, self.scroll_y+delta_y-self.move_start))
                self.callback(self, self.get())
                self.update_pos()

        def mouse_press(event: tkinter.Event):
            if (not self._dis_event):
                flag = False
                if (event.y >= self.scroll_y and event.y <= self.scroll_y+self.bar_len):
                    pass
                else:
                    self.scroll_y = min(self.h-self.bar_len,
                                        max(0, event.y-self.bar_len//2))
                    flag = True
                self.move_start = event.y-self.scroll_y
                for i in range(len(self.__fill_obj["upside"])):
                    self.canvas.itemconfig(
                        self.__fill_obj["upside"][i], fill=color_tmpl.mix_color(
                            self.color["background"], self.color["border_base"], int((1-self.border_info[self.__fill_obj["upside_pos2"][i][0]][self.__fill_obj["upside_pos2"][i][1]]/255)*1000)/1000))
                self.canvas.itemconfig(
                    self.__fill_obj["fgbar"][0], fill=self.color["border_base"])
                for i in range(len(self.__fill_obj["bottomside"])):
                    self.canvas.itemconfig(
                        self.__fill_obj["bottomside"][i], fill=color_tmpl.mix_color(
                            self.color["background"], self.color["border_base"], int((1-self.border_info[self.__fill_obj["bottomside_pos2"][i][0]][self.__fill_obj["bottomside_pos2"][i][1]]/255)*1000)/1000))
                if (flag):
                    self.update_pos()
                    mouse_move(event)

        def mouse_release(event: tkinter.Event):
            if (not self._dis_event):
                for i in range(len(self.__fill_obj["upside"])):
                    self.canvas.itemconfig(
                        self.__fill_obj["upside"][i], fill=color_tmpl.mix_color(
                            self.color["background"], self.color["border_light"], int((1-self.border_info[self.__fill_obj["upside_pos2"][i][0]][self.__fill_obj["upside_pos2"][i][1]]/255)*1000)/1000))
                self.canvas.itemconfig(
                    self.__fill_obj["fgbar"][0], fill=self.color["border_light"])
                for i in range(len(self.__fill_obj["bottomside"])):
                    self.canvas.itemconfig(
                        self.__fill_obj["bottomside"][i], fill=color_tmpl.mix_color(
                            self.color["background"], self.color["border_light"], int((1-self.border_info[self.__fill_obj["bottomside_pos2"][i][0]][self.__fill_obj["bottomside_pos2"][i][1]]/255)*1000)/1000))

        self.canvas.bind("<B1-Motion>", mouse_move)
        self.canvas.bind("<Button-1>", mouse_press)
        self.canvas.bind("<ButtonRelease-1>", mouse_release)

    def __draw(self):
        self.__draw_corner(0, 0, 0, self.scroll_y,
                           self.color["border_light"], "upside", bgcolor=self.color["background"])
        self.__fill_obj["fgbar"] = [
            self.canvas.create_rectangle(1, 4+self.scroll_y, self.w-1, self.scroll_y+self.bar_len-4+1, width=0, fill=self.color["border_light"])]
        self.__draw_corner(0, 1, 0, self.scroll_y+self.bar_len-4+1,
                           self.color["border_light"], "bottomside", bgcolor=self.color["background"])

    def get(self):
        if (self.scroll_y+self.bar_len >= self.h):
            return self._r_allh-self._r_maxh
        else:
            return int(min(self.scroll_y*self.y_size, self._r_allh))
