import numpy as np

from supreme_bassoon.methods import (
    bilinear_interpolation,
    l2_optimal_interpolation,
    nearest_neighbor,
    piecewise_linear_interpolation,
)

# def test_nearest_neighbor_identity():
#     arr = np.arange(9).reshape(3, 3)
#     out = nearest_neighbor(arr, 1)
#     assert np.allclose(arr, out)

# def test_bilinear_identity():
#     arr = np.arange(9).reshape(3, 3)
#     out = bilinear_interpolation(arr, 1)
#     assert np.allclose(arr, out)

# def test_piecewise_linear_identity():
#     arr = np.arange(9).reshape(3, 3)
#     out = piecewise_linear_interpolation(arr, 1)
#     assert np.allclose(arr, out)

# def test_l2_optimal_identity():
#     arr = np.arange(9).reshape(3, 3)
#     out = l2_optimal_interpolation(arr, 1)
#     assert np.allclose(arr, out)


def test_upscale_shapes() -> None:
    arr = np.arange(9).reshape(3, 3)
    for func in [
        nearest_neighbor,
        bilinear_interpolation,
        piecewise_linear_interpolation,
        l2_optimal_interpolation,
    ]:
        out = func(arr, 2)
        assert out.shape == (6, 6)
