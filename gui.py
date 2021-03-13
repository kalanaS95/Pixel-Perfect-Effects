from tkinter import PhotoImage, filedialog
from win32api import GetMonitorInfo, MonitorFromPoint
from GUI_modules.pencilSketch_GUI import *
from GUI_modules.popArt_GUI import *
from GUI_modules.oilPaint_GUI import *
from GUI_modules.solarize_GUI import *
from GUI_modules.morphology_GUI import *
import ctypes #to get screen resolution (This is exclusive to windows)

class GUI:
    def __init__(self):
        self.mainWindow = None
        self.main_window_width = 30 + 30 + (128 * 6) + (20 * 6)
        self.main_window_height = 128 + 15 + (20 * 2)
        self.screen_size_work = None
        self.sketch_icon_label = None
        self.sketch_text_label = None
        self.popArt_icon_label = None
        self.popArt_text_label = None
        self.oilPaint_icon_label = None
        self.oilPaint_text_label = None
        self.cartoon_icon_label = None
        self.cartoon_text_label = None
        self.solarize_icon_label = None
        self.solarize_text_label = None
        self.morph_icon_label = None
        self.morph_text_label = None


    def draw_main_window(self):
        self.screen_size_work = self.getWorking_area()
        self.mainWindow = tk.Tk()
        # turn off main window resize
        self.mainWindow.resizable(False,False)
        # set window name
        self.mainWindow.title("Pixel Perfect Effects")
        self.mainWindow.geometry(f"{(int)(self.main_window_width)}x{(int)(self.main_window_height)}+{(int)((self.screen_size_work[2]/2) - self.main_window_width/2)}+{(int)(self.screen_size_work[3] - self.main_window_height*1.2)}")


        # Creating buttons to click
        # Sketch button label
        img_sketch = PhotoImage(file='icons/sketch.png')
        self.sketch_icon_label = tk.Label(self.mainWindow, image=img_sketch, cursor="hand2")
        self.sketch_icon_label.place(x=30, y=20)
        self.sketch_text_label = tk.Label(self.mainWindow, text="Sketch", justify=tk.CENTER, cursor="hand2")
        self.sketch_text_label.place(x= (30 + 128)/2, y= (20 + 128 + 5))
        self.sketch_icon_label.bind("<Enter>", lambda event, arg="sketch", obj=self.sketch_icon_label: self.on_enter(event, arg, obj))
        self.sketch_icon_label.bind("<Leave>", lambda event, arg="sketch", obj=self.sketch_icon_label: self.on_leave(event, arg, obj))
        self.sketch_icon_label.bind("<Button-1>", lambda event, arg="sketch": self.on_click(event, arg))
        self.sketch_text_label.bind("<Enter>", lambda event, arg="sketch", obj=self.sketch_icon_label: self.on_enter(event, arg, obj))
        self.sketch_text_label.bind("<Leave>", lambda event, arg="sketch", obj=self.sketch_icon_label: self.on_leave(event, arg, obj))

        # Pop art button label
        img_pop = PhotoImage(file='icons/pop.png')
        self.popArt_icon_label = tk.Label(self.mainWindow, image=img_pop, cursor="hand2")
        self.popArt_icon_label.place(x= 30 + 128 + 20, y=20)
        self.popArt_text_label = tk.Label(self.mainWindow, text="Pop Art", justify=tk.CENTER, cursor="hand2")
        self.popArt_text_label.place(x= (30 + 128) + 128/2, y= (20 + 128 + 5))
        self.popArt_icon_label.bind("<Enter>", lambda event, arg="pop", obj=self.popArt_icon_label: self.on_enter(event, arg, obj))
        self.popArt_icon_label.bind("<Leave>", lambda event, arg="pop", obj=self.popArt_icon_label: self.on_leave(event, arg, obj))
        self.popArt_icon_label.bind("<Button-1>", lambda event, arg="popart": self.on_click(event, arg))
        self.popArt_text_label.bind("<Enter>", lambda event, arg="pop", obj=self.popArt_icon_label: self.on_enter(event, arg, obj))
        self.popArt_text_label.bind("<Leave>", lambda event, arg="pop", obj=self.popArt_icon_label: self.on_leave(event, arg, obj))


        # oilpaint button label
        img_oil = PhotoImage(file='icons/oilpaint.png')
        self.oilPaint_icon_label = tk.Label(self.mainWindow, image=img_oil, cursor="hand2")
        self.oilPaint_icon_label.place(x= 30 + 128*2 + 20*2, y=20)
        self.oilPaint_text_label = tk.Label(self.mainWindow, text="Oil Paint", justify=tk.CENTER, cursor="hand2")
        self.oilPaint_text_label.place(x= (30 + 128*2 + 20) + 128/2, y= (20 + 128 + 5))
        self.oilPaint_icon_label.bind("<Enter>", lambda event, arg="oilpaint", obj=self.oilPaint_icon_label: self.on_enter(event, arg, obj))
        self.oilPaint_icon_label.bind("<Leave>", lambda event, arg="oilpaint", obj=self.oilPaint_icon_label: self.on_leave(event, arg, obj))
        self.oilPaint_icon_label.bind("<Button-1>", lambda event, arg="oilpaint": self.on_click(event, arg))
        self.oilPaint_text_label.bind("<Enter>", lambda event, arg="oilpaint", obj=self.oilPaint_icon_label: self.on_enter(event, arg, obj))
        self.oilPaint_text_label.bind("<Leave>", lambda event, arg="oilpaint", obj=self.oilPaint_icon_label: self.on_leave(event, arg, obj))

        # cartoon button label
        img_cartoon = PhotoImage(file='icons/cartoon.png')
        self.cartoon_icon_label = tk.Label(self.mainWindow, image=img_cartoon, cursor="hand2")
        self.cartoon_icon_label.place(x= 30 + 128*3 + 20*3, y=20)
        self.cartoon_text_label = tk.Label(self.mainWindow, text="Cartoon", justify=tk.CENTER, cursor="hand2")
        self.cartoon_text_label.place(x= (30 + 128*3 + 20*2) + 128/2, y= (20 + 128 + 5))
        self.cartoon_icon_label.bind("<Enter>", lambda event, arg="cartoon", obj=self.cartoon_icon_label: self.on_enter(event, arg, obj))
        self.cartoon_icon_label.bind("<Leave>", lambda event, arg="cartoon", obj=self.cartoon_icon_label: self.on_leave(event, arg, obj))
        self.cartoon_text_label.bind("<Enter>", lambda event, arg="cartoon", obj=self.cartoon_icon_label: self.on_enter(event, arg, obj))
        self.cartoon_text_label.bind("<Leave>", lambda event, arg="cartoon", obj=self.cartoon_icon_label: self.on_leave(event, arg, obj))

        # Solarize button label
        img_solarize = PhotoImage(file='icons/solarize.png')
        self.solarize_icon_label = tk.Label(self.mainWindow, image=img_solarize, cursor="hand2")
        self.solarize_icon_label.place(x= 30 + 128*4 + 20*4, y=20)
        self.solarize_text_label = tk.Label(self.mainWindow, text="Solarize", justify=tk.CENTER, cursor="hand2")
        self.solarize_text_label.place(x= (30 + 128*4 + 20*3) + 128/2, y= (20 + 128 + 5))
        self.solarize_icon_label.bind("<Enter>", lambda event, arg="solarize", obj=self.solarize_icon_label: self.on_enter(event, arg, obj))
        self.solarize_icon_label.bind("<Leave>", lambda event, arg="solarize", obj=self.solarize_icon_label: self.on_leave(event, arg, obj))
        self.solarize_icon_label.bind("<Button-1>", lambda event, arg="solarize": self.on_click(event, arg))
        self.solarize_text_label.bind("<Enter>", lambda event, arg="solarize", obj=self.solarize_icon_label: self.on_enter(event, arg, obj))
        self.solarize_text_label.bind("<Leave>", lambda event, arg="solarize", obj=self.solarize_icon_label: self.on_leave(event, arg, obj))

        # Morphology button label
        img_morph = PhotoImage(file='icons/morph.png')
        self.morph_icon_label = tk.Label(self.mainWindow, image=img_morph, cursor="hand2")
        self.morph_icon_label.place(x= 30 + 128*5 + 20*5, y=20)
        self.morph_text_label = tk.Label(self.mainWindow, text="Morphology", justify=tk.CENTER, cursor="hand2")
        self.morph_text_label.place(x= (30 + 128*5 + 20*4 - 10) + 128/2, y= (20 + 128 + 5))
        self.morph_icon_label.bind("<Enter>", lambda event, arg="morph", obj=self.morph_icon_label: self.on_enter(event, arg, obj))
        self.morph_icon_label.bind("<Leave>", lambda event, arg="morph", obj=self.morph_icon_label: self.on_leave(event, arg, obj))
        self.morph_icon_label.bind("<Button-1>", lambda event, arg="morph": self.on_click(event, arg))
        self.morph_text_label.bind("<Enter>", lambda event, arg="morph", obj=self.morph_icon_label: self.on_enter(event, arg, obj))
        self.morph_text_label.bind("<Leave>", lambda event, arg="morph", obj=self.morph_icon_label: self.on_leave(event, arg, obj))

        self.mainWindow.mainloop()



    def getScreenSize(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def getWorking_area(self):
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        return monitor_info.get("Work")

    def on_enter(self, event, icon_name, obj):
        img = PhotoImage(file=f'icons/{icon_name}_h.png')
        obj.config(image= img)
        obj.image = img



    def on_leave(self, event, icon_name, obj):
        img_sketch = PhotoImage(file=f'icons/{icon_name}.png')
        obj.config(image=img_sketch)
        obj.image = img_sketch

    def on_click(self, event, effectName):
        filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                filetypes=[("Image files",
                                                            "*.bmp; *.dib; *.jpeg; *.jpg; *.jp2; *.png; *.webp; *.pbm; "
                                                            "*.pgm; *.ppm; *.pxm; *.pnm; *.sr; *.ras; *.hdr; *.pic")
                                                            ])

        if filename: # Make sure file is selected
            if effectName.lower() == "sketch":
                pencilSketch_GUI(self.mainWindow,filename,self.screen_size_work[2], self.screen_size_work[3], "Sketch")
            elif effectName.lower() == "popart":
                popArt_GUI(self.mainWindow,filename,self.screen_size_work[2], self.screen_size_work[3], "Pop Art")
            elif effectName.lower() == "oilpaint":
                oilPaint_GUI(self.mainWindow,filename,self.screen_size_work[2], self.screen_size_work[3], "Oil Paint")
            elif effectName.lower() == "solarize":
                solarize_GUI(self.mainWindow,filename,self.screen_size_work[2], self.screen_size_work[3], "Solarize")
            elif effectName.lower() == "morph":
                morphology_GUI(self.mainWindow,filename,self.screen_size_work[2], self.screen_size_work[3], "Morphology")
