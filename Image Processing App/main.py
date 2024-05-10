import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import numpy as np

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing App")

        self.max_canvas_width = 800
        self.max_canvas_height = 600

        self.canvas = tk.Canvas(self.master, bg="white", width=self.max_canvas_width, height=self.max_canvas_height)
        self.canvas.pack()

        self.load_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.process_buttons_frame = tk.Frame(self.master)
        self.process_buttons_frame.pack()

        self.blur_button = tk.Button(self.process_buttons_frame, text="Blur", command=self.blur_image, state=tk.DISABLED)
        self.blur_button.pack(side=tk.LEFT, padx=5)

        self.edge_detect_button = tk.Button(self.process_buttons_frame, text="Edge Detection", command=self.edge_detect_image, state=tk.DISABLED)
        self.edge_detect_button.pack(side=tk.LEFT, padx=5)

        self.resize_button = tk.Button(self.process_buttons_frame, text="Resize", command=self.resize_image, state=tk.DISABLED)
        self.resize_button.pack(side=tk.LEFT, padx=5)

        self.add_noise_button = tk.Button(self.process_buttons_frame, text="Add Noise", command=self.add_noise_image, state=tk.DISABLED)
        self.add_noise_button.pack(side=tk.LEFT, padx=5)

        self.remove_noise_button = tk.Button(self.process_buttons_frame, text="Remove Noise", command=self.remove_noise_image, state=tk.DISABLED)
        self.remove_noise_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack()

        self.image_path = None
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.display_image(self.original_image)
            self.enable_process_buttons()

    def enable_process_buttons(self):
        self.blur_button.config(state=tk.NORMAL)
        self.edge_detect_button.config(state=tk.NORMAL)
        self.resize_button.config(state=tk.NORMAL)
        self.add_noise_button.config(state=tk.NORMAL)
        self.remove_noise_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)

    def display_image(self, image):
        # Resize the image if it exceeds the maximum canvas size
        width, height = image.size
        if width > self.max_canvas_width or height > self.max_canvas_height:
            ratio = min(self.max_canvas_width / width, self.max_canvas_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height))

        self.canvas.delete("all")
        self.img_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
        self.canvas.config(width=new_width, height=new_height)

    def blur_image(self):
        if self.original_image:
            blur_radius = 5  # Increase the blur radius for a stronger effect
            self.processed_image = self.original_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            self.display_image(self.processed_image)

    def edge_detect_image(self):
        if self.original_image:
            gray_image = self.original_image.convert('L')
            gray_array = np.array(gray_image)
            edge_array = np.abs(np.gradient(gray_array)[0]) + np.abs(np.gradient(gray_array)[1])
            edge_image = Image.fromarray(edge_array.astype(np.uint8))
            self.display_image(edge_image)

    def resize_image(self):
        if self.original_image:
            new_width = 400
            new_height = int(self.original_image.height * (new_width / self.original_image.width))
            self.processed_image = self.original_image.resize((new_width, new_height))
            self.display_image(self.processed_image)

    def add_noise_image(self):
        if self.original_image:
            noisy_image = np.array(self.original_image)
            noise = np.random.normal(loc=0, scale=50, size=noisy_image.shape)  # Increased scale for more effect
            noisy_image = np.clip(noisy_image + noise, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(noisy_image)
            self.display_image(self.processed_image)

    def remove_noise_image(self):
        if self.original_image:
            self.processed_image = self.original_image.filter(ImageFilter.SMOOTH)
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                try:
                    self.processed_image.save(save_path)
                    print("Processed image saved successfully!")
                except Exception as e:
                    print(f"Error saving processed image: {e}")
        else:
            print("No processed image available to save.")

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
