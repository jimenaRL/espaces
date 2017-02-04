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
def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate):
    """ Returns the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : [list of dict] eigen-values and their multiplicities of a manifold M 
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int] sampling rate of the output
    """

    # convert to correct type for precaution
    c  = np.float64(c)
    nu = np.float64(nu)

    # compute Green function
    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.linspace(0,duration,dur_points)

    green_fn_0 = np.zeros(dur_points)

    for ev_j in tqdm(eigen_vals):
        value = ev_j['value']
        multiplicity = ev_j['multiplicity']
        green_fn_i = multiplicity * np.exp( (-1) * nu * value * t_discret ) * np.cos( np.sqrt(value) * c *  np.sqrt(1-(value*nu*nu/(c*c))) * t_discret)
        green_fn_0 += green_fn_i

    return green_fn_0
