# FENICS diffusion solver

*Author: Juan José Rodríguez Aldavero*

Project to solve the modified diffusion equation representing the growth of semiconducting nanowires using the FENICS library for the internship in the Quantum Materials group led by Prof. Erik Bakkers, Department of Applied Physics at the University of Eindhoven.

This project solves the difussion equation with custom sources and sinks numerically, and argues that the equation models the growth of semiconducting nanowires. These nanowires form the basis of many groundbreaking quantum technologies such as topological quantum computers, and therefore insight into their growth regimes is of value. To know more, check out the Presentation.pdf and Report.pdf files.

**Installation**

Requires the installation of the FENICS/DOLFIN library, as well as numpy and json. The easiest way is by means of an Anaconda environment.

```bash
conda create -n fenicsproject -c conda-forge fenics
source activate fenicsproject
```

**Usage**

- Use the 'solution.py' to compute a single solution of the equation.
- Use the 'simulation.py' file to compute several solutions (for example plot the regime diagram depending on the nanowire height difference).
