#
#                                                                            */
#                              green_fn.py                                   */
#                                                                            */
#                      Espaces Imaginaires sound project                     */
#                                                                            */
# -------------------------------------------------------------------------- */

from tqdm import tqdm
import numpy as np

import theano 
import theano.tensor as T


def compute_green_fn_theano(c,nu,eigen_vals,duration,sampling_rate):

    c  = np.float64(c)
    nu = np.float64(nu)

    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.linspace(0,duration,dur_points).reshape((1,dur_points))
    X = T.constant(t_discret)

    values = np.array([e['value'] for e in  eigen_vals]).astype('float32').reshape(len(eigen_vals),1)

    multiplicities = np.array([e['multiplicity'] for e in  eigen_vals]).astype('float32').reshape(len(eigen_vals),1)
    V = T.constant(values)

    EXP = T.sqrt(V*c*c-V*V*nu*nu)
    EXP_X = EXP*X

    theano_green_fn_0 = ( multiplicities * (T.exp( (-1) * nu * V*X ) * T.cos( T.sqrt(V) * c * T.sqrt(1-(V*nu*nu/c*c) ) * X ) ) ).sum(axis=0)

    return theano_green_fn_0.eval()


def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate,sym=False):
    """ Returns the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : TO DO 
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

    for ev_j in  tqdm(eigen_vals):
        value = ev_j['value']
        multiplicity = ev_j['multiplicity']
        green_fn_0 += multiplicity * np.exp( (-1) * nu * value * t_discret ) * np.cos( np.sqrt(value) * c *  np.sqrt(1-(value*nu*nu/(c*c))) * t_discret)  

    return green_fn_0
