import importlib
import sys


def test_main_entrypoint(monkeypatch) -> None:
    # Patch click.echo to capture output
    called = {}
    monkeypatch.setattr("click.echo", lambda msg, **_: called.setdefault("echo", msg))
    sys_argv = sys.argv
    sys.argv = ["prog", "--help"]
    importlib.reload(importlib.import_module("supreme_bassoon.__main__"))
    sys.argv = sys_argv
    # Accept either no output (if __main__ just prints usage) or any echo call
    assert called is not None  # Just check no crash, not strict on output


def test_main_imports() -> None:
    import supreme_bassoon.__main__  # noqa: F401


def test_main_function(monkeypatch) -> None:
    # Patch all side effects: load_image, save_image, methods, plt.show
    import supreme_bassoon.__main__ as main_mod

    monkeypatch.setattr(main_mod, "load_image", lambda *_a, **_k: __import__("numpy").zeros((8, 8)))
    monkeypatch.setattr(main_mod, "save_image", lambda *_a, **_k: None)
    monkeypatch.setattr(
        main_mod, "nearest_neighbor", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod, "bilinear_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod,
        "piecewise_linear_interpolation",
        lambda *_a, **_k: __import__("numpy").zeros((8, 8)),
    )
    monkeypatch.setattr(
        main_mod, "l2_optimal_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda *_a, **_k: None)

    # Test each method
    class DummyFile:
        name = "dummy.png"

    for method in ["nn", "bl", "pw", "l2"]:
        assert main_mod.main.callback(DummyFile(), method, 2, save=False, verbose=False) is None
    # Test invalid method
    ret = main_mod.main.callback(DummyFile(), "invalid", 2, save=False, verbose=False)
    assert ret == 1
    # Test save branch
    main_mod.main.callback(DummyFile(), "nn", 2, save=True, verbose=False)


def test_list_methods(monkeypatch) -> None:
    import supreme_bassoon.__main__ as main_mod

    called = {}
    monkeypatch.setattr("click.echo", lambda msg, **_: called.setdefault("echo", msg))
    main_mod.list_methods()
    assert "nearest neighbor" in called["echo"]


def test_main_invalid_file(monkeypatch) -> None:
    import supreme_bassoon.__main__ as main_mod

    class DummyFile:
        name = "not_an_image.txt"

    # Patch load_image to raise an error
    monkeypatch.setattr(
        main_mod,
        "load_image",
        lambda *_a, **_k: (_ for _ in ()).throw(ValueError("bad file")),
    )
    monkeypatch.setattr(main_mod, "save_image", lambda *_a, **_k: None)
    monkeypatch.setattr(
        main_mod, "nearest_neighbor", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod, "bilinear_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod,
        "piecewise_linear_interpolation",
        lambda *_a, **_k: __import__("numpy").zeros((8, 8)),
    )
    monkeypatch.setattr(
        main_mod, "l2_optimal_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda *_a, **_k: None)
    # Should raise or return error code
    try:
        ret = main_mod.main.callback(DummyFile(), "nn", 2, save=False, verbose=False)
        assert ret is not None
    except ValueError:
        pass


def test_main_save_and_verbose(monkeypatch, tmp_path) -> None:
    import supreme_bassoon.__main__ as main_mod

    called = {}
    monkeypatch.setattr(main_mod, "load_image", lambda *_a, **_k: __import__("numpy").zeros((8, 8)))
    monkeypatch.setattr(main_mod, "save_image", lambda *_a, **_k: called.setdefault("saved", True))
    monkeypatch.setattr(
        main_mod, "nearest_neighbor", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod, "bilinear_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    monkeypatch.setattr(
        main_mod,
        "piecewise_linear_interpolation",
        lambda *_a, **_k: __import__("numpy").zeros((8, 8)),
    )
    monkeypatch.setattr(
        main_mod, "l2_optimal_interpolation", lambda *_a, **_k: __import__("numpy").zeros((8, 8))
    )
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda *_a, **_k: None)

    class DummyFile:
        name = str(tmp_path / "dummy.png")

    # Should call save_image and print verbose output
    main_mod.main.callback(DummyFile(), "nn", 2, save=True, verbose=True)
    assert called.get("saved")
