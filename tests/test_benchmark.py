from click.testing import CliRunner

from supreme_bassoon import benchmark


def test_benchmark_help() -> None:
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, ["--help"])
    assert result.exit_code == 0
    assert "Scaling factor" in result.output


def test_benchmark_runs(monkeypatch, tmp_path) -> None:
    import numpy as np
    from click.testing import CliRunner
    from PIL import Image

    # Create a dummy image
    arr = (np.random.Generator(16, 16) * 255).astype("uint8")
    img_path = tmp_path / "dummy.png"
    Image.fromarray(arr).save(img_path)
    # Patch methods to return the input
    monkeypatch.setattr(benchmark, "nearest_neighbor")
    monkeypatch.setattr(benchmark, "bilinear_interpolation")
    monkeypatch.setattr(benchmark, "piecewise_linear_interpolation")
    monkeypatch.setattr(benchmark, "l2_optimal_interpolation")
    # Patch metrics to avoid actual computation
    monkeypatch.setattr(benchmark, "compute_psnr")
    monkeypatch.setattr(benchmark, "compute_ssim")
    monkeypatch.setattr(benchmark, "compute_mse")
    # Patch resize to identity
    monkeypatch.setattr(benchmark, "resize")
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, [str(img_path)])
    assert result.exit_code == 0
    assert "Nearest Neighbor" in result.output
    assert "Bilinear" in result.output
    assert "Piecewise Linear" in result.output
    assert "L2 Optimal" in result.output
