import contextlib

from supreme_bassoon.gui import UpscaleApp


def test_gui_instantiates(monkeypatch) -> None:
    # Patch Tkinter mainloop to avoid opening a window
    monkeypatch.setattr(UpscaleApp, "mainloop", lambda *_a, **_k: None)
    app = UpscaleApp()
    assert hasattr(app, "create_widgets")
    assert hasattr(app, "open_image")
    assert hasattr(app, "upscale")
    assert hasattr(app, "save_result")
    assert hasattr(app, "display_image")


def test_gui_methods(monkeypatch) -> None:
    # Patch methods to avoid side effects
    app = UpscaleApp()
    monkeypatch.setattr(app, "display_image", lambda *_a, **_k: None)
    app.image = None
    app.out_image = None
    # open_image should not fail if no file is selected
    monkeypatch.setattr("tkinter.filedialog.askopenfilename", lambda *_a, **_k: "")
    app.open_image()
    # save_result should not fail if out_image is None
    app.save_result()


def test_gui_all_buttons(monkeypatch) -> None:
    app = UpscaleApp()
    # Patch all file dialogs and messageboxes with generic lambdas that accept any args
    monkeypatch.setattr("tkinter.filedialog.askopenfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.filedialog.asksaveasfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *_a, **_k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *_a, **_k: None)
    monkeypatch.setattr(app, "display_image", lambda *_a, **_k: None)
    # Simulate button presses
    app.open_image()  # Should handle no file
    app.upscale()     # Should handle no image
    app.save_result() # Should handle no out_image
    # Now set dummy images and test again
    import numpy as np
    app.image = np.zeros((8, 8), dtype=np.uint8)
    app.out_image = np.ones((8, 8), dtype=np.uint8)
    app.upscale()
    app.save_result()
    app.create_widgets()


def test_gui_menu(monkeypatch) -> None:
    app = UpscaleApp()
    # Patch all file dialogs and messageboxes
    monkeypatch.setattr("tkinter.filedialog.askopenfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.filedialog.asksaveasfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *_a, **_k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *_a, **_k: None)
    monkeypatch.setattr(app, "display_image", lambda *_a, **_k: None)
    # Simulate menu actions if present
    if hasattr(app, "menubar"):
        for menu in app.menubar.winfo_children():
            with contextlib.suppress(Exception):
                menu.invoke(0)
    # Simulate method/scale changes if present
    if hasattr(app, "method_var"):
        app.method_var.set("Bilinear")
    if hasattr(app, "scale_var"):
        app.scale_var.set(2)
    # Simulate window close if present
    if hasattr(app, "destroy"):
        app.destroy()


# Additional tests for coverage of gui.py

def test_gui_upscale_with_method(monkeypatch) -> None:
    app = UpscaleApp()
    monkeypatch.setattr("tkinter.filedialog.askopenfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.filedialog.asksaveasfilename", lambda *_a, **_k: "")
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *_a, **_k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *_a, **_k: None)
    monkeypatch.setattr(app, "display_image", lambda *_a, **_k: None)
    import numpy as np
    app.image = np.zeros((8, 8), dtype=np.uint8)
    app.method_var.set("Nearest Neighbor")
    app.scale_var.set(2)
    app.upscale()
    app.method_var.set("Bilinear")
    app.upscale()
    app.method_var.set("Piecewise Linear")
    app.upscale()
    app.method_var.set("L2 Optimal")
    app.upscale()


def test_gui_save_result_success(monkeypatch, tmp_path) -> None:
    app = UpscaleApp()
    monkeypatch.setattr(
        "tkinter.filedialog.asksaveasfilename",
        lambda *_a, **_k: str(tmp_path / "dummy.png"),
    )
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *_a, **_k: None)
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *_a, **_k: None)
    import numpy as np
    app.out_image = np.ones((8, 8), dtype=np.uint8)
    app.save_result()
