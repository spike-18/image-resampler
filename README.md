# image-resampler

**image-resampler** is a modern Python toolkit for image interpolation and upscaling. It features a command-line interface, benchmarking tools, and a graphical user interface (GUI). Built with NumPy, Pillow, Matplotlib, and Click, it is designed for both ease of use and extensibility.

![Example input image](examples/cat_1.jpg)

## Features

- **Multiple interpolation methods:**
  - Nearest Neighbor (nn)
  - Bilinear (bl)
  - Piecewise Linear (pw)
  - L2 Optimal (l2, Fourier-based)
- **Side-by-side visualization** of original and upscaled images
- **Command-line interface (CLI)** and **GUI**
- **Benchmarking** with metrics: PSNR, SSIM, MSE
- **Easy extensibility** and modern Python packaging

## Overview

image-resampler provides several interpolation methods for upscaling images:

- **Nearest Neighbor (nn):** Assigns each new pixel the value of the closest original pixel.
- **Bilinear (bl):** Uses a weighted average of the four nearest pixels.
- **Piecewise Linear (pw):** Interpolates first along rows, then columns.
- **L2 Optimal (l2):** Uses Fourier zero-padding for optimal upscaling (integer scale only).

## Installation

Clone the repository and install dependencies with Poetry:

```bash
git clone https://github.com/spike-18/image-resampler.git
cd image-resampler
poetry install
```

## Quickstart

**Upscale an image from the command line:**

```bash
poetry run image-resampler upscale path/to/image.png -m bl -s 3 --save
```

**Run the GUI:**

```bash
poetry run image-resampler gui
```

**Benchmark all methods:**

```bash
poetry run image-resampler benchmark path/to/image.png -s 2
```

**Example comparison of methods:**

```bash
poetry run image-resampler example
```

## Command-Line Options

- `file`: The input image file.
- `-m, --method`: Interpolation method (`nn`, `bl`, `pw`, `l2`).
- `-s, --scale`: Scaling factor (default: 2).
- `-v, --verbose`: Print detailed information.
- `--save`: Save the upscaled image to the `output/` directory.

## Project Structure

- `src/image_resampler/`: Core package (CLI, GUI, methods, metrics, visualization)
- `tests/`: Unit tests
- `docs/`: Documentation (Sphinx)
- `examples/`: Example images
- `plots/`: Output plots

## API Reference

See the [references](docs/references.rst) page in the documentation for full API details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss your ideas.

- Follow PEP8 and project coding standards
- Add or update docstrings for all public functions and classes
- Ensure all tests pass with `pytest` and code is formatted with `ruff`

See [CONTRIBUTING](docs/contributing.rst) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of NumPy, Pillow, Matplotlib, and Click
- Inspired by various image processing and interpolation techniques in the Python ecosystem
- Thanks to ChatGPT and DeepSeek
