from click.testing import CliRunner
import numpy as np

from supreme_bassoon import benchmark


def test_benchmark_help() -> None:
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, ["--help"])
    assert result.exit_code == 0
    assert "Scaling factor" in result.output


def test_benchmark_runs(monkeypatch, tmp_path) -> None:
    from PIL import Image

    # Create a dummy image
    arr = np.random.default_rng().integers(0, 255, (16, 16), dtype="uint8")
    img_path = tmp_path / "dummy.png"
    Image.fromarray(arr).save(img_path)
    # Patch methods to return the input
    monkeypatch.setattr(benchmark, "nearest_neighbor", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "bilinear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "piecewise_linear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "l2_optimal_interpolation", lambda arr, _: arr)
    # Patch metrics to avoid actual computation
    monkeypatch.setattr(benchmark, "compute_psnr", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_ssim", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_mse", lambda *_: 1)
    # Patch resize to identity
    monkeypatch.setattr(benchmark, "resize", lambda arr, *a, **k: arr)
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, [str(img_path)])
    assert result.exit_code == 0
    assert "Nearest Neighbor" in result.output
    assert "Bilinear" in result.output
    assert "Piecewise Linear" in result.output
    assert "L2 Optimal" in result.output


def test_benchmark_metrics_called(monkeypatch, tmp_path) -> None:
    """Test that all metrics are called for each method during benchmarking."""
    from PIL import Image

    arr = np.random.default_rng().integers(0, 255, (16, 16), dtype="uint8")
    img_path = tmp_path / "dummy.png"
    Image.fromarray(arr).save(img_path)

    called = {"psnr": 0, "ssim": 0, "mse": 0}

    def fake_metric(*args: object, **kwargs: object) -> float:
        called["psnr"] += 1
        return 42.0

    def fake_ssim(*args: object, **kwargs: object) -> float:
        called["ssim"] += 1
        return 0.9

    def fake_mse(*args: object, **kwargs: object) -> float:
        called["mse"] += 1
        return 1.0

    monkeypatch.setattr(benchmark, "compute_psnr", fake_metric)
    monkeypatch.setattr(benchmark, "compute_ssim", fake_ssim)
    monkeypatch.setattr(benchmark, "compute_mse", fake_mse)
    monkeypatch.setattr(benchmark, "nearest_neighbor", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "bilinear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "piecewise_linear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "l2_optimal_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "resize", lambda arr, *a, **k: arr)
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, [str(img_path)])
    assert result.exit_code == 0
    # Each metric should be called once per method (4 methods)
    assert called["psnr"] == 4
    assert called["ssim"] == 4
    assert called["mse"] == 4


def test_benchmark_downscale(monkeypatch, tmp_path) -> None:
    """Test that downscaling is performed and shape is correct for upscaling."""
    from PIL import Image

    arr = np.random.default_rng().integers(0, 255, (32, 32), dtype="uint8")
    img_path = tmp_path / "dummy.png"
    Image.fromarray(arr).save(img_path)
    # Track the shape passed to each method
    shapes = []

    def fake_method(arr, _) -> None:
        shapes.append(arr.shape)
        return arr

    monkeypatch.setattr(benchmark, "nearest_neighbor", fake_method)
    monkeypatch.setattr(benchmark, "bilinear_interpolation", fake_method)
    monkeypatch.setattr(benchmark, "piecewise_linear_interpolation", fake_method)
    monkeypatch.setattr(benchmark, "l2_optimal_interpolation", fake_method)
    monkeypatch.setattr(benchmark, "compute_psnr", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_ssim", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_mse", lambda *_: 1)
    monkeypatch.setattr(
        benchmark, "resize", lambda arr, shape, *a, **k: arr[: shape[0], : shape[1]]
    )
    runner = CliRunner()
    result = runner.invoke(benchmark.benchmark, [str(img_path), "--scale", "2"])
    assert result.exit_code == 0
    # The input to each method should be the downscaled shape
    assert all(s[0] == 16 and s[1] == 16 for s in shapes)


def test_benchmark_missing_argument() -> None:
    from click.testing import CliRunner

    result = CliRunner().invoke(benchmark.benchmark, [])
    assert result.exit_code != 0


def test_benchmark_invalid_file(tmp_path) -> None:
    from click.testing import CliRunner

    # Create a dummy non-image file
    bad_file = tmp_path / "not_an_image.txt"
    bad_file.write_text("not an image")
    result = CliRunner().invoke(benchmark.benchmark, [str(bad_file)])
    # Accept either error output or exception (result.output may be empty if exception is raised)
    assert result.exit_code != 0
    if result.output:
        assert "error" in result.output.lower() or "cannot identify" in result.output.lower()
    else:
        assert result.exception is not None


def test_benchmark_invalid_scale(monkeypatch, tmp_path) -> None:
    from PIL import Image

    arr = np.random.default_rng().integers(0, 255, (8, 8), dtype="uint8")
    img_path = tmp_path / "dummy.png"
    Image.fromarray(arr).save(img_path)
    # Patch methods to avoid actual computation
    monkeypatch.setattr(benchmark, "nearest_neighbor", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "bilinear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "piecewise_linear_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "l2_optimal_interpolation", lambda arr, _: arr)
    monkeypatch.setattr(benchmark, "compute_psnr", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_ssim", lambda *_: 1)
    monkeypatch.setattr(benchmark, "compute_mse", lambda *_: 1)
    monkeypatch.setattr(benchmark, "resize", lambda arr, *_: arr)
    runner = CliRunner()
    # Use scale 0 (invalid)
    result = runner.invoke(benchmark.benchmark, [str(img_path), "--scale", "0"])
    assert result.exit_code != 0
    if result.output:
        assert (
            "scale" in result.output.lower()
            or "error" in result.output.lower()
            or "zero" in result.output.lower()
        )
    else:
        assert result.exception is not None
