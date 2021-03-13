from GUI_modules.main_canvas import *
from tkinter.font import BOLD, Font
from algorithms.pop_art import *
from algorithms.pop_art_GPU import *
from tkinter import colorchooser

class popArt_GUI:
    def __init__(self, root, imagePath, work_width, work_height, effectName):
        self.mainCanvas = canvas_GUI(root, imagePath, work_width, work_height, effectName)
        self.processButton = None
        self.background_color = [255, 255, 255]
        self.backgroundColor_label = None
        self.backgroundColor_btn = None
        self.backgroundColor_disp = None
        self.dots_color = [0, 0, 0]
        self.dotsColor_label = None
        self.dotsColor_btn = None
        self.dotsColor_disp = None
        self.dots_slider_label = None
        self.dots_slider = None
        self.multiplier_slider_label = None
        self.multiplier_slider = None
        self.GPU_OPTIMIZE = None
        self.IS_GPU_OPTIMIZED = False
        self.draw_GUI()

    def draw_GUI(self):
        self.mainCanvas.draw_window()
        self.mainCanvas.root.update()
        self.mainCanvas.adjustment_area.pack_propagate(0)
        self.mainCanvas.adjustment_area.grid_propagate(0)

        adjust_height = self.mainCanvas.adjustment_area.winfo_height()
        adjust_width = self.mainCanvas.adjustment_area.winfo_width()

        # background color label, color chooser and selected color
        self.backgroundColor_label = tk.Label(self.mainCanvas.adjustment_area, text="Background color: ", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.backgroundColor_btn = tk.Button(self.mainCanvas.adjustment_area, text="Select Color", height=2, width=10, command=lambda background=True: self.color_chooser(background))
        self.backgroundColor_disp = tk.Label(self.mainCanvas.adjustment_area, borderwidth=1, relief="solid", bg="white", height=2, width=5)

        self.backgroundColor_label.place(x=adjust_width - adjust_width//1.3, y=adjust_height - adjust_height//1.05)
        self.backgroundColor_btn.place(x=adjust_width - adjust_width//1.3, y=adjust_height - adjust_height//1.05 + 25)
        self.backgroundColor_disp.place(x=adjust_width - adjust_width//1.3 + 90, y=adjust_height - adjust_height//1.05 + 30)

        # dots color label, color chooser and selected color
        self.dotsColor_label = tk.Label(self.mainCanvas.adjustment_area, text="Dots color: ", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.dotsColor_btn = tk.Button(self.mainCanvas.adjustment_area, text="Select Color", height=2, width=10, command=lambda background=False: self.color_chooser(background))
        self.dotsColor_disp = tk.Label(self.mainCanvas.adjustment_area, borderwidth=1, relief="solid", bg="black",height=2, width=5)

        self.mainCanvas.root.update()
        self.dotsColor_label.place(x=adjust_width - adjust_width//1.3, y=adjust_height - adjust_height//1.05 + self.backgroundColor_label.winfo_height() + self.backgroundColor_btn.winfo_height() + 20)
        self.dotsColor_btn.place(x=adjust_width - adjust_width//1.3, y=adjust_height - adjust_height//1.05 + self.backgroundColor_label.winfo_height() + self.backgroundColor_btn.winfo_height() + 20 + 25)
        self.dotsColor_disp.place(x=adjust_width - adjust_width//1.3 + 90, y=adjust_height - adjust_height//1.05 + self.backgroundColor_label.winfo_height() + self.backgroundColor_btn.winfo_height() + 20 + 25 + 5)

        self.multiplier_slider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width // 4, width=adjust_height // 8, orient=tk.HORIZONTAL, from_=2, to=20, showvalue=0, command=self.slider_multiplier_event)
        self.multiplier_slider.place(x=adjust_width - adjust_width//2, y=adjust_height - adjust_height//1.05 + 25)
        self.multiplier_slider_label = tk.Label(self.mainCanvas.adjustment_area, text="Multiplier: 2",font=Font(self.mainCanvas.adjustment_area, size=12))
        self.multiplier_slider_label.place(x=adjust_width - adjust_width//2, y=adjust_height - adjust_height//1.05)
        self.mainCanvas.root.update()

        self.dots_slider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width // 4, width=adjust_height // 8, orient=tk.HORIZONTAL, from_=120, to=self.mainCanvas.ImageInfo.width()//2, showvalue=0, command=self.slider_dots_event)
        self.dots_slider.place(x = adjust_width - adjust_width // 2, y = adjust_height - adjust_height // 1.05 + self.multiplier_slider_label.winfo_height() + self.multiplier_slider.winfo_height() + 20 + 25)
        self.dots_slider_label = tk.Label(self.mainCanvas.adjustment_area, text="Horizontal Dots: 120", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.dots_slider_label.place(x=adjust_width - adjust_width // 2, y=adjust_height - adjust_height // 1.05 + self.multiplier_slider_label.winfo_height() + self.multiplier_slider.winfo_height() + 20)
        self.mainCanvas.root.update()

        # GPU OPTIMIZE Button
        self.GPU_OPTIMIZE = tk.Checkbutton(self.mainCanvas.adjustment_area,
                                           text="Use GPU optimization (For real time processing)",
                                           command=self.GPU_toggle)
        self.GPU_OPTIMIZE.place(x=adjust_width//2, y=adjust_height - adjust_height//1.05 + self.backgroundColor_label.winfo_height() + self.backgroundColor_btn.winfo_height() + self.dotsColor_label.winfo_height() + self.dotsColor_btn.winfo_height() + 20 + 10 )
        self.GPU_OPTIMIZE.deselect()



        # Process button
        self.processButton = tk.Button(self.mainCanvas.adjustment_area, text="Process Image (CPU)", command=self.processImage)
        self.processButton.place(x=adjust_width, y=adjust_height)
        self.mainCanvas.root.update()
        self.processButton.place(x=adjust_width - self.processButton.winfo_width() - 15, y=adjust_height - self.processButton.winfo_height() - 25)


    def GPU_toggle(self):
        if(self.IS_GPU_OPTIMIZED):
            self.IS_GPU_OPTIMIZED = False
        else:
            self.IS_GPU_OPTIMIZED = True

    def processImage(self):
        if (not self.IS_GPU_OPTIMIZED):
            popART = popArt(None, cv2.cvtColor(np.array(self.mainCanvas.PIL_image), cv2.COLOR_RGB2BGR))
            results = popART.perform_popArt(self.background_color, self.dots_color, (int)(self.multiplier_slider.get()), (int)(self.dots_slider.get()))
            PIL_Image = Image.fromarray(results)
            PIL_Image = PIL_Image.resize((self.mainCanvas.ImageInfo.width(), self.mainCanvas.ImageInfo.height()))
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

    def real_time_process(self):
        if (self.IS_GPU_OPTIMIZED):
            results = popArt(cv2.cvtColor(np.array(self.mainCanvas.PIL_image), cv2.COLOR_RGB2BGR), self.background_color, self.dots_color, (int)(self.multiplier_slider.get()), (int)(self.dots_slider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

    def slider_multiplier_event(self, n):
        self.multiplier_slider_label['text'] = f"Multiplier: {n}"
        self.real_time_process()

    def slider_dots_event(self, n):
        self.dots_slider_label['text'] = f"Horizontal Dots: {n}"
        self.real_time_process()

    def color_chooser(self, isBackground):
            color_code = colorchooser.askcolor(title="Choose color")
            if color_code:
                if isBackground:
                    self.background_color = [(int)(color_code[0][0]), (int)(color_code[0][1]), (int)(color_code[0][2])]
                    self.backgroundColor_disp['bg'] = color_code[1]
                else:
                    self.dots_color = [(int)(color_code[0][0]), (int)(color_code[0][1]), (int)(color_code[0][2])]
                    self.dotsColor_disp['bg'] = color_code[1]
                self.real_time_process()


