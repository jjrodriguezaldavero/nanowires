import numpy as np

from tools import plots as p
from tools import solver as s

import numpy as np
import pickle
import cv2
import os

class Surface():
    
    def __init__(self, name, config):
        self.name = name
        self.surface = np.array([])
        self.config = config

    def assemble_trenches(self, Cmask, Ctrench):
        """
        Assembles a layer of the surface with rectilinear trenches, having a value of Cmask for the mask and Ctrench for the trench.
        """

        [self.Lx, self.Ly, self.wx, self.wy, d, self.N] = self.config["surf_parameters"].values()
        self.trench_indices = []

        #Define value for the mask
        layer = np.full((self.Ly, self.Lx), Cmask)
        
        #Starting point for the trenches
        x0 = int(self.Lx/2 - (self.N/2)*(d+self.wx) + d/2) if self.N % 2 == 0 else int(self.Lx/2 - (self.N//2)*(d+self.wx) - self.wx/2)

        #Draw trenches on the mask
        for n in range(self.N):
            x1 = x0 + n * (d + self.wx)
            self.trench_indices.append(np.arange(x1, x1 + self.wx))
            layer[self.wy : self.Ly - self.wy, x1 : x1 + self.wx] = Ctrench

        #Checks if the first layer has been filled
        if self.surface.size == 0:
            self.surface = np.expand_dims(layer, axis=0)
        else:
            try:
                self.surface = np.concatenate([self.surface, np.expand_dims(layer, axis=0)], axis=0)
            except:
                print("Something went wrong when building the layer. Check previous layer dimensions.")

    def assemble_geometry(self, Cmask, Ctrench, path):
        """
        Assembles a layer of the surface with an arbitrary geometry given by path, having a value of Cmask for the mask and Ctrench for the trench.
        """

        #Import geometry from png file, with white pixels being mask and black pixels being trench
        geometry = cv2.imread(path, 0)
        geometry = 1 - geometry/255
        self.Lx = geometry.shape[1]
        self.Ly = geometry.shape[0]

        #Define value for the mask
        layer = np.full((self.Ly, self.Lx), Cmask) 
        
        #Draw trenches on the mask
        layer = np.add(layer, (Ctrench - Cmask) * geometry, casting="unsafe")

        #Check if the first layer has been filled
        if self.surface.size == 0:
            self.surface = np.expand_dims(layer, axis=0)
        else:
            try:
                self.surface = np.concatenate([self.surface, np.expand_dims(layer, axis=0)], axis=0)
            except:
                print("Something went wrong when building the layer. Check previous layer dimensions.")

    def save(self, path): 
        """
        Saves the object in pickle format.
        """
        my_path = path + self.name + '.pickle'
        with open(os.path.abspath(my_path), 'wb') as f:
        #The FEniCS solution can't be saved, only the sampled array, so it is destroyed before saving
            self.__dict__.pop('solution_dolfin')
            pickle.dump(self.__dict__, f, 2)
            
    def load(self, path):
        """
        Loads the object in pickle format. 
        """
        my_path = path + self.name + '.pickle'
        with open(os.path.abspath(my_path), 'rb') as f:
            tmp_dict = pickle.load(f)

        #Update the whole object contents
        self.__dict__.update(tmp_dict)

class Diffusion(Surface):

    def solve(self, mesh_size_x, mesh_size_y):
        """
        Solves the diffusion PDE starting from the surface with layers given by:
            1. Characteristic times t
            2. Characteristic lengths L
            3. Incoming particle flux G

        Returns both the FEniCS solution and a sampled solution in a numpy array.
        """
        T_layer = self.surface[0,:,:]
        L_layer = self.surface[1,:,:]
        G_layer = self.surface[2,:,:]
        
        self.solution_dolfin = s.build_fem_PP(T_layer, L_layer, G_layer, mesh_size_x, mesh_size_y)
        self.solution = np.array([[self.solution_dolfin(i, j) for i in np.linspace(0, self.Lx-1, self.Lx)] for j in np.linspace(0, self.Ly-1, self.Ly)])
    
        return self.solution_dolfin, self.solution

    def compute_trench_profile(self):
        """
        Computes the trench midpoint heights and areas for the inner and outermost trenches.
        """
        try:
            self.trench_indices != []
        except:
            print("A rectilinear trench layer could not be found. Please use rectilinear geometry.")
        else:
            avg = np.mean(self.solution, axis=0)
            trench_values = [avg[self.trench_indices[i]] for i in range(self.N)]
            self.trench_midpoint_heights = [trench_values[i][int(self.wx/2)] for i in range(self.N)]
            self.trench_areas = [trench_values[i].sum() for i in range(self.N)]
            trench_height_profile = [self.trench_midpoint_heights[0], self.trench_midpoint_heights[int(self.N/2)]]
            trench_area_profile = [self.trench_areas[0], self.trench_areas[int(self.N/2)]]

            return trench_height_profile, trench_area_profile

    def plot_surface(self, title=""):
        """
        Plots the solution of the FEniCS solver. 
        """
        p.plot_fenics(self.solution_dolfin, title)  

    def plot_avg(self, direction, title="" , hold=False):
        """
        Plots the average of the sampled solution for some direction (0 = x, 1 = y)
        """
        p.plot_avg(self.solution, direction, title, hold)  
        
    def plot_avg_growth_rate(self, direction, title="", hold=False):
        """
        Plots the growth rate for some direction (0 = x, 1 = y)
        """
        try: 
            F_layer = self.surface[3,:,:]
        except:
            print("A fourth layer containing the consumption characteristic times is necessary to plot growth rates.")
        else:
            p.plot_avg(np.multiply(F_layer, self.solution), direction, title, hold)
    