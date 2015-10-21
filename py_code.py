# All units in International System of Units (SI)

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

def compute_green_fn(c,nu,eigen_vals,duration,sampling_rate,im_path,au_path):
    """ Computes the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c               : [float] sound velocity
        nu              : [float] kinematic viscosity
        eigen_vals      : [list of floats] eigen values of the manifold M
        duration        : [float] duration of the Green function in seconds
        sampling_rate   : [int]   sampling rate of the output sound
        im_path         : [string] prefixe name to save image without extention
        au_path         : [string] prefixe name to save audio without extention
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

    # # save function in a .txt file for Max input
    # file_name = name + '.txt'
    # with open(file_name, 'w') as f:
    #     for t in range(dur_points):
    #         f.write('%i,%f\n' % (t,green_fn_0[t]))

    ## plot and save Green function
    t_plot  = np.linspace(0.0, duration,dur_points)
    fig, ax = plt.subplots(1,figsize=(8, 8))

    ax.plot(t_plot,green_fn_0,'g')
    ax.set_title('1-torus Green function at x=0')
    ax.set_xlabel('seconds')

    im_path += '.png'
    fig.savefig(im_path)
    print 'Figure saved at %s' % im_path
    # plt.show()

    # save Green function as .wav audio file
    au_path  += '.wav'
    scaled_green_fn_0 = np.int16(green_fn_0/np.max(np.abs(green_fn_0)) * 32767)
    wavfile.write(au_path, sampling_rate, scaled_green_fn_0)
    print 'Audio saved at %s' % au_path

    return au_path

def eigen_vals_1_torus(c,L,j_max):
    """ Computes the Green function at x=0 of the wave equation 
        in a manifold M defined by its eigen-values.

        c     : [float] sound velocity
        L     : [float] length of the torus
        j_max : [int] number of eigen-values to compute
    """
    eigen_vals = [ np.square(2*np.pi*j/L) for j in range(-j_max,j_max+1)]
    return eigen_vals

def convolve(audio_path_1,audio_path_2, cv_path, mode='full'):
    # read audio
    sr_1, audio_1 = wavfile.read(audio_path_1)
    sr_2, audio_2 = wavfile.read(audio_path_2)
    assert(sr_1==sr_2)
    # convert to mono
    if len(audio_1.shape)==2:
        audio_1 = audio_1[:,0]
    if len(audio_2.shape)==2:
        audio_2 = audio_2[:,0]
    # convolve signals
    conv_signal = signal.fftconvolve(audio_1, audio_2, mode=mode)

    # save audio
    scaled_conv_signal = np.int16(conv_signal/np.max(np.abs(conv_signal)) * 32767)
    cv_path += '.wav'
    wavfile.write(cv_path, sr_1, scaled_conv_signal)

    print 'Audio saved at %s' % cv_path

if __name__:

    ## set parameters
    sound_speed   = 3.4e2
    viscosity     = 1.7e-5

    duration      = 5.0
    sampling_rate = 44100.0

    torus_length_list  = np.linspace(1e-2,1e4,50) # [1e-2,1e-1,1e-0,1e1,1e2,1e3,1e4]

    j_max = 10 # 100 #int(np.square(sound_speed/viscosity)) -> j_max to big : memory allocation error

    mode = 'full'
    sound_example_path = '/Users/jimena/Zsound/projects/espaces_project/data/examples/speech.wav'

    im_folder =  '/Users/jimena/Zsound/projects/espaces_project/data/generated/green_fn/images/'
    au_folder =  '/Users/jimena/Zsound/projects/espaces_project/data/generated/green_fn/audio/'
    cv_folder = '/Users/jimena/Zsound/projects/espaces_project/exps/convolutions/20151021_python/'

    for L in torus_length_list:
        file_name  = 'green_function_from_eigen_vals_j_max_%i_torus_length_%1.2f_%1.1f_sec' % (j_max,L,duration)

        # green fn
        im_path    = os.path.join(im_folder,file_name)
        au_path    = os.path.join(au_folder,file_name)
        eigen_vals = eigen_vals_1_torus(sound_speed,L,j_max)
        sound_files_path = compute_green_fn(c=sound_speed,nu=viscosity, eigen_vals=eigen_vals,
                                            duration=duration, sampling_rate=sampling_rate,
                                            im_path=im_path, au_path=au_path)

        # cv
        cv_path = os.path.join(cv_folder,file_name)
        convolve(au_path+'.wav',sound_example_path, cv_path, mode)
