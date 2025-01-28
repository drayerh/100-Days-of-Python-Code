import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont, UnidentifiedImageError

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.geometry("800x600")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
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

        self.add_watermark_button = tk.Button(root, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.image = None
        self.watermarked_image = None
        self.logo = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.display_image(self.image)
            except UnidentifiedImageError:
                messagebox.showerror("Error", "The selected file is not a valid image")

    def upload_logo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.logo = Image.open(file_path)
            except UnidentifiedImageError:
                messagebox.showerror("Error", "The selected file is not a valid image")

    def display_image(self, image):
        image.thumbnail((800, 600))
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)

    def add_watermark(self):
        if not self.image:
            messagebox.showerror("Error", "Please upload an image first")
            return

        self.watermarked_image = self.image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)
        width, height = self.watermarked_image.size

        if self.watermark_type.get() == "text":
            watermark_text = self.watermark_text_entry.get()
            if not watermark_text:
                messagebox.showerror("Error", "Please enter watermark text")
                return
            font = ImageFont.load_default()
            text_width, text_height = draw.textsize(watermark_text, font)
            x, y = width - text_width - 10, height - text_height - 10
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))
        elif self.watermark_type.get() == "logo":
            if not self.logo:
                messagebox.showerror("Error", "Please upload a logo")
                return
            logo_width, logo_height = self.logo.size
            x, y = width - logo_width - 10, height - logo_height - 10
            self.watermarked_image.paste(self.logo, (x, y), self.logo)

        self.display_image(self.watermarked_image)

    def save_image(self):
        if not self.watermarked_image:
            messagebox.showerror("Error", "No watermarked image to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.watermarked_image.save(file_path)
            messagebox.showinfo("Success", "Image saved successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()