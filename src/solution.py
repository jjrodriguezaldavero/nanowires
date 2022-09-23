import json
from models.Diffusion import Diffusion

def solution(path_geometry, geometry=False):
    """
    Plots the solution to the diffusion equation in 2D for the parameters specified in the config dictionary.
    If geometry==True, the geometry specified in path_geometry is used for the simulation.
    It must be a png file consisting on white and black pixels, where the white pixels will be represent the mask and the black ones the trenches.
    """
    config = {

        "mesh_sizes": {
            "mesh_size_x": 50,
            "mesh_size_y": 50
        },

        "surf_parameters": {
            "Lx": 300,
            "Ly": 100,
            "wx": 10,
            "wy": 0,
            "d": 10,
            "n_trenches": 5
        },

        "mask_parameters": {
            "T_mask": 10,
            "L_mask": 40,
            "G_mask": 10,
            "F_mask": 0
        },

        "trench_parameters": {
            "T_trench": 50,
            "L_trench": 40,
            "G_trench": 50,
            "F_trench": 1
        },

        "order_parameter_type": "hr"
    }

    [T_mask, L_mask, G_mask, F_mask] = config["mask_parameters"].values()
    [T_trench, L_trench, G_trench, F_trench] = config["trench_parameters"].values()
    [mesh_size_x, mesh_size_y] = config["mesh_sizes"].values()

    #BUILD SURFACE
    if geometry == False:
        solution = Diffusion('test', config)
        solution.assemble_trenches(T_mask, T_trench)
        solution.assemble_trenches(L_mask, L_trench)
        solution.assemble_trenches(G_mask, G_trench)
        solution.assemble_trenches(F_mask, F_trench)
        solution.solve(mesh_size_x, mesh_size_y)

    elif geometry == True:
        solution = Diffusion('test', config)
        solution.assemble_geometry(T_mask, T_trench, path_geometry)
        solution.assemble_geometry(L_mask, L_trench, path_geometry)
        solution.assemble_geometry(G_mask, G_trench, path_geometry)
        solution.assemble_geometry(F_mask, F_trench, path_geometry)
        solution.solve(mesh_size_x, mesh_size_y)

    #PLOT RESULTS
    solution.plot_surface(title="Surface plot")
    solution.plot_avg(direction=0, title="Avg mobile species with respect to x axis")
    solution.plot_avg_growth_rate(direction=0, title="Avg mobile species with respect to x axis")

path_geometry = "tools/geometries/testgeom1.png"

solution(path_geometry, geometry=True)