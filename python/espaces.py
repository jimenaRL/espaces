#
#                                                                            */
#                         espaces.py                                         */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os
import sys
import time

import numpy as np

from utils import set_paths, open_osx
from signals import Signal

from eigenvalues import n_torus
from green_fn import compute_green_fn
from convolutions import convolve_signals

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def espaces(path_es,torus_j_max=100,L=10,duration=1,torus_dim=1):

    ## set physical parameters
    sound_speed   = 3.4e2
    viscosity     = 1.7e-5

    for key in locals().keys():
        print '%s : %s' % (key,locals()[key])

    # set saving paths
    gf_im_path, gf_au_path = set_paths('green_fn',torus_j_max,L,duration)
    cv_im_path, cv_au_path = set_paths('cv',torus_j_max,L,duration)
    es_im_path, es_au_path = set_paths('es',torus_j_max,L,duration)

    # read and save audio for emitted sound
    sig_es = Signal(path_es,mono=True,normalize=True)
    sampling_rate = sig_es.fs

    # compute 1-torus eigen-values
    print "\tcomputing 1-torus eigen-values..."
    start_t = time.time()
    eigen_vals = n_torus(sound_speed,L,torus_j_max,torus_dim)
    print "eigen-values computation took %1f milliseconds" % ((time.time() -start_t)*1e3)

    # compute and save green function
    print "\tcomputing green function..."
    start_t = time.time()
    green_fn_0 = compute_green_fn(sound_speed, viscosity, eigen_vals, duration, sampling_rate)
    print "green_fn_0 computation took %1.3f seconds" % ((time.time() -start_t))
    sig_gf = Signal(green_fn_0,fs=sampling_rate,mono=True,normalize=True)


    # convolve emitted sound with the green function and save it
    print "\tperforming convolution..."
    start_t = time.time()
    sig_cv = convolve_signals(sig_es,sig_gf,kind='ola')
    print "convolution computation took %1f milliseconds" % ((time.time() -start_t)*1e3)

    # save audio and image
    print "\tsaving files..."
    sig_es.write(es_au_path)
    sig_es.save_image(es_im_path, title='emitted sound')

    sig_gf.write(gf_au_path)
    sig_gf.save_image(gf_im_path, title='green_fn_0')

    sig_cv.write(cv_au_path)
    sig_cv.save_image(cv_im_path, title='reverberated sound')

    # look at results
    open_osx(cv_au_path,cv_im_path,gf_au_path,gf_im_path,es_au_path,es_im_path)

if __name__:

    # set emited sound
    if len(sys.argv)>=2:
        path_es = sys.argv[1]
    else:
        path_es = os.path.join(ESPACES_PROJECT,'dev','snds','speech_small.wav')

    ## other settings 
    # NOTE : the physical bound for the 1-torus eigen-values is
    #              int(np.square(sound_speed/viscosity))
    #        but this leads to a memory allocation error.
    if len(sys.argv)>=3:
        torus_j_max = int(sys.argv[2])
    else:
        torus_j_max = [1000]

    if len(sys.argv)>=4:
        torus_lengths = [np.float32(sys.argv[3])]
    else:
        torus_lengths = [100]

    if len(sys.argv)>=4:
        duration = np.float32(sys.argv[4])
    else:
        duration  = 1.0

    if len(sys.argv)>=5:
        torus_dim = np.int32(sys.argv[4])
    else:
        torus_dim  = 1

    espaces(path_es,torus_j_max,torus_lengths,duration,torus_dim)