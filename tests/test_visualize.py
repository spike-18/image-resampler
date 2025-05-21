from supreme_bassoon.visualize import example


def test_example_runs(monkeypatch) -> None:
    # Patch plt.show to avoid opening a window
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda: None)
    # Should not raise
    example()


# def test_example_output(monkeypatch, capsys):
#     import matplotlib.pyplot as plt
#     monkeypatch.setattr(plt, "show", lambda: None)
#     example()
#     captured = capsys.readouterr()
#     assert "Example comparison between interpolation methods is loaded." in captured.out
