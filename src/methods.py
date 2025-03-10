import numpy as np


def node_wise_interpolation(donor_mesh, donor_values, target_mesh):
    donor_shape = (donor_mesh.shape[0], donor_mesh.shape[1])
    target_shape = (target_mesh.shape[0], target_mesh.shape[1])

    target_values = np.zeros(target_shape, dtype=np.float32)

    def local_interpol_f(x, y, a, b, c):
        return a * x + b * y + c

    for i in range(donor_shape[0]):
        for j in range(donor_shape[1]):
            if i != donor_shape[0] - 1 and j != donor_shape[1] - 1:
                a = (donor_values[i + 1][j] - donor_values[i][j]) / (
                    donor_mesh[i + 1][j][0] - donor_mesh[i][j][0]
                )

                b = (donor_values[i][j + 1] - donor_values[i][j]) / (
                    donor_mesh[i][j + 1][1] - donor_mesh[i][j][1]
                )

                c = (
                    donor_values[i][j]
                    - a * donor_mesh[i][j][0]
                    - b * donor_mesh[i][j][1]
                )

                for k in range(target_shape[0]):
                    for m in range(target_shape[1]):
                        if (
                            donor_mesh[i][j][0] <= target_mesh[k][m][0]
                            and target_mesh[k][m][0] < donor_mesh[i + 1][j][0]
                        ):
                            if (
                                donor_mesh[i][j][1] <= target_mesh[k][m][1]
                                and target_mesh[k][m][1] < donor_mesh[i][j + 1][1]
                            ):
                                target_values[k][m] = local_interpol_f(
                                    donor_mesh[i][j][0], donor_mesh[i][j][1], a, b, c
                                )

            elif i != donor_shape[0] - 1:
                for k in range(target_shape[0]):
                    for m in range(target_shape[1]):
                        if (
                            donor_mesh[i][j][0] <= target_mesh[k][m][0]
                            and target_mesh[k][m][0] < donor_mesh[i + 1][j][0]
                        ):
                            if donor_mesh[i][j][1] <= target_mesh[k][m][1]:
                                target_values[k][m] = donor_values[i][j]

            elif j != donor_shape[1] - 1:
                for k in range(target_shape[0]):
                    for m in range(target_shape[1]):
                        if donor_mesh[i][j][0] <= target_mesh[k][m][0]:
                            if (
                                donor_mesh[i][j][1] <= target_mesh[k][m][1]
                                and target_mesh[k][m][1] < donor_mesh[i][j + 1][1]
                            ):
                                target_values[k][m] = donor_values[i][j]

            else:
                target_values[k][m] = donor_values[donor_shape[0] - 1][
                    donor_shape[1] - 1
                ]

    return target_values


def galerkin_interpolation():
    pass
