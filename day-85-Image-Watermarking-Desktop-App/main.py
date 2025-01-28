import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import (Image, ImageTk, ImageDraw, ImageFont, UnidentifiedImageError)

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.geometry("800x600")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.upload_button = tk.Button(root, text="Upload Images", command=self.upload_images)
        self.upload_button.pack()

        self.watermark_text_entry = tk.Entry(root, width=50)
        self.watermark_text_entry.pack()
        self.watermark_text_entry.insert(0, "Enter watermark text here")

        self.upload_logo_button = tk.Button(root, text="Upload Logo", command=self.upload_logo)
        self.upload_logo_button.pack()

        self.watermark_type = tk.StringVar(value="text")
        self.text_radio = tk.Radiobutton(root, text="Text Watermark", variable=self.watermark_type, value="text")
        self.text_radio.pack()
        self.logo_radio = tk.Radiobutton(root, text="Logo Watermark", variable=self.watermark_type, value="logo")
        self.logo_radio.pack()

        self.transparency_label = tk.Label(root, text="Transparency:")
        self.transparency_label.pack()
        self.transparency_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.transparency_slider.set(128)
        self.transparency_slider.pack()

        self.x_position_label = tk.Label(root, text="X Position:")
        self.x_position_label.pack()
        self.x_position_slider = tk.Scale(root, from_=0, to=800, orient=tk.HORIZONTAL)
        self.x_position_slider.set(0)
        self.x_position_slider.pack()

        self.y_position_label = tk.Label(root, text="Y Position:")
        self.y_position_label.pack()
        self.y_position_slider = tk.Scale(root, from_=0, to=600, orient=tk.HORIZONTAL)
        self.y_position_slider.set(0)
        self.y_position_slider.pack()

        self.add_watermark_button = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()

        self.preview_button = tk.Button(root, text="Preview Next Image", command=self.preview_next_image)
        self.preview_button.pack()

        self.save_button = tk.Button(root, text="Save Images", command=self.save_images)
        self.save_button.pack()

        self.images = []
        self.watermarked_images = []
        self.logo = None
        self.current_preview_index = 0

    def upload_images(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.images = []
            for file_path in file_paths:
                try:
                    image = Image.open(file_path)
                    self.images.append(image)
                except UnidentifiedImageError:
                    messagebox.showerror("Error", f"The selected file {file_path} is not a valid image")
            if self.images:
                self.display_image(self.images[0])

    def upload_logo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.logo = Image.open(file_path)
            except UnidentifiedImageError:
                messagebox.showerror("Error", "The selected file is not a valid image")

    def display_image(self, image):
        image.thumbnail((800, 600))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def add_watermark(self):
        if not self.images:
            messagebox.showerror("Error", "Please upload images first")
            return

        self.watermarked_images = []
        transparency = self.transparency_slider.get()
        x_position = self.x_position_slider.get()
        y_position = self.y_position_slider.get()

        for image in self.images:
            watermarked_image = image.copy()
            draw = ImageDraw.Draw(watermarked_image)
            width, height = watermarked_image.size

            if self.watermark_type.get() == "text":
                watermark_text = self.watermark_text_entry.get()
                if not watermark_text:
                    messagebox.showerror("Error", "Please enter watermark text")
                    return
                font = ImageFont.load_default()
                draw.text((x_position, y_position), watermark_text, font=font, fill=(255, 255, 255, transparency))
            elif self.watermark_type.get() == "logo":
                if not self.logo:
                    messagebox.showerror("Error", "Please upload a logo")
                    return
                logo = self.logo.copy()
                logo.putalpha(transparency)
                watermarked_image.paste(logo, (x_position, y_position), logo)

            self.watermarked_images.append(watermarked_image)

        self.current_preview_index = 0
        self.display_image(self.watermarked_images[0])

    def preview_next_image(self):
        if not self.watermarked_images:
            messagebox.showerror("Error", "No watermarked images to preview")
            return

        self.current_preview_index = (self.current_preview_index + 1) % len(self.watermarked_images)
        self.display_image(self.watermarked_images[self.current_preview_index])

    def save_images(self):
        if not self.watermarked_images:
            messagebox.showerror("Error", "No watermarked images to save")
            return

        save_dir = filedialog.askdirectory()
        if save_dir:
            for i, watermarked_image in enumerate(self.watermarked_images):
                file_path = f"{save_dir}/watermarked_image_{i + 1}.png"
                watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Images saved successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()