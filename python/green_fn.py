#
#                                                                            */
#                              green_fn.py                                   */
#                                                                            */
#                      Espaces Imaginaires sound project                     */
#                                                                            */
# -------------------------------------------------------------------------- */

from tqdm import tqdm
import numpy as np

def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate,sym=False):
    """ Returns the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : [list of floats] eigen-values of manifold, ranged in increasing order, multiplicity counted.
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int]   sampling rate of the output sound
    """

    # convert to correct type for precaution
    c  = np.float64(c)
    nu = np.float64(nu)

    # compute Green function
    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.linspace(0,duration,dur_points)

    green_fn_0 = np.zeros(dur_points)

    if sym:

        ev_j = np.prod(eigen_vals[0].flatten())
        green_fn_0 += np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
        for ev_j in  tqdm(eigen_vals[1:]): #eigen_vals[1:]: 
            ev_j = np.prod(ev_j.flatten())
            green_fn_0 += 2*np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)  


    else:

        for ev_j in tqdm(eigen_vals[0:]):
            ev_j = np.prod(ev_j.flatten())
            green_fn_0 += 2*np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)

    return green_fn_0
