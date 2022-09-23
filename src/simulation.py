import json
from tools import plots as p
from tools import tools as t

def simulation(path, savefig=False, run=True, X=None):
    """
    Computes a collection of solutions to the 2D diffusion equation and plots the regime diagram.
    The X parameter is a patch used to plot the ratios of the parameters as seen in the appendix of the report, instead of the regime diagram.
    The data for each individual solution will be saved in a folder 'data' inside a folder located in the path parameter.
    If savefig=True, the figures will be automatically saved in a folder 'figures' in the path parameter.
    The run parameter is set in order to avoid rerunning a simulation when the data is already available.
    """
    #LOAD PARAMETERS IN CONFIG FILE
    with open(path + "config.json") as f:
        config = json.load(f)

    if X == None:
        #RUN AND SAVE DATA
        if run == True:
            t.run_simulation(path, config)

        #LOAD DATA
        order_parameter = t.load_simulation(path, config)

    else:
        order_parameter = t.run_simulation_ratios(path, config, X)
        p.plot_order_parameter_X(order_parameter, config, X, path=path, savefig=savefig)


path = "simulations/simulation_1/" #Must reference to a folder containing a config.json file, a figures folder and a data folder
simulation(path, savefig=True, run=True, X=None)