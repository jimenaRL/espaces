#
#                                                                            */
#                               core.py                                      */
#                                                                            */
#                        Deezer deep learning                                */
#                                                                            */
# -------------------------------------------------------------------------- */


# All units in International System of Units (SI)

import os
import sys

import numpy as np
from scipy import signal

from scipy.io import wavfile
import matplotlib.pyplot as plt

from pyo import *

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def open_osx(*args):
    """ """
    if sys.platform=='darwin':
        for arg in args:
            os.system("open %s" % arg)
    else:
        raise StandardError("open_osx only implemente for mac osx")

def save_max_format(array,file_name):
    """ Saves a numpy array or list in a file file for Max ~pfft object """
    with open(file_name, 'w') as f:
        for t in range(len(array)):
            f.write('%i,%f\n' % (t,array[t]))

def save_image(array,duration,file_name,title=''):
    """ Saves and plot an image of a numpy array or list associated with an audio source.

        array        : [numpy array or list] numpy array or list to save 
        duration     : [float] duration in seconds associated to array
    """

    ## plot and save Green function
    t_plot  = np.linspace(0.0, duration, len(array))
    fig, ax = plt.subplots(1,figsize=(8, 8))

    ax.plot(t_plot,array,'g')
    ax.set_title(title)
    ax.set_xlabel('seconds')

    fig.savefig(file_name)
    print 'Figure saved at %s' % file_name

def save_audio(array,sampling_rate,file_name,show=False):
    """ Saves an audio file of a numpy array or list associated with an audio source.

        array        : [numpy array or list] numpy array or list to save 
        duration     : [float] duration in seconds associated to array
    """
    scaled_array = np.int16(array/np.max(np.abs(array)) * 32767)
    wavfile.write(file_name, sampling_rate, scaled_array)
    print 'Audio saved at %s' % file_name

def read_audio(path,mono=False):
    # read audio
    sr, audio = wavfile.read(path)
    # convert to mono
    if mono and len(audio.shape)==2:
        audio = audio[:,0]
    return sr, audio

def play_audio(path,mono=False):
    # read audio
    sr, audio = wavfile.read(path)
    # convert to mono
    if mono and len(audio.shape)==2:
        audio = audio[:,0]
    return sr, audio
