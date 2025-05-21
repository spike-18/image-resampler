from click.testing import CliRunner

from supreme_bassoon import cli


def test_cli_group_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--help"])
    assert result.exit_code == 0
    for cmd in ["upscale", "example", "benchmark", "gui"]:
        assert cmd in result.output


def test_cli_upscale_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["upscale", "--help"])
    assert result.exit_code == 0
    assert "method" in result.output
    assert "scaling factor" in result.output


# def test_cli_example(monkeypatch):
#     runner = CliRunner()
#     import matplotlib.pyplot as plt
#     monkeypatch.setattr(plt, "show", lambda: None)
#     result = runner.invoke(cli.cli, ["example"])
#     assert result.exit_code == 0


def test_cli_benchmark_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["benchmark", "--help"])
    assert result.exit_code == 0
    assert "Scaling factor" in result.output


# def test_cli_gui(monkeypatch):
#     runner = CliRunner()
#     from supreme_bassoon import gui as gui_module
#     class DummyApp:
#         def mainloop(self):
#             pass
#     monkeypatch.setattr(gui_module, "UpscaleApp", DummyApp)
#     result = runner.invoke(cli.cli, ["gui"])
#     assert result.exit_code == 0
