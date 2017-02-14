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

from ee_utils import ESPACES_PROJECT, cartesian

def compute_green_fn_cube(c,nu,F,j_max,duration,sampling_rate,**kwargs):
    """ Returns the Green function of the wave equation in a perfect cube of size L.

        x_t             : [3-tuple] source position
        x_0             : [3-tuple] listen position
        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        F               : [3-tuple] contains c/l1, c/l2, c/l3, where l1, l2, l3 are the cube's lengths
        j_max           : [int] sets index of eigen-values to compute as {-j_max, ..., j_max} in each direction
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int] sampling rate of the output
    """

    # convert to correct type for precaution
    c  = np.float64(c)
    nu = np.float64(nu)
    F = np.array(F).astype("float64")

    # compute Green function
    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.linspace(0,duration,dur_points)
    green_fn_0 = np.zeros(dur_points)

    x = 0.5 * (2*np.pi/c) * F

    index_1 = range(-j_max, j_max+1, 1)
    index_1_plus = range(0, j_max+1, 1)
    index_3d = cartesian([index_1_plus, index_1, index_1])
    index_3d = [el for el in index_3d if not (el[0]==el[1]==el[2]==0)]

    for index in tqdm(index_3d):

        direction = (2*np.pi/c) * F * index
        value = np.dot(direction, direction)

        D = nu * value
        omega_square = c*c*value-(value*value*nu*nu)
        # use only audible eigen values correspondant to propagative solutions of sound equation
        if 0 < omega_square < 22050**2:
            omega = np.sqrt(omega_square)
            green_fn_0 += (1/omega) * np.exp(-D*t_discret) * np.sin(omega*t_discret) * np.cos(np.dot(direction,x))

    return green_fn_0

def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate, **kwargs):
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
        D = nu * value
        omega_square = c*c*value-(value*value*nu*nu)
        # use only audible eigen values correspondant to propagative solutions of sound equation
        if 0 < omega_square < 22050**2:
            omega = np.sqrt(omega_square)
            green_fn_0 += multiplicity * (1/omega) * np.exp(-D*t_discret) * np.sin(omega*t_discret)

    return green_fn_0


if __name__=='__main__':

    print 333
    c = 3.4*1e2
    nu = 0.085
    sampling_rate= 44100
    j_max = 5
    F = [40, 40,40]
    duration = 1

    compute_green_fn_cube(c,nu,F,j_max,duration,sampling_rate)