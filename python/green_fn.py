#
#                                                                            */
#                              green_fn.py                                   */
#                                                                            */
#                      Espaces Imaginaires sound project                     */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np

import theano
import theano.tensor as T

def compute_green_fn_theano(c,nu,eigen_vals,duration,sampling_rate):

    # convert to correct type for precaution
    c  = np.array(c).astype(theano.config.floatX)
    nu = np.array(nu).astype(theano.config.floatX)
    sampling_rate = np.array(sampling_rate).astype(theano.config.floatX)
    time_step  = np.array(1/sampling_rate).astype(theano.config.floatX) 

    dur_points = np.int(duration/time_step)
    t_discret  = np.array([time_step*t for t in range(dur_points)]).astype(theano.config.floatX) 


    _t_discret = T.vector(dtype=theano.config.floatX)
    _pre_sum = []
    for ev_j in eigen_vals:
        _pre_sum.extend([   T.exp( (-1) * ev_j * nu * t_discret ) * 
                            np.cos( np.sqrt(ev_j) * c * np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret )
                        ])

    green_fn_0 = T.sum(_pre_sum, axis = 0)

    return  0


def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate):
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
    t_discret  = np.array([time_step*t for t in range(dur_points)])
    green_fn_0 = np.sum(np.array([ np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
                                    for ev_j in eigen_vals]), axis = 0)
    green_fn_0 = green_fn_0/np.max(np.abs(green_fn_0))
    return green_fn_0
