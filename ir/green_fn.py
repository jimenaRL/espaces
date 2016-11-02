#
#                                                                            */
#                              green_fn.py                                   */
#                                                                            */
#                      Espaces Imaginaires sound project                     */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os
from tqdm import tqdm
import numpy as np
from joblib import Memory

from ee_utils import ESPACES_PROJECT

# memory = Memory(cachedir=os.path.join(ESPACES_PROJECT,"data","joblib_cache"),verbose=1)

# @memory.cache
def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate,p=None):
    """ Returns the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : [list of dict] eigen-values and their multiplicities of a manifold M 
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int] sampling rate of the output
        p               : [str] type of normalisation TO EXPLAIN BETTER
    """

    # convert to correct type for precaution
    c  = np.float64(c)
    nu = np.float64(nu)

    # compute Green function
    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.linspace(0,duration,dur_points)

    green_fn_0 = np.zeros(dur_points)

    # import matplotlib.pyplot as plt

    for ev_j in tqdm(eigen_vals):
        value = ev_j['value']
        multiplicity = ev_j['multiplicity']
        green_fn_i = multiplicity * np.exp( (-1) * nu * value * t_discret ) * np.cos( np.sqrt(value) * c *  np.sqrt(1-(value*nu*nu/(c*c))) * t_discret)

        # normalisation l^p or l^infty
        if p is None:
            norm_i = 1
        elif int(p)==-1:
            norm_i = np.abs(green_fn_i).max()
        else:
            norm_i = ((green_fn_i**p).sum())**(1/p)

        green_fn_0 += (1/norm_i) * green_fn_i

    green_fn_0 /= np.abs(green_fn_0).max()

    # plt.figure()
    # plt.plot(green_fn_0)
    # plt.show()
    # print np.abs(green_fn_i_norm).max()

    return green_fn_0
