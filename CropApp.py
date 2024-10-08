import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class CornerBox():
    def __init__(self, pos, canvas, c_height, c_width, inplace=False, x=0, y=0):
        if pos == 'NW':
            self.x, self.y = 5, 5
        elif pos == 'NE':
            self.x, self.y = c_width-5, 5
        elif pos == 'SE':
            self.x, self.y = c_width-5, c_height-5
        elif pos == 'SW':
            self.x, self.y = 5, c_height-5

        self.c_height, self.c_width = c_height, c_width
        self.canvas = canvas

        self.reset_x, self.reset_y = self.x, self.y

        if inplace == True:
            self.x = x
            self.y = y

        self.cb_id = canvas.create_rectangle(
            self.x-5, self.y-5, self.x+5, self.y+5, fill="blue")

        # canvas.tag_bind(self.cb_id, "<Button-1>", self.grab)
        # canvas.tag_bind(self.cb_id, "<B1-Motion>", self.drag)

    def grab(self, event):
        widget = event.widget
        self.x = widget.canvasx(event.x)
        self.y = widget.canvasy(event.y)
        self.widget = self.cb_id

    def drag(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasy(event.y)
        if xc < 5 or yc < 5 or xc > self.c_width-5 or yc > self.c_height-5:
            return

        self.canvas.move(self.widget, xc-self.x, yc-self.y)
        self.x, self.y = xc, yc

        x1, y1, x2, y2 = self.canvas.coords(self.cb_id)
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2

    @property
    def coords(self):
        return (self.x, self.y)

    @property
    def id(self):
        return self.cb_id

    def reset(self):
        xc, yc = self.reset_x, self.reset_y
        self.canvas.move(self.cb_id, xc-self.x, yc-self.y)
        self.x, self.y = xc, yc

        x1, y1, x2, y2 = self.canvas.coords(self.cb_id)
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2

    @coords.setter
    def coords(self, xc, yc):
        if xc < 5 or yc < 5 or xc > self.c_width-5 or yc > self.c_height-5:
            return
        self.canvas.move(self.cb_id, xc-self.x, yc-self.y)
        self.x, self.y = xc, yc

        x1, y1, x2, y2 = self.canvas.coords(self.cb_id)
        self.x = (x1+x2)/2
        self.y = (y1+y2)/2


class CropApp:

    def __init__(self, master, img_array, inplace=False, coordinates=[[0, 0], [0, 0], [0, 0], [0, 0]]):
        self.master = master

        self.crop_pressed = False

        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()

        self.img_array = img_array
        self.im = Image.fromarray(self.img_array)
        self.img_width, self.img_height = self.im.size

        f1 = 0
        f2 = 0
        self.scale_factor = 1

        if self.img_width > self.screen_width:
            f1 = self.img_width // self.screen_width

        if self.img_height > self.screen_height:
            f2 = self.img_height // self.screen_height

        if f1 != 0 or f2 != 0:
            self.scale_factor = max(f1, f2)
            self.scale_factor += 1
            self.im = self.im.resize(
                (self.img_width//self.scale_factor, self.img_height//self.scale_factor), Image.Resampling.LANCZOS)
            self.img_width, self.img_height = self.im.size

        self.c_width = self.img_width + 10
        self.c_height = self.img_height + 10

        self.canvas = tk.Canvas(
            self.master, width=self.c_width, height=self.c_height)
        self.canvas.pack()

        self.img_canvas = ImageTk.PhotoImage(self.im)
        self.img_canvas_img_id = self.canvas.create_image(
            5, 5, image=self.img_canvas, anchor=tk.NW)
        if inplace == False:
            self.NW = CornerBox('NW', self.canvas, self.c_height, self.c_width)
            self.NE = CornerBox('NE', self.canvas, self.c_height, self.c_width)
            self.SE = CornerBox('SE', self.canvas, self.c_height, self.c_width)
            self.SW = CornerBox('SW', self.canvas, self.c_height, self.c_width)
        else:
            self.NW = CornerBox('NW', self.canvas, self.c_height,
                                self.c_width, True, coordinates[0][0]//self.scale_factor, coordinates[0][1]//self.scale_factor)
            self.NE = CornerBox('NE', self.canvas, self.c_height,
                                self.c_width, True, coordinates[1][0]//self.scale_factor, coordinates[1][1]//self.scale_factor)
            self.SE = CornerBox('SE', self.canvas, self.c_height,
                                self.c_width, True, coordinates[2][0]//self.scale_factor, coordinates[2][1]//self.scale_factor)
            self.SW = CornerBox('SW', self.canvas, self.c_height,
                                self.c_width, True, coordinates[3][0]//self.scale_factor, coordinates[3][1]//self.scale_factor)

        self.but_frame = tk.Frame(self.master)
        self.but_frame.pack()

        # self.coord_butt = tk.Button(  
        #     self.but_frame, text="Show Coordinates", command=self.printBoxDetails)
        # self.coord_butt.pack(side=tk.LEFT)

        style = ttk.Style()

        style.configure('TButton',
                        background='#4788f7',
                        foreground='#4788f7',
                        font=('Helvetica', 10, 'bold'),
                        borderwidth=1,
                        # padding=(10, 20)
                        padding=(5, 10))
        
        

        # Apply a hover effect (requires ttk 8.6+)
        style.map('TButton',
                  background=[('active', '#073c6d')])

        self.reset_butt = ttk.Button(
            self.but_frame, text="Reset", style='TButton', command=self.restCorners)
        self.reset_butt.pack(side=tk.LEFT, padx=5, pady=5)

        self.crop_butt = ttk.Button(
            self.but_frame, text="Crop", style='TButton', command=self.crop)
        self.crop_butt.pack(side=tk.LEFT, padx=5, pady=5)

        self.box_id = None
        self.p1_id = None
        self.p2_id = None
        self.p3_id = None
        self.p4_id = None

        self.drawBox()

        for i in [self.NW, self.NE, self.SE, self.SW]:
            self.canvas.tag_bind(i.cb_id, "<Button-1>", i.grab)
            self.canvas.tag_bind(i.cb_id, "<B1-Motion>", i.drag)

    def printBoxDetails(self):
        print(self.NW.coords, self.NE.coords, self.SE.coords, self.SW.coords)

    def crop(self):
        self.crop_pressed = True
        self.master.destroy()

    def restCorners(self):
        self.NW.reset()
        self.NE.reset()
        self.SE.reset()
        self.SW.reset()

    def drawBox(self, event=None):
        if self.box_id != None:
            self.canvas.delete(self.box_id)
        if self.p1_id != None:
            self.canvas.delete(self.p1_id)
        if self.p2_id != None:
            self.canvas.delete(self.p2_id)
        if self.p3_id != None:
            self.canvas.delete(self.p3_id)
        if self.p4_id != None:
            self.canvas.delete(self.p4_id)

        self.box_id = self.canvas.create_line(
            *self.NW.coords,
            *self.NE.coords,
            *self.SE.coords,
            *self.SW.coords,
            *self.NW.coords,
            fill="#4788f7", width=2)

        self.p1_id = self.canvas.create_polygon(
            0, 0, *self.NW.coords, *self.SW.coords, 0, self.c_height, fill="#4788f7", stipple="gray25")
        self.p2_id = self.canvas.create_polygon(
            0, 0, *self.NW.coords, *self.NE.coords, self.c_width, 0, fill="#4788f7", stipple="gray25")
        self.p3_id = self.canvas.create_polygon(
            self.c_width, 0, *self.NE.coords, *self.SE.coords, self.c_width, self.c_height, fill="#4788f7", stipple="gray25")
        self.p4_id = self.canvas.create_polygon(
            self.c_width, self.c_height, *self.SE.coords, *self.SW.coords, 0, self.c_height, fill="#4788f7", stipple="gray25")

        self.canvas.tag_raise(self.NW.cb_id, 'all')
        self.canvas.tag_raise(self.NE.cb_id, 'all')
        self.canvas.tag_raise(self.SE.cb_id, 'all')
        self.canvas.tag_raise(self.SW.cb_id, 'all')

        self.canvas.after(1, self.drawBox)
