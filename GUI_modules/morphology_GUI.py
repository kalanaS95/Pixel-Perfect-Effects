from GUI_modules.main_canvas import *
from tkinter.font import BOLD, Font
from algorithms.solarize import *
from algorithms.solarize_GPU import *


class morphology_GUI:
    def __init__(self, root, imagePath, work_width, work_height, effectName):
        self.mainCanvas = canvas_GUI(root, imagePath, work_width, work_height, effectName)
        self.b_k_label = None
        self.b_k_checkbox = None
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



        # GPU OPTIMIZE Button
        #self.GPU_OPTIMIZE = tk.Checkbutton(self.mainCanvas.adjustment_area, text="Use GPU optimization (For real time processing)", command=self.GPU_toggle)
        #self.GPU_OPTIMIZE.place(x=adjust_width // 4,y=adjust_height // 12 + self.RThresholdSlider.winfo_height() + self.GThresholdLabel.winfo_height() + self.GThresholdSlider.winfo_height() + self.BThresholdLabel.winfo_height() + self.BThresholdSlider.winfo_height() + 5)
        #self.GPU_OPTIMIZE.deselect()

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
            solarize_ = solarize(self.mainCanvas.ImagePath, np.array(self.mainCanvas.PIL_image))
            results = solarize_.perform_solarization((int)(self.BThresholdSlider.get()), (int)(self.GThresholdSlider.get()), (int)(self.RThresholdSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

    def real_time_process(self):
        if (self.IS_GPU_OPTIMIZED):
            pass
            results = perform_solarization(np.array(self.mainCanvas.PIL_image), (int)(self.BThresholdSlider.get()), (int)(self.GThresholdSlider.get()), (int)(self.RThresholdSlider.get()))
            PIL_Image = Image.fromarray(results)
            photo_result = ImageTk.PhotoImage(PIL_Image)
            self.mainCanvas.render_result_image(photo_result)

