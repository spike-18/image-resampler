Supreme Bassoon Documentation
=============================

A Python toolkit for image interpolation and upscaling, featuring a command-line interface, benchmarking, and a modern GUI. Built with NumPy, Pillow, Matplotlib, and Click.

.. image:: ../examples/cat_1.jpg
   :width: 300
   :alt: Example input image

Overview
--------
Supreme Bassoon provides several interpolation methods for upscaling images, including:

- **Nearest Neighbor (nn):** Assigns each new pixel the value of the closest original pixel.
- **Bilinear (bl):** Uses a weighted average of the four nearest pixels.
- **Piecewise Linear (pw):** Interpolates first along rows, then columns.
- **L2 Optimal (l2):** Uses Fourier zero-padding for optimal upscaling (integer scale only).

Features
--------
- Multiple interpolation methods
- Side-by-side visualization of original and upscaled images
- Command-line interface (CLI) and GUI
- Benchmarking and metrics (PSNR, SSIM, MSE)
- Easy extensibility and modern Python packaging

Quickstart
----------
Install dependencies with Poetry:

.. code-block:: bash

   poetry install

Upscale an image from the command line:

.. code-block:: bash

   poetry run supreme-bassoon upscale path/to/image.png -m bl -s 3 --save

Run the GUI:

.. code-block:: bash

   poetry run supreme-bassoon gui

Benchmark all methods:

.. code-block:: bash

   poetry run supreme-bassoon benchmark path/to/image.png -s 2

Example comparison of methods:

.. code-block:: bash

   poetry run supreme-bassoon example

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   references
   license
   contributing

API Reference
-------------
See :doc:`references` for full API documentation generated from the source code.

Contributing
------------
Contributions are welcome! Please see the :doc:`contributing` page, README, or open issues or pull requests on GitHub.

- Source code: https://github.com/canne16/supreme-bassoon
- Author: Kirill Madorskii