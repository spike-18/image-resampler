import numpy as np


def node_wise_interpolation(donor_mesh, target_x, method="linear"):
    target_values = np.zeros_like(target_x)
    num_donors = donor_mesh.shape[1]
    num_targets = len(target_x)

    for j in range(num_donors - 1):
        local_interpol_f = None
        if method == "linear":
            k = (donor_mesh[1][j + 1] - donor_mesh[1][j]) / (
                donor_mesh[0][j + 1] - donor_mesh[0][j]
            )
            b = donor_mesh[1][j] - k * donor_mesh[0][j]

            def local_interpol_f(x):
                return k * x + b

        for i in range(num_targets):
            if donor_mesh[0][j] <= target_x[i] and target_x[i] < donor_mesh[0][j + 1]:
                target_values[i] = local_interpol_f(target_x[i])

        if donor_mesh[0][num_donors - 1] <= target_x[i]:
            target_values[i] = donor_mesh[1][num_donors - 1]

    return np.array([target_x, target_values])


def galerkin_interpolation():
    pass
