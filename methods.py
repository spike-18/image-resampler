import numpy as np


def node_wise_interpolation(donor_mesh, target_x, method='linear'):
    target_values = np.zeros_like(target_x)
    num_donors = donor_mesh.shape[1]
    num_targets = len(target_x)


    # for j in range(num_donors-1):
        
    #     local_interpol_f = None
    #     if method == 'linear':    
    #         k = (donor_mesh[1][j+1]-donor_mesh[1][j]) / (donor_mesh[0][j+1]-donor_mesh[0][j])
    #         b = donor_mesh[1][j] - k*donor_mesh[0][j]
    #         local_interpol_f = lambda x: k*x + b

    #     for i in range(num_targets):
    #         if donor_mesh[0][j] <= target_x[i] and target_x[i] < donor_mesh[0][j+1]:
    #             target_values[i] = local_interpol_f(target_x[i])

    #     if donor_mesh[0][num_donors-1] <= target_x[i]:
    #         target_values[i] = donor_mesh[1][num_donors-1]


    if method == 'quadratic':

        for j in range(num_donors-2):
            
            local_interpol_f = None
            a = ((donor_mesh[1][j]-donor_mesh[1][j+1])/(donor_mesh[0][j]-donor_mesh[0][j+1]) - 
                (donor_mesh[1][j]-donor_mesh[1][j+2])/(donor_mesh[0][j]-donor_mesh[0][j+2]) ) / (donor_mesh[0][j+1]-donor_mesh[0][j+2])
            b = (donor_mesh[1][j]-donor_mesh[1][j+1])/(donor_mesh[0][j]-donor_mesh[0][j+1]) - a*((donor_mesh[0][j]+donor_mesh[0][j+1]))
            c = donor_mesh[1][j] - a*donor_mesh[0][j]**2 - b*donor_mesh[0][j]
            print(a,b,c)
            local_interpol_f = lambda x: a*x**2+b*x+c
        
            for i in range(num_targets):
                if donor_mesh[0][j] <= target_x[i] and target_x[i] < donor_mesh[0][j+1]:
                    target_values[i] = local_interpol_f(target_x[i])

            if j == num_donors - 3:
                for i in range(num_targets):
                        if donor_mesh[0][num_donors-2] <= target_x[i]:
                            target_values[i] = local_interpol_f(target_x[i])

    return np.array([target_x, target_values])

def galerkin_interpolation():
    pass
