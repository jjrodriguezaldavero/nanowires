import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import dolfin as df
       
def plot_avg(surf, direction, title, hold=False): 
    """
    Plots the avg of the adatom distribution projected into the direction 0 or 1 as indicated in the 'direction' parameter.
    """
    try:
        avg = np.mean(surf, axis=direction)
    except:
        print("There was an error. Please specify a valid direction (x=0, y=1).")
    else:
        plt.figure() if hold == False else None
        plt.plot(avg)
        if direction == 0:
            plt.xlabel("Adsorption site x")
            plt.ylabel("Average site y occupation")
        elif direction == 1:
            plt.xlabel("Adsorption site y")
            plt.ylabel("Average site x occupation")
        plt.title(title)
        plt.show() if hold == False else None
    
def plot_fenics(u, title="Title"):
    """
    Plot the adatom distribution directly from the fenics solution instead of the sampled solution.
    """
    c = df.plot(u)
    plt.colorbar(c)
    plt.title(title)
    plt.show()

def plot_order_parameter(arr, config, fixed_variable1, fixed_variable2, path="", savefig=False):
    """
    Plot the regime diagram for the sampled solution
    """

    vals_ref = [1] + list(config["mask_parameters"].values())
    vals = list(config["simulation_parameters"].values())
    order_parameter_type = config["order_parameter_type"]

    names0 = ['d', 'T', 'L', 'G']
    names = [r'$d$', r'$\frac{t_{trench}}{t_{mask}}$', r'$L$', r'$\frac{G_{trench}}{G_{mask}}$']

    #Gets the indices of the two variables that are being fixed given their names
    axis_reduced = [names0.index(fixed_variable1[0]), names0.index(fixed_variable2[0])]

    #Gets the indices of the values of the variables that are being fixed given their values
    values_reduced = [
        vals[names0.index(fixed_variable1[0])].index(fixed_variable1[1]), \
        vals[names0.index(fixed_variable2[0])].index(fixed_variable2[1])]

    #Reduce the dimensionality of the 4D array by fixing two of the dimensions
    arr_reduced = np.take(np.take(arr, values_reduced[1], axis_reduced[1]), values_reduced[0], axis_reduced[0])

    #Finds the two axis that are not reduced
    axis_orig = [0,1,2,3]; axis_orig.pop(axis_reduced[1]); axis_orig.pop(axis_reduced[0])

    #Gets the relative values with respect to the reference
    vals_relative = [
        [d for d in vals[0]], 
        [T / vals_ref[1] for T in vals[1]], 
        [L for L in vals[2]], 
        [G / vals_ref[3] for G in vals[3]]]

    plt.figure()
    x = vals_relative[axis_orig[0]]
    for i in range(arr_reduced.shape[1]):
        y = arr_reduced[:,i]
        plt.plot(x,y, '-1')
        plt.text(x[0],y[0], '{}'.format(vals_relative[axis_orig[1]][i]))

    if order_parameter_type == 'ha':
        titlename = "Absolute height"
    elif order_parameter_type == 'hr':
        titlename = "Relative height"
    elif order_parameter_type == 'aa':
        titlename = "Absolute area"
    elif order_parameter_type == 'ar':
        titlename = "Relative area"
    else:
        titlename = ""
    plt.title("{} profile for {} = {}, {} = {}".format(
        titlename, 
        names[axis_reduced[0]], vals_relative[axis_reduced[0]][values_reduced[0]], 
        names[axis_reduced[1]], vals_relative[axis_reduced[1]][values_reduced[1]]))
    plt.xlabel("{}".format(names[axis_orig[0]]))
    plt.ylabel("{} difference (%)".format(titlename))
    plt.legend(vals_relative[axis_orig[1]], title="{}".format(names[axis_orig[1]]), bbox_to_anchor=(1, 1), loc="upper left")
    plt.axhline(y = 0.0, linestyle = 'dashed', color='gray')
    plt.axhspan(1.1*np.amin(arr_reduced), 0, facecolor='red', alpha=0.15)
    plt.axhspan(0, 1.1*np.amax(arr_reduced), facecolor='yellow', alpha=0.2)
    if savefig == True:
        plt.tight_layout()
        save_path = path + "figures/{}{}_{}{}".format(fixed_variable1[0], fixed_variable1[1], fixed_variable2[0], fixed_variable2[1])
        plt.savefig(save_path, dpi=199)
    plt.show()

def plot_order_parameter_X(arr, config, X, path="", savefig=False):
    """
    """
    names0 = ['d', 'T', 'L', 'G']
    names = [r'$d$', r'$\frac{t_{trench}}{t_{mask}}$', r'$\frac{L_{trench}}{L_{mask}}$', r'$\frac{G_{trench}}{G_{mask}}$']
    indices = [0, 1, 2, 3]
    index = names0.index(X)
    indices.pop(index)
    names0.remove(X)
    
    plt.figure()
    x = np.asarray(config["ratios_values"])
    for i in range(arr.shape[0]):
        y = arr[i]
        plt.plot(x,y,'-1')
        plt.text(x[-1],arr[i][-1], '{}'.format(x[i]))
    plt.legend(x, title=r"${}^{{mask}}$".format(X), bbox_to_anchor=(1, 1), loc="upper left")
    plt.axhline(y = 0.0, linestyle = 'dashed', color='gray')
    plt.axhspan(1.1*np.amin(arr), 0, facecolor='red', alpha=0.2)
    plt.axhspan(0, 1.1*np.amax(arr), facecolor='yellow', alpha=0.2)
    plt.xlabel(r"${}^{{trench}}$".format(X))
    plt.ylabel("Height difference (%)")
    plt.title("Height profile for {} = {}, {} = {}, {} = {}".format(
        names[indices[0]], 1.0,
        names[indices[1]], 1.0,
        names[indices[2]], 1.0
    ))
    if savefig == True:
        plt.tight_layout()
        save_path = path + "figures/{}".format(X)
        plt.savefig(save_path, dpi=199)
    plt.show()