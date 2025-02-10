import numpy as np


def node_wise_interpolation(donor_mesh, func_basis, target_x):
    target_values = np.zeros_like(target_x)

    num_donors = donor_mesh.shape[1]
    num_targets = len(target_x)

    for i in range(num_targets):
        for j in range(num_donors-1):
            if donor_mesh[0][j] <= target_x[i] and target_x[i] < donor_mesh[0][j+1]:
                target_values[i] = func_basis[j](target_x[i])

        if donor_mesh[0][num_donors-1] <= target_x[i]:
            target_values[i] = func_basis[num_donors-1](target_x[i])


    return np.array([target_x, target_values])

def galerkin_interpolation():
    pass
