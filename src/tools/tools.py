import numpy as np

from models.Diffusion import Diffusion

def run_simulation(path, config):
    """
    Runs and saves the Diffusion object for all the possible combinations of the values in the simulation parameters.
    """
    [T_mask, L_mask, G_mask] = config["mask_parameters"].values()
    [d_list, T_list, L_list, G_list] = config["simulation_parameters"].values()
    [mesh_size_x, mesh_size_y] = config["mesh_sizes"].values()
    

    for d in d_list:
        for T in T_list:
            for L in L_list:
                for G in G_list:

                    name = "d{}_T{}_L{}_G{}".format(d, T, L, G)
                    config["surf_parameters"]["d"] = d #sloppy fix due to design error

                    test = Diffusion(name, config)
                    test.assemble_trenches(T_mask, T)
                    test.assemble_trenches(L, L)
                    test.assemble_trenches(G_mask, G)

                    try:
                        #Saves time by skipping already existing data
                        print("Trying to load {}".format(name))
                        test.load(path+'data/')
                    except:
                        test.solve(mesh_size_x, mesh_size_y)
                        test.save(path=path+'data/')

def load_simulation(path, config):
    """
    Loads all the objects in the data folder and computes an array with the order parameters.
    """
    [d_list, T_list, L_list, G_list] = config["simulation_parameters"].values()
    order_parameter_type = config["order_parameter_type"]

    order_parameter = np.zeros([len(d_list), len(T_list), len(L_list), len(G_list)]) 
       
    for i in range(len(d_list)):
        for j in range(len(T_list)):
            print("d: {}, T: {}".format(d_list[i],T_list[j]))
            for k in range(len(L_list)):
                for l in range(len(G_list)):

                    name = "d{}_T{}_L{}_G{}".format(d_list[i], T_list[j], L_list[k], G_list[l])
                    solution = Diffusion(name, config)
                    try:
                        solution.load(path=path+'data/')
                    except:
                        continue
                    trench_height_profile, trench_area_profile = solution.compute_trench_profile()

                    if order_parameter_type == 'ha':
                        order_parameter[i,j,k,l] = trench_height_profile[1] - trench_height_profile[0]
                    elif order_parameter_type == 'hr':
                        order_parameter[i,j,k,l] = 100 * (trench_height_profile[1] - trench_height_profile[0]) / (trench_height_profile[1] + trench_height_profile[0])
                    if order_parameter_type == 'aa':
                        order_parameter[i,j,k,l] = trench_area_profile[1] - trench_area_profile[0]
                    elif order_parameter_type == 'ar':
                        order_parameter[i,j,k,l] = 100 * (trench_area_profile[1] - trench_area_profile[0]) / (trench_area_profile[1] + trench_area_profile[0])
                    
    return order_parameter

def run_simulation_ratios(path, config, X):
    [T_mask, L_mask, G_mask] = config["mask_parameters"].values()
    [T_trench, L_trench, G_trench] = config["trench_parameters"].values()
    [mesh_size_x, mesh_size_y] = config["mesh_sizes"].values()

    ratios_values = config["ratios_values"]
    
    order_parameter_type = config["order_parameter_type"]

    order_parameter = np.zeros([len(ratios_values), len(ratios_values)])

    for i in range(len(ratios_values)):
        for j in range(len(ratios_values)):
                name="{}{}_{}{}".format(X, ratios_values[i], X, ratios_values[j])
                solution = Diffusion(name, config)
                if X == "T":
                    solution.assemble_trenches(ratios_values[i], ratios_values[j])
                    solution.assemble_trenches(L_mask, L_trench)
                    solution.assemble_trenches(G_mask, G_trench)
                elif X == "L":
                    solution.assemble_trenches(T_mask, T_trench)
                    solution.assemble_trenches(ratios_values[i], ratios_values[j])
                    solution.assemble_trenches(G_mask, G_trench)
                elif X == "G":
                    solution.assemble_trenches(T_mask, T_trench)
                    solution.assemble_trenches(L_mask, L_trench)
                    solution.assemble_trenches(ratios_values[i], ratios_values[j])

                try:
                        #Saves time by skipping already existing data
                    print("Trying to load {}".format(name))
                    solution.load(path +'data/')
                except:
                    solution.solve(mesh_size_x, mesh_size_y)
                    solution.save(path=path+'data/')

                trench_height_profile, trench_area_profile = solution.compute_trench_profile()

                if order_parameter_type == 'ha':
                    order_parameter[i,j] = trench_height_profile[1] - trench_height_profile[0]
                elif order_parameter_type == 'hr':
                    order_parameter[i,j] = 100 * (trench_height_profile[1] - trench_height_profile[0]) / (trench_height_profile[1] + trench_height_profile[0])
                if order_parameter_type == 'aa':
                    order_parameter[i,j] = trench_area_profile[1] - trench_area_profile[0]
                elif order_parameter_type == 'ar':
                    order_parameter[i,j] = 100 * (trench_area_profile[1] - trench_area_profile[0]) / (trench_area_profile[1] + trench_area_profile[0])

    return order_parameter

                