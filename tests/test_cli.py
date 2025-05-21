"""Test cases for the CLI module of supreme_bassoon."""

import pytest
from click.testing import CliRunner

from supreme_bassoon.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_cli_help(runner) -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Supreme Bassoon" in result.output
    assert "upscale" in result.output
    assert "example" in result.output
    assert "benchmark" in result.output
    assert "gui" in result.output


# def test_cli_example_runs(runner):
#     result = runner.invoke(cli, ["example"])
#     # Should exit cleanly, even if it opens a plot window
#     assert result.exit_code == 0


def test_cli_benchmark_requires_argument(runner) -> None:
    result = runner.invoke(cli, ["benchmark"])
    assert result.exit_code != 0
    assert "Usage" in result.output


def test_cli_upscale_requires_argument(runner) -> None:
    result = runner.invoke(cli, ["upscale"])
    assert result.exit_code != 0
    assert "Usage" in result.output


# def test_cli_gui_runs(monkeypatch, runner):
#     # Patch UpscaleApp to avoid opening a real window
#     from supreme_bassoon import gui as gui_module

#     class DummyApp:
#         def mainloop(self):
#             pass

#     monkeypatch.setattr(gui_module, "UpscaleApp", DummyApp)
#     result = runner.invoke(cli, ["gui"])
#     assert result.exit_code == 0
