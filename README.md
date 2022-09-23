# FENICS diffusion solver

**Juan José Rodríguez Aldavero**

Project to solve the modified diffusion equation representing the growth of semiconducting nanowires using the FENICS library for the internship in the Quantum Materials group led by Prof. Erik Bakkers, Department of Applied Physics at the University of Eindhoven.

This project solves the difussion equation with custom sources and sinks numerically, and argues that the equation models the growth of semiconducting nanowires. These nanowires form the basis of many groundbreaking quantum technologies such as topological quantum computers, and therefore insight into their growth regimes is of value.

**Installation**

Requires the installation of the FENICS/DOLFIN library, as well as numpy and json. The easiest way is by means of an Anaconda environment.

```bash
conda create -n fenicsproject -c conda-forge fenics
source activate fenicsproject
```

The 'solution.py' file is available to compute a single solution of the equation, while to compute several solutions and for example plot the regime diagram depending on, for example, the nanowire height difference, use the 'simulation.py' file. In the later case, the file must be referenced to a folder inside the 'simulations' folder through the 'path' parameter, containing a 'config.json' file with the parameters of the simulation, a 'data' folder to store the data for each run of the algorithm and a 'figures' folder to store the figures.
