import dolfin as df
from scipy.interpolate import interp2d
import numpy as np


def build_fem_PP(T_surf, L_surf, G_surf, mesh_size_x, mesh_size_y):
    """
    dffefe
    """
    Lx = T_surf.shape[1]
    Ly = T_surf.shape[0]

    # Sub domain for Periodic boundary condition
    class PeriodicBoundary(df.SubDomain):

        # Left boundary is "target domain" G
        def inside(self, x, on_boundary):
            # return True if on left or bottom boundary AND NOT on one of the two corners (0, 1) and (1, 0)
            return bool((df.near(x[0], 0) or df.near(x[1], 0)) and
                        (not ((df.near(x[0], 0) and df.near(x[1], Ly)) or
                              (df.near(x[0], Lx) and df.near(x[1], Ly)))) and on_boundary)

        def map(self, x, y):
            if df.near(x[0], Lx) and df.near(x[1], Ly):
                y[0] = x[0] - float(Lx)
                y[1] = x[1] - float(Ly)
            elif df.near(x[0], float(Lx)):
                y[0] = x[0] - float(Lx)
                y[1] = x[1]
            else:   # near(x[1], 1)
                y[0] = x[0]
                y[1] = x[1] - float(Ly)

    #Define diffusion coefficient as user expression
    class TableLookupCoefficient(df.UserExpression):
        def __init__(self, surf, Lx, Ly, **kwargs):
            super().__init__(**kwargs)
            self.surf = surf
            # self.Lx = Lx
            # self.Ly = Ly

        def eval(self, values, x):
            values[0] = self.surf(x[0], x[1]).item()

        def value_shape(self):
            return ()

    #Interpolate surfaces
    x_surf = np.linspace(0, Lx-1, Lx)
    y_surf = np.linspace(0, Ly-1, Ly)

    Tinv_surf = interp2d(x_surf, y_surf, 1 / T_surf)
    L2_surf = interp2d(x_surf, y_surf, L_surf ** 2)
    G_surf = interp2d(x_surf, y_surf, G_surf)

    #Instantiate coefficients
    tinv = TableLookupCoefficient(Tinv_surf, Lx, Ly)  # CHARACTERISTIC TIME
    l2 = TableLookupCoefficient(L2_surf, Lx, Ly)  # CHARACTERISTIC LENGTH
    g = TableLookupCoefficient(G_surf, Lx, Ly)  # SOURCE

    # Create mesh and finite elements
    mesh = df.RectangleMesh(df.Point(0.0, 0.0), df.Point(
        float(Lx), float(Ly)), mesh_size_x, mesh_size_y)
    V = df.FunctionSpace(mesh, "CG", 1, constrained_domain=PeriodicBoundary())
    bc = []

    # Define variational functions
    u = df.TrialFunction(V)
    v = df.TestFunction(V)

    # Define variational problem
    a = df.dot(l2 * (tinv/4) * df.grad(u), df.grad(v))*df.dx
    L = (u * -tinv + g)*v*df.dx
    F = a - L
    u_ = df.Function(V)
    F = df.action(F, u_)
    J = df.derivative(F, u_, u)

    # Compute solution
    u = df.Function(V)
    problem = df.NonlinearVariationalProblem(F, u_, bc, J)
    solver = df.NonlinearVariationalSolver(problem)
    solver.solve()

    return u_
