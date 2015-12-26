#
#                                                                            */
#                           convolutions.py                                  */
#                                                                            */
#                       Espaces Imaginaires sound project                    */
#                                                                            */
# -------------------------------------------------------------------------- */

import scipy.signal as ss
import numpy as np
import signals

def convolve_audio(array_1,array_2,mode='full'):
    """ Convolves two 1-dim arrays using fftconvolve from scipy.signal 
    """
    if not array_1.ndim==1==array_2.ndim:
        raise ValueError('Both arrays to convolve must be one dimensional.')
    if len(array_1) > len(array_2):
        conv_signal = ss.fftconvolve(array_1, array_2, mode=mode)
    else:
        conv_signal = ss.fftconvolve(array_2,array_1,mode=mode)
    return conv_signal

def convolve_signals(sig_1,sig_2,mode='full'):
    """ TO WRTITE """
    if not sig_1.fs==sig_2.fs:
        raise ValueError('Both signals to convolve must have the same sampling rate.')
    cv = convolve_audio(sig_1.data[:,0],sig_2.data[:,0],mode='full')
    return signals.Signal(cv,sig_1.fs)

def convolve_paths(audio_path_1,audio_path_2,mode='full'):
    """ TO WRTITE """
    # read audio and convert to mono
    sr_1, audio_1 = read_audio(audio_path_1,mono=True)
    sr_2, audio_2 = read_audio(audio_path_2,mono=True)
    if not sr_1==sr_2:
        raise ValueError("Convolve between two audio files only implemented for equal sampling rates." 
                         "Got sr_1 = %s and sr_2 = %s" % (str(sr_1),str(sr_2)))
    # return convolution signal
    return convolve(audio_1,audio_2,mode=mode)

def convolve(data_1,data_2,mode='full'):
    if not type(data_1)==type(data_2):
        raise ValueError("Both datas to convolve must be of same type. Got %s, %s." % (type(data_1),type(data_2)))
    if isinstance(data_1,str):
        return convolve_paths(data_1,data_2,mode)
    elif isinstance(data_1,np.ndarray):
        return convolve_audio(data_1,data_2,mode)
    elif isinstance(data_1,signals.Signal):
        return convolve_signals(data_1,data_2,mode)
    else:
        raise ValueError("Wrong data types to convolve. Got %s" % type(data_1))
