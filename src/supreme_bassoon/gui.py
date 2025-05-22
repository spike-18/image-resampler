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

        # Top control panel
        control_frame = tk.Frame(self, bg=bg, padx=10, pady=5)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Left side controls
        left_controls = tk.Frame(control_frame, bg=bg)
        left_controls.pack(side=tk.LEFT, padx=5)

        self.open_btn = tk.Button(
            left_controls,
            text="Open Image",
            width=15,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.open_image,
        )
        self.open_btn.pack(side=tk.LEFT, padx=5)

        # Center controls
        center_controls = tk.Frame(control_frame, bg=bg)
        center_controls.pack(side=tk.LEFT, padx=5)

        method_frame = tk.Frame(center_controls, bg=bg)
        method_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(method_frame, text="Method:", font=font, bg=bg, fg=fg).pack(side=tk.LEFT)
        self.method_var = tk.StringVar(value="Bilinear")
        method_menu = tk.OptionMenu(
            method_frame,
            self.method_var,
            "Nearest Neighbor",
            "Bilinear",
            "Piecewise Linear",
            "L2 Optimal",
        )
        method_menu.config(font=font, bg=btn_bg, fg=btn_fg, highlightthickness=0)
        method_menu.pack(side=tk.LEFT, padx=5)

        scale_frame = tk.Frame(center_controls, bg=bg)
        scale_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(scale_frame, text="Scale:", font=font, bg=bg, fg=fg).pack(side=tk.LEFT)
        self.scale_var = tk.IntVar(value=2)
        scale_entry = tk.Entry(
            scale_frame,
            textvariable=self.scale_var,
            width=5,
            font=font,
            bg=entry_bg,
            fg=entry_fg,
        )
        scale_entry.pack(side=tk.LEFT, padx=5)

        # Right side controls
        right_controls = tk.Frame(control_frame, bg=bg)
        right_controls.pack(side=tk.RIGHT, padx=5)

        self.upscale_btn = tk.Button(
            right_controls,
            text="Upscale",
            width=10,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.upscale,
        )
        self.upscale_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(
            right_controls,
            text="Save Result",
            width=10,
            font=font,
            bg=btn_bg,
            fg=btn_fg,
            command=self.save_result,
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # Images container
        images_frame = tk.Frame(self, bg=bg)
        images_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Add a zoom slider above the images
        zoom_frame = tk.Frame(images_frame, bg=bg)
        zoom_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        tk.Label(
            zoom_frame,
            text="Zoom:",
            font=font,
            bg=bg,
            fg=fg,
        ).pack(side=tk.LEFT)
        self.zoom_var = tk.DoubleVar(value=1.0)
        zoom_slider = tk.Scale(
            zoom_frame,
            from_=1.0,
            to=16.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.zoom_var,
            length=300,
            showvalue=True,
            bg=bg,
            fg=fg,
            troughcolor=btn_bg,
            highlightthickness=0,
            command=lambda _: self.update_images_zoom(),
        )
        zoom_slider.pack(side=tk.LEFT, padx=10)

        # Original image frame
        original_frame = tk.Frame(images_frame, bg=bg)
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(original_frame, text="Original", font=font, bg=bg, fg=fg).pack()
        self.original_label = tk.Label(original_frame, bg=bg, relief=tk.SUNKEN, borderwidth=2)
        self.original_label.pack(fill=tk.BOTH, expand=True, pady=5)

        # Result image frame
        result_frame = tk.Frame(images_frame, bg=bg)
        result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(result_frame, text="Upscaled", font=font, bg=bg, fg=fg).pack()
        self.result_label = tk.Label(result_frame, bg=bg, relief=tk.SUNKEN, borderwidth=2)
        self.result_label.pack(fill=tk.BOTH, expand=True, pady=5)

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
            self.display_original(self.image)
            self.status_var.set(f"Loaded: {path}")

    def _update_label_image(self, label, img_arr, zoom=1.0, scale_factor=1.0) -> None:
        if img_arr is None:
            return
        # Fixed display area
        display_w, display_h = 400, 400
        img = Image.fromarray(img_arr)
        w, h = img.size
        # Adjust zoom for upscaled image so it appears smaller by scale_factor initially
        effective_zoom = zoom / scale_factor if scale_factor != 1.0 else zoom
        new_w, new_h = max(1, int(w * effective_zoom)), max(1, int(h * effective_zoom))
        img = img.resize((new_w, new_h), Image.NEAREST)
        # Center crop to display area
        left = max(0, (new_w - display_w) // 2)
        upper = max(0, (new_h - display_h) // 2)
        right = left + display_w
        lower = upper + display_h
        img = img.crop((left, upper, right, lower))
        imgtk = ImageTk.PhotoImage(img)
        label.imgtk = imgtk
        label.config(image=imgtk, width=display_w, height=display_h)

    def display_original(self, img_arr: np.ndarray) -> None:
        self._original_img_arr = img_arr.copy() if img_arr is not None else None
        self._update_label_image(self.original_label, img_arr)

    def display_result(self, img_arr: np.ndarray) -> None:
        self._result_img_arr = img_arr.copy() if img_arr is not None else None
        # Use the current scale factor for initial display
        scale = self.scale_var.get() if hasattr(self, "scale_var") else 1.0
        self._update_label_image(self.result_label, img_arr, scale_factor=scale)

    def update_images_zoom(self) -> None:
        zoom = self.zoom_var.get() if hasattr(self, "zoom_var") else 1.0
        scale = self.scale_var.get() if hasattr(self, "scale_var") else 1.0
        if hasattr(self, "_original_img_arr") and self._original_img_arr is not None:
            self._update_label_image(self.original_label, self._original_img_arr, zoom)
        if hasattr(self, "_result_img_arr") and self._result_img_arr is not None:
            self._update_label_image(
                self.result_label, self._result_img_arr, zoom, scale_factor=scale
            )

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
        self.display_result(self.out_image)
        self.status_var.set(f"Upscaled using {method} (scale={scale})")

    def save_result(self) -> None:
        if self.out_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path:
                save_image(self.out_image, path)
                messagebox.showinfo("Saved", f"Image saved to {path}")
                self.status_var.set(f"Saved: {path}")


def rungui() -> None:
    app = UpscaleApp()
    app.mainloop()
