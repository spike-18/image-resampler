import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
from PIL import Image, ImageTk

from .io import load_image, save_image
from .methods import (
    bilinear_interpolation,
    l2_optimal_interpolation,
    nearest_neighbor,
    piecewise_linear_interpolation,
)


class UpscaleApp(tk.Tk):
    """
    Tkinter-based GUI application for interactive image upscaling.

    Features:
        - Load an image from disk
        - Select upscaling method and scale
        - Preview upscaled result
        - Save upscaled image
        - Modern, user-friendly interface
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Image Upscaling App")
        self.geometry("800x600")
        self.image = None
        self.out_image = None
        self.create_widgets()

    def create_widgets(self) -> None:
        # Use a modern font and color scheme
        font = ("Segoe UI", 11)
        bg = "#222831"
        fg = "#eeeeee"
        btn_bg = "#393e46"
        btn_fg = "#00adb5"
        entry_bg = "#393e46"
        entry_fg = "#eeeeee"
        status_bg = "#393e46"
        status_fg = "#00adb5"

        self.configure(bg=bg)

        # Frame for controls
        control_frame = tk.Frame(self, padx=18, pady=18, bg=bg)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.open_btn = tk.Button(
            control_frame,
            text="Open Image",
            width=20,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.open_image,
        )
        self.open_btn.pack(pady=(0, 16))

        tk.Label(control_frame, text="Method:", anchor="w", font=font, bg=bg, fg=fg).pack(fill=tk.X)
        self.method_var = tk.StringVar(value="Bilinear")
        method_menu = tk.OptionMenu(
            control_frame,
            self.method_var,
            "Nearest Neighbor",
            "Bilinear",
            "Piecewise Linear",
            "L2 Optimal",
        )
        method_menu.config(width=18, font=font, bg=btn_bg, fg=btn_fg, highlightthickness=0)
        method_menu.pack(pady=(0, 16))

        tk.Label(control_frame, text="Scale:", anchor="w", font=font, bg=bg, fg=fg).pack(fill=tk.X)
        self.scale_var = tk.IntVar(value=2)
        scale_entry = tk.Entry(
            control_frame,
            textvariable=self.scale_var,
            width=20,
            font=font,
            bg=entry_bg,
            fg=entry_fg,
        )
        scale_entry.pack(pady=(0, 16))

        self.upscale_btn = tk.Button(
            control_frame,
            text="Upscale",
            width=20,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.upscale,
        )
        self.upscale_btn.pack(pady=(0, 16))

        self.save_btn = tk.Button(
            control_frame,
            text="Save Result",
            width=20,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.save_result,
        )
        self.save_btn.pack(pady=(0, 16))

        # Frame for image display
        image_frame = tk.Frame(self, padx=10, pady=10, bg=bg)
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.img_label = tk.Label(image_frame, bg=bg, relief=tk.SUNKEN, borderwidth=2)
        self.img_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Status bar
        self.status_var = tk.StringVar(value="Welcome to Image Upscaling App!")
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 10),
            bg=status_bg,
            fg=status_fg,
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open_image(self) -> None:
        path = filedialog.askopenfilename()
        if path:
            self.image = load_image(path)
            self.display_image(self.image)
            self.status_var.set(f"Loaded: {path}")

    def upscale(self) -> None:
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        method = self.method_var.get()
        scale = self.scale_var.get()
        self.status_var.set(f"Upscaling with {method} (scale={scale})...")
        self.update_idletasks()
        match method:
            case "Nearest Neighbor":
                self.out_image = nearest_neighbor(self.image, scale)
            case "Bilinear":
                self.out_image = bilinear_interpolation(self.image, scale)
            case "Piecewise Linear":
                self.out_image = piecewise_linear_interpolation(self.image, scale)
            case "L2 Optimal":
                self.out_image = l2_optimal_interpolation(self.image, scale)
        self.display_image(self.out_image)
        self.status_var.set(f"Upscaled using {method} (scale={scale})")

    def save_result(self) -> None:
        if self.out_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                save_image(self.out_image, path)
                messagebox.showinfo("Saved", f"Image saved to {path}")
                self.status_var.set(f"Saved: {path}")

    def display_image(self, img_arr: np.ndarray) -> None:
        img = Image.fromarray(img_arr)
        img.thumbnail((500, 500))
        imgtk = ImageTk.PhotoImage(img)
        self.img_label.imgtk = imgtk
        self.img_label.config(image=imgtk)


def rungui() -> None:
    app = UpscaleApp()
    app.mainloop()
