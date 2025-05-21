from supreme_bassoon.gui import UpscaleApp


def test_gui_instantiates(monkeypatch) -> None:
    # Patch Tkinter mainloop to avoid opening a window
    monkeypatch.setattr(UpscaleApp, "mainloop")
    app = UpscaleApp()
    assert hasattr(app, "create_widgets")
    assert hasattr(app, "open_image")
    assert hasattr(app, "upscale")
    assert hasattr(app, "save_result")
    assert hasattr(app, "display_image")


def test_gui_methods(monkeypatch) -> None:
    # Patch methods to avoid side effects
    app = UpscaleApp()
    monkeypatch.setattr(app, "display_image")
    app.image = None
    app.out_image = None
    # open_image should not fail if no file is selected
    monkeypatch.setattr("tkinter.filedialog.askopenfilename", lambda: "")
    app.open_image()
    # save_result should not fail if out_image is None
    app.save_result()
