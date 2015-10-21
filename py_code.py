import numpy as np
import matplotlib.pyplot as plt 

import numpy as np
from scipy.io import wavfile
# import scikits.audiolab

def compute_green_fn(c,nu,L,j_max,eigen_vals,duration,sampling_rate):
    """ Computes the Green function of the wave equation in a manifold M.
        It plots the Green function and save it in .txt file for Max input
        Version v2 coded on 20151011.
        All units in International System of Units (SI)

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : [list of floats] eigen values of the manifold M
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int]   sampling rate of the output sound
    """

    # convert to correct type for precaution
    c  = np.float64(c)
    nu = np.float64(nu)

    # define Green function
    time_step  = 1/np.float64(sampling_rate)
    dur_points = np.int(duration/time_step)
    t_discret  = np.array([time_step*t for t in range(dur_points)])
    green_fn_0  = np.sum(np.array([ np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
                                    for ev_j in eigen_vals]), axis = 0)

    ## save Green function
    name      = 'green_function_from_eigen_vals_j_max_%i_torus_length_%1.2f_%1.1f_sec' % (j_max,L,duration)

    # # save function in a .txt file for Max input
    # file_name = name + '.txt'
    # with open(file_name, 'w') as f:
    #     for t in range(dur_points):
    #         f.write('%i,%f\n' % (t,green_fn_0[t]))

    # plot and save image
    t_plot  = np.linspace(0.0, duration,dur_points)
    fig, ax = plt.subplots(1,figsize=(8, 8))

    ax.plot(t_plot,green_fn_0,'g')
    ax.set_title('1-torus Green function at x=0')
    ax.set_xlabel('seconds')

    fig_name = 'image/'+name+'.png'
    fig.savefig(fig_name)
    print 'Saved %s' % fig_name
    #plt.show()

    ### WRITE .wav AUDIO FILE HERE ###
    sound_name  = 'audio/'+name+'.wav'
    scaled_green_fn_0 = np.int16(green_fn_0/np.max(np.abs(green_fn_0)) * 32767)
    wavfile.write(sound_name, sampling_rate, scaled_green_fn_0)
    scaled_green_fn_0 = np.int16(green_fn_0/np.max(np.abs(green_fn_0)) * 32767)
    print 'Saved %s' % sound_name


if __name__:

    # All units in International System of Units

    sound_speed   = 3.4e2
    viscosity     = 1.7e-5

    duration      = 10.0
    sampling_rate = 44100.0

    torus_length_list  = [1e-2,1e-1,1e-0,1e1,1e2,1e3,1e4]

    # # v2 version 
    j_max = 100 #int(np.square(sound_speed/viscosity)) -> j_max to big : memory allocation error
    for L in torus_length_list:
        eigen_vals = [ np.square(2*np.pi*j/L) for j in range(-j_max,j_max+1)]
        compute_green_fn_v2(c=sound_speed,nu=viscosity,L=L,j_max=j_max,
                            eigen_vals=eigen_vals,
                            duration=duration,sampling_rate=sampling_rate)
