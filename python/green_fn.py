#
#                                                                            */
#                              green_fn.py                                   */
#                                                                            */
#                      Espaces Imaginaires sound project                     */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np
try:
    import theano
    import theano.tensor as T
except:
    print "Unable to import thenao module."

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
    if 0: #'theano' in globals():
        T_t_discret  = T.vector(name='T_t_discret')
        T_green_fn_0 = T.vector(name='T_green_fn_0')
        for ev_j in eigen_vals:
            T_green_fn_0 += T.exp( (-1) * ev_j * nu * T_t_discret ) * T.cos( T.sqrt(ev_j) * c *  T.sqrt(1-(ev_j*nu*nu/(c*c))) * T_t_discret)
            return T_green_fn_0.eval({T_t_discret:t_discret})
    else: 
        green_fn_0 = np.zeros(dur_points)
        for ev_j in eigen_vals:
            green_fn_0 += np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
        # green_fn_0 = np.sum(np.array([ np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
        #                                 for ev_j in eigen_vals]), axis = 0)
        return green_fn_0
