import numpy as np
import click
import matplotlib.pyplot as plt
from skimage import data

from . import __version__
from .methods import nearest_neighbor, bilinear_interpolation, piecewise_linear_interpolation, l2_optimal_interpolation


@click.command()
@click.version_option(version=__version__)
def main():
    
    image = data.camera()  # shape: (512, 512)
    
    scale = 2 
    
    nn_image = nearest_neighbor(image, scale)
    bilinear_image = bilinear_interpolation(image, scale)
    piecewise_image = piecewise_linear_interpolation(image, scale)
    
    l2_image = l2_optimal_interpolation(image, scale)
    
    fig, axes = plt.subplots(1, 5, figsize=(20, 5))
    
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(nn_image, cmap='gray')
    axes[1].set_title("Nearest Neighbor")
    axes[1].axis('off')
    
    axes[2].imshow(bilinear_image, cmap='gray')
    axes[2].set_title("Bilinear")
    axes[2].axis('off')
    
    axes[3].imshow(piecewise_image, cmap='gray')
    axes[3].set_title("Piecewise Linear")
    axes[3].axis('off')
    
    axes[4].imshow(l2_image, cmap='gray')
    axes[4].set_title("L2 Optimal (FFT)")
    axes[4].axis('off')
    
    plt.tight_layout()
    plt.show()

# if __name__ == '__main__':
#     main()
