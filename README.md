# Supreme Bassoon

**Supreme Bassoon** is a Python command-line tool for image interpolation and scaling. The project implements several interpolation methods to upscale images and visualize the results. It’s built using popular libraries such as NumPy, Pillow, Matplotlib, and Click.

## Overview

This tool provides an easy way to experiment with different image interpolation techniques. It supports the following methods:

- **Nearest Neighbor (nn):** A simple method that assigns each new pixel the value of the closest original pixel.
- **Bilinear (bl):** A method that uses a weighted average of the four nearest pixels.
- **Piecewise Linear (pw):** Interpolates first along the rows and then along the columns using linear interpolation.
- **L2 Optimal (l2):** Uses Fourier zero-padding to upscale images optimally in an L2 sense (requires an integer scaling factor).

The tool accepts an image file as input, performs the chosen interpolation, and displays both the original and upscaled images side by side. Optionally, you can also save the upscaled image.

## Features

- **Multiple interpolation methods:** Easily switch between different upscaling techniques.
- **Visualization:** View a side-by-side comparison of the original and interpolated images.
- **Command-line interface:** Simple and flexible CLI powered by Click.
- **Python packaging:** Managed using Poetry for dependency handling and packaging.

## Requirements

- Python 3.10+
- [NumPy](https://numpy.org/)
- [Pillow](https://python-pillow.org/)
- [Matplotlib](https://matplotlib.org/)
- [Click](https://click.palletsprojects.com/)

## Installation

Clone the repository:

```bash
git clone https://github.com/canne16/supreme-bassoon.git
cd supreme-bassoon
```

Install the dependencies using [Poetry](https://python-poetry.org/):

```bash
poetry install
```

### Command Options

- `file`: The input image file.
- `-m, --method`: Interpolation method to use. Options are:
  - `nn` – Nearest Neighbor (default)
  - `bl` – Bilinear
  - `pw` – Piecewise Linear
  - `l2` – L2 Optimal (requires an integer scale factor)
- `-s, --scale`: Scaling factor (default is 2).
- `-v, --verbose`: Print detailed information about the interpolation process.
- `--save`: Save the upscaled image to the `output/` directory.

## Example Usage

Here are some concrete examples to help you get started:

0. **Example comparison of methods**  
   Upscale an example image by a factor of 2 using several methods, print them alongside:

   ```bash
   poetry run example
   ```

1. **Nearest Neighbor Interpolation**  
   Upscale an image by a factor of 3 using the bilinear interpolation method, print the parameters, and save the output:

   ```bash
   poetry run interpolate example.jpg --method nn --scale 3 --verbose --save
   ```

2. **Piecewise Linear Interpolation**  
   Use piecewise linear interpolation to upscale an image by a factor of 2:

   ```bash
   poetry run python interpolate example.jpg --method pw --scale 2
   ```

## Interpolation Methods

The core functionality is implemented in the `methods.py` module:
- **nearest_neighbor:** Uses a basic copy mechanism from the source image.
- **bilinear_interpolation:** Computes a weighted average of surrounding pixels.
- **piecewise_linear_interpolation:** Performs sequential linear interpolation first vertically then horizontally.
- **l2_optimal_interpolation:** Applies Fourier-based zero-padding for optimal scaling.

See the source code in [`src/supreme_bassoon/__main__.py`](https://github.com/canne16/supreme-bassoon/blob/main/src/supreme_bassoon/__main__.py) and [`src/supreme_bassoon/methods.py`](https://github.com/canne16/supreme-bassoon/blob/main/src/supreme_bassoon/methods.py) for more details.

## Contributing

Contributions are welcome! If you’d like to improve the code or add new features, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is not licensed.

## Acknowledgments

- Thanks to the developers of NumPy, Pillow, Matplotlib, and Click for making high-quality tools available to the community.
- Inspired by various image processing and interpolation techniques in the Python ecosystem.
- Thanks to ChatGPT and DeepSeek
