import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Курбонзода Зухал")
        self.pack()
        self.create_widgets()
        self.transformations = []
        self.master.configure(bg="#FFFFFF")
        self.configure(bg="#FFFFFF")
        self.left_frame.configure(bg="#FFFFFF")
        self.right_frame.configure(bg="#FFFFFF")
        self.image_label.configure(bg="#FFFFFF")

    def create_widgets(self):
        button_width = 24

        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left")

        self.open_button = tk.Button(self.left_frame, width=button_width)
        self.open_button["text"] = "Открыть"
        self.open_button["command"] = self.load_image
        self.open_button.pack(side="top")

        self.affine_button = tk.Button(self.left_frame, width=button_width)
        self.affine_button["text"] = "Афинные преобразования"
        self.affine_button["command"] = self.apply_affine_transformation
        self.affine_button.pack(side="top")

        self.nonlinear_button = tk.Button(self.left_frame, width=button_width)
        self.nonlinear_button["text"] = "Нелинейные преобразования"
        self.nonlinear_button["command"] = self.apply_nonlinear_transformation
        self.nonlinear_button.pack(side="top")

        self.save_button = tk.Button(self.left_frame, width=button_width)
        self.save_button["text"] = "Сохранить"
        self.save_button["command"] = self.save_result
        self.save_button.pack(side="top")

        self.restore_button = tk.Button(self.left_frame, width=button_width)
        self.restore_button["text"] = "Восстановить"
        self.restore_button["command"] = self.restore_original
        self.restore_button.pack(side="top")

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="y")

        self.image_label = tk.Label(self.right_frame)
        self.image_label.pack(fill="both", expand=True)

        self.original_image = None
        self.transformed_image = None

    def load_image(self):
        image_path = filedialog.askopenfilename()
        self.source_image = Image.open(image_path)
        self.processed_image = self.source_image.copy()
        self.processed_image.thumbnail((800, 400))
        self.display_image = ImageTk.PhotoImage(self.processed_image)
        self.image_label.config(image=self.display_image)
        self.transformation_history = []
    
    
    def apply_affine_transformation(self):
        if self.processed_image:
            angle = 30 
            skew = 0.5

            self.processed_image = self.processed_image.transform(self.processed_image.size, Image.AFFINE, (np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0, np.sin(np.radians(angle)), np.cos(np.radians(angle)), skew))
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history.append(("affine", angle, skew))
    
    def apply_nonlinear_transformation(self):
        if self.processed_image:
            pixel_array = np.array(self.processed_image)
            width, height = pixel_array.shape[1], pixel_array.shape[0]
            transformed_array = np.zeros_like(pixel_array)
            coordinate_map = []
            for i in range(height):
                for j in range(width):
                    x_prime = np.sqrt(np.exp(j))
                    y_prime = i
                    i_prime = int(y_prime)
                    j_prime = int(x_prime)
                    if 0 <= i_prime < height and 0 <= j_prime < width:
                        transformed_array[i, j] = pixel_array[i_prime, j_prime]
                        coordinate_map.append((i_prime, j_prime))
            self.processed_image = Image.fromarray(transformed_array)
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history.append(("nonlinear", coordinate_map))
    
    def save_result(self):
        if self.processed_image:
            filename, file_extension = os.path.splitext(self.source_image.filename)
            output_filename = f"{filename}_out.jpg"
            self.processed_image.save(output_filename)
    
    def restore_original(self):
        if self.transformation_history:
            for transformation in reversed(self.transformation_history):
                if transformation[0] == "affine":
                    angle = -transformation[1]
                    skew = -transformation[2]
                    self.processed_image = self.processed_image.transform(self.processed_image.size, Image.AFFINE, (np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0, np.sin(np.radians(angle)), np.cos(np.radians(angle)), skew))
            self.display_image = ImageTk.PhotoImage(self.processed_image)
            self.image_label.config(image=self.display_image)
            self.transformation_history = []
            self.transformations = []
    
root = tk.Tk()
app = Application(master=root)
app.mainloop()