#
#                                                                            */
#                             espaces.py                                     */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os
from datetime import date

import numpy as np
import scipy

from utils import save_image, save_audio, read_audio, play_audio, open_osx

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

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
    green_fn_0  = np.sum(np.array([ np.exp( (-1) * ev_j * nu * t_discret ) * np.cos( np.sqrt(ev_j) * c *  np.sqrt(1-(ev_j*nu*nu/(c*c))) * t_discret)
                                    for ev_j in eigen_vals]), axis = 0)

    return green_fn_0

def eigen_vals_1_torus(c,L,j_max):
    """ Returns the eigen-values of a 1-torus in a list. 

        c     : [float] sound velocity
        L     : [float] length of the torus
        j_max : [int] absolute value of maximun eigen-value to compute
    """
    return [ np.square(2*np.pi*j/L) for j in range(-j_max,j_max+1) ]

def convolve(array_1,array_2,mode='full'):
    """ Convolves two 1-dim arrays using fftconvolve from scipy.signal
 
    """
    if not array_1.ndim==1==array_2.ndim:
        raise ValueError('Both arrays to convolve must be one dimensional.')
    if len(array_1) > len(array_2):
        conv_signal = scipy.signal.fftconvolve(array_1, array_2, mode=mode)
    else:
        conv_signal = scipy.signal.fftconvolve(array_2,array_1,mode=mode)
    return conv_signal

def convolve_from_paths(audio_path_1,audio_path_2,mode='full'):
    """ Convolves two audio files using fftconvolve from scipy.signal.
        Optionally save convolved signal.
    """ 
    # read audio and convert to mono
    sr_1, audio_1 = read_audio(audio_path_1,mono=True)
    sr_2, audio_2 = read_audio(audio_path_2,mono=True)
    if not sr_1==sr_2:
        raise ValueError("Convolve between two audio files only implemented for equal sampling rates." 
                         "Got sr_1 = %s and sr_2 = %s" % (str(sr_1),str(sr_2)))
    # return convolution signal
    return convolve(audio_1,audio_2,mode=mode)

def set_folders():
    """ """

    results_path = os.path.join(ESPACES_PROJECT,'data','results',date.today().isoformat())

    folders = {}

    folders['green_fn_im'] = os.path.join(results_path,'green_fn','images')
    folders['green_fn_au'] = os.path.join(results_path,'green_fn','audio')

    folders['cv_im'] = os.path.join(results_path,'conv_result','images')
    folders['cv_au'] = os.path.join(results_path,'conv_result','audio')

    folders['es_im'] = os.path.join(results_path,'emitted_sound','images')
    folders['es_au'] = os.path.join(results_path,'emitted_sound','audio')

    for key in folders:
        if not os.path.exists(folders[key]):
            os.makedirs(folders[key])

    return folders

def set_paths(type,torus_j_max=None,L=None,duration=None):
    """ """
    if type=='green_fn':
        name  = 'green_function_from_eigen_vals_j_max_%i_torus_length_%1.2f_%1.1f_sec' % (torus_j_max,L,duration)
        im_folder = set_folders()['green_fn_im']
        au_folder = set_folders()['green_fn_au']
    elif type=='cv':
        name = 'conv_j_max_%i_torus_length_%1.2f_%1.1f_sec' % (torus_j_max,L,duration)
        im_folder = set_folders()['cv_im']
        au_folder = set_folders()['cv_au']
    elif type=='es':
        name = 'emitted_sound'
        im_folder = set_folders()['es_im']
        au_folder = set_folders()['es_au']
    return os.path.join(im_folder,name+'.png'), os.path.join(au_folder,name+'.wav')

def espaces(torus_j_max,L,duration,emitted_sound_path):

    ## set physical parameters
    sound_speed   = 3.4e2
    viscosity     = 1.7e-5

    # set saving paths
    gf_im_path, gf_au_path = set_paths('green_fn',torus_j_max,L,duration)
    cv_im_path, cv_au_path = set_paths('cv',torus_j_max,L,duration)
    es_im_path, es_au_path = set_paths('es')

    # read and save audio for emitted sound
    sampling_rate, emitted_sound = read_audio(emitted_sound_path,mono=True)
    save_image(emitted_sound, len(emitted_sound)/np.float64(sampling_rate), es_im_path, title='es')
    save_audio(emitted_sound, sampling_rate, es_au_path)

    # compute 1-torus eigen-values
    print "\tcomputing 1-torus eigen-values..."
    eigen_vals = eigen_vals_1_torus(sound_speed,L,torus_j_max)

    # compute and save green function
    print "\tcomputing green function..."
    green_fn_0 = compute_green_fn(sound_speed, viscosity, eigen_vals, duration, sampling_rate)
    save_image(green_fn_0, duration, gf_im_path,title='es')
    save_audio(green_fn_0, sampling_rate, gf_au_path)

    # convolve emitted sound with the green function and save it
    print "\tperforming convolution..."
    cv_sound = convolve(green_fn_0,emitted_sound,mode='valid')
    save_image(cv_sound, len(cv_sound)/sampling_rate, cv_im_path, title='cv')
    save_audio(cv_sound, sampling_rate, cv_au_path)

    # look at results
    open_osx(cv_im_path,es_im_path,gf_im_path,es_au_path,gf_au_path,cv_au_path)

if __name__:

    # set files paths
    emitted_sound_path = os.path.join(ESPACES_PROJECT,'data','examples','bd01.wav')
 
    # ## settings 
    # # NOTE : the physical bound for the 1-torus eigen-values is
    # #              int(np.square(sound_speed/viscosity))
    # #        but this leads to a memory allocation error.
    torus_j_max   = 10
    torus_lengths = [100] # np.linspace(1e-2,1e4,10) # [1e-2,1e-1,1e-0,1e1,1e2,1e3,1e4]
    duration      = 2.0

    for L in torus_lengths: 
        print "\tlength : %1.2f" % L
        espaces(torus_j_max,L,duration,emitted_sound_path)
