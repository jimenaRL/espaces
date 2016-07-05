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

# def fn(c,nu,ev_j,X):

#     return T.exp( (-1) * ev_j * nu * X ) * T.cos( T.sqrt(ev_j) * c *  T.sqrt(1-(ev_j*nu*nu/(c*c))) * X)


# def compute_green_fn_theano(c,nu,eigen_vals,duration,sampling_rate):

#     c  = np.float64(c)
#     nu = np.float64(nu)

#     time_step  = 1/np.float64(sampling_rate)
#     dur_points = np.int(duration/time_step)

#     X = T.constant(np.linspace(0,duration,dur_points)) # t_discret

#     components, updates = theano.scan( fn=fn,
#                                         outputs_info=None,
#                                         sequences=[eigen_vals],
#                                         non_sequences=[c,nu,X])
#     green_fn = components.sum()

#     return theano.function(inputs=[eigen_vals], outputs=green_fn)



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
        green_fn_0 += multiplicity*np.exp( (-1) * value * nu * t_discret ) * np.cos( np.sqrt(value) * c *  np.sqrt(1-(value*nu*nu/(c*c))) * t_discret)  

    return green_fn_0
