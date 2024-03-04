import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import threading
import os

class PNGtoWEBPConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PNG to WEBP Converter')
        self.geometry('500x250')

        self.output_folder = ""
        self.create_widgets()

    def create_widgets(self):
        # Frame for file and output folder selection
        frame_selection = tk.Frame(self)
        frame_selection.pack(pady=10)

        # Button to select files
        btn_select = tk.Button(frame_selection, text="Select PNG Files", command=self.select_files)
        btn_select.pack(side=tk.LEFT, padx=10)

        # Button to select output folder
        btn_output_folder = tk.Button(frame_selection, text="Select Output Folder", command=self.select_output_folder)
        btn_output_folder.pack(side=tk.LEFT, padx=10)

        # Frame for conversion quality
        frame_quality = tk.Frame(self)
        frame_quality.pack(pady=10)

        # Slider for quality
        self.quality_slider = tk.Scale(frame_quality, from_=1, to=100, orient=tk.HORIZONTAL, label="Conversion Quality")
        self.quality_slider.set(90)  # Default quality
        self.quality_slider.pack()

        # Frame for conversion action
        frame_action = tk.Frame(self)
        frame_action.pack(pady=10)

        # Button to start conversion
        btn_convert = tk.Button(frame_action, text="Start Conversion", command=self.start_conversion)
        btn_convert.pack(side=tk.LEFT, padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=20)

        # Status label
        self.label_status = tk.Label(self, text="")
        self.label_status.pack(pady=10)

        # List to hold the files
        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("PNG Files", "*.png")])
        self.update_status()

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        self.update_status()

    def update_status(self):
        status_text = f"{len(self.files)} files selected"
        if self.output_folder:
            status_text += f" | Output Folder: {os.path.basename(self.output_folder)}"
        self.label_status.config(text=status_text)

    def start_conversion(self):
        if not self.files:
            messagebox.showerror("Error", "No files selected for conversion!")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Output folder is not selected!")
            return
        
        self.progress['value'] = 0
        self.update_idletasks()

        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self):
        total_files = len(self.files)
        for index, file_path in enumerate(self.files, start=1):
            output_path = os.path.join(self.output_folder, os.path.basename(file_path).rsplit('.', 1)[0] + '.webp')
            try:
                self.convert_png_to_webp(file_path, output_path, self.quality_slider.get())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {os.path.basename(file_path)}: {e}")
                continue
            progress = (index / total_files) * 100
            self.progress['value'] = progress
            self.label_status.config(text=f"Converting: {index}/{total_files}")
            self.update_idletasks()
        
        self.label_status.config(text="Conversion completed. Opening output folder...")
        self.open_output_folder()

    def convert_png_to_webp(self, input_path, output_path, quality=90):
        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGB")
            img.save(output_path, "WEBP", quality=quality)

    def open_output_folder(self):
        try:
            os.startfile(self.output_folder)
        except AttributeError:
            # os.startfile isn't available on macOS or Linux, so use alternatives
            if os.name == 'posix':
                os.system(f'open "{self.output_folder}"')
            else:
                os.system(f'xdg-open "{self.output_folder}"')
        messagebox.showinfo("Success", "All files have been converted and output folder is opened.")

if __name__ == "__main__":
    app = PNGtoWEBPConverter()
    app.mainloop()