from GUI_modules.main_canvas import *
from tkinter.font import BOLD, Font
from algorithms.solarize import *
from algorithms.solarize_GPU import *


class solarize_GUI:
    def __init__(self, root, imagePath, work_width, work_height, effectName):
        self.mainCanvas = canvas_GUI(root, imagePath, work_width, work_height, effectName)
        self.RThresholdSlider = None
        self.RThresholdLabel = None
        self.GThresholdLabel = None
        self.GThresholdSlider = None
        self.BThresholdLabel = None
        self.BThresholdSlider = None
        self.processButton = None
        self.GPU_OPTIMIZE = None
        self.IS_GPU_OPTIMIZED = False
        self.draw_GUI()
        # priming the code, this way numba can build code cache and during the next run things willmuch faster !
        perform_solarization(np.array(self.mainCanvas.PIL_image), 10, 10, 10)

    def draw_GUI(self):
        self.mainCanvas.draw_window()
        self.mainCanvas.root.update()

        adjust_height = self.mainCanvas.adjustment_area.winfo_height()
        adjust_width = self.mainCanvas.adjustment_area.winfo_width()

        # draw slider for kernel size
        self.RThresholdSlider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width//2, width=adjust_height//12, orient=tk.HORIZONTAL, from_=10, to=255,  command=self.R_Slide, showvalue=0)
        self.RThresholdSlider.place(x=adjust_width//4, y=adjust_height//12)
        self.RThresholdLabel = tk.Label(self.mainCanvas.adjustment_area, text="Red threshold: 10", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.RThresholdLabel.place(x=adjust_width // 4, y=adjust_height // 12 - 25)
        self.mainCanvas.root.update()

        # Sigma label
        self.GThresholdLabel = tk.Label(self.mainCanvas.adjustment_area, text="Green threshold: 10", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.GThresholdLabel.place(x=adjust_width // 4, y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + 5)
        self.mainCanvas.root.update()
        # Sigma label
        self.GThresholdSlider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width // 2, width=adjust_height // 12, orient=tk.HORIZONTAL, from_=10, to=255, showvalue=0, command=self.G_Slide)
        self.GThresholdSlider.place(x=adjust_width // 4, y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + self.GThresholdLabel.winfo_height() + 5)
        self.mainCanvas.root.update()

        # Sigma label
        self.BThresholdLabel = tk.Label(self.mainCanvas.adjustment_area, text="Blue threshold: 10", font=Font(self.mainCanvas.adjustment_area, size=12))
        self.BThresholdLabel.place(x=adjust_width // 4, y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + self.GThresholdLabel.winfo_height() + self.GThresholdSlider.winfo_height() + 5 + 5)
        self.mainCanvas.root.update()
        # Sigma label
        self.BThresholdSlider = tk.Scale(self.mainCanvas.adjustment_area, length=adjust_width // 2, width=adjust_height // 12, orient=tk.HORIZONTAL, from_=10, to=255, showvalue=0, command=self.B_Slide)
        self.BThresholdSlider.place(x=adjust_width // 4, y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + self.GThresholdLabel.winfo_height() + self.GThresholdSlider.winfo_height() + self.BThresholdLabel.winfo_height() + 5)
        self.mainCanvas.root.update()

        # GPU OPTIMIZE Button
        self.GPU_OPTIMIZE = tk.Checkbutton(self.mainCanvas.adjustment_area, text="Use GPU optimization (For real time processing)", command=self.GPU_toggle)
        self.GPU_OPTIMIZE.place(x=adjust_width // 4,y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + self.GThresholdLabel.winfo_height() + self.GThresholdSlider.winfo_height() + self.BThresholdLabel.winfo_height() + self.BThresholdSlider.winfo_height() + 5)
        self.GPU_OPTIMIZE.deselect()

        # Process button
        self.processButton = tk.Button(self.mainCanvas.adjustment_area, text="Process Image (CPU)", command=self.processImage)
        self.processButton.place(x=adjust_width, y=adjust_height)
        self.mainCanvas.root.update()
        self.processButton.place(x=adjust_width - self.processButton.winfo_width() - 15, y=adjust_height - self.processButton.winfo_height() - 25)


    def R_Slide(self, n):
        self.RThresholdLabel['text'] = f"Red threshold: {n}"
        self.real_time_process()


    def G_Slide(self, n):
        self.GThresholdLabel['text'] = f"Green threshold: {n}"
        self.real_time_process()

    def B_Slide(self, n):
        self.BThresholdLabel['text'] = f"Blue threshold: {n}"
        self.real_time_process()

    def GPU_toggle(self):
        if(self.IS_GPU_OPTIMIZED):
            self.IS_GPU_OPTIMIZED = False
        else:
            self.IS_GPU_OPTIMIZED = True

    def processImage(self):
        if (not self.IS_GPU_OPTIMIZED):
            solarize_ = solarize(self.mainCanvas.ImagePath, np.array(self.mainCanvas.PIL_image))
            results = solarize_.perform_solarization((int)(self.BThresholdSlider.get()), (int)(self.GThresholdSlider.get()), (int)(self.RThresholdSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

    def real_time_process(self):
        if (self.IS_GPU_OPTIMIZED):
            results = perform_solarization(np.array(self.mainCanvas.PIL_image), (int)(self.BThresholdSlider.get()), (int)(self.GThresholdSlider.get()), (int)(self.RThresholdSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

