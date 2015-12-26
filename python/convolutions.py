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


def filter_OLA(signal, impulse_response):
    """
    partitionned convolution (also known as "overlap and add method") of short audio signal "h" with long audio signal "x"
    """

    x = signal
    h = impulse_response

    M = h.shape[0];
    N = np.ceil(x.shape[0]/float(M));
    Nfft = 2*M ;

    # if impulse_response.n_chan != signal.n_chan:
    #     raise ValueError("impulse response and signal must have the same number of channels")

    # if impulse_response.fs != signal.fs:
    #     raise ValueError("impulse response and signal must have the same sampling frequency")

    output_data = np.zeros((max(Nfft*np.ceil(N/2.0),M+Nfft*(N/2.0)), 1));

    x_buff = np.zeros((M,N));

    if x.shape[0]%M == 0:
        x_buff[:,:] = x.reshape((M,N), order='F');
    else:
        x[0:np.floor(x.shape[0]/float(M))*M].reshape((M,np.floor(x.shape[0]/float(M))));
        x_buff[:,0:-1] = x[0:np.floor(x.shape[0]/float(M))*M].reshape((M,np.floor(x.shape[0]/float(M))), order='F');
        x_buff[0:x.shape[0]-np.floor(x.shape[0]/float(M))*M,-1] = x[np.floor(x.shape[0]/float(M))*M:];


    x_buff_ft = utils.fft(x_buff, n=Nfft, axis=0)

    h_ft = utils.fft(h, n=Nfft)

    cv_buff = np.real(utils.ifft(h_ft.reshape((Nfft,1))*x_buff_ft, axis=0))

    cv = np.zeros(max(Nfft*np.ceil(N/2.0),M+Nfft*(N/2)));

    cv[0:Nfft*np.ceil(N/2.0)] = cv_buff[:,0::2].reshape((Nfft*np.ceil(N/2.0)), order='F')
    cv[M:M+Nfft*np.floor(N/2.0)] += cv_buff[:,1::2].reshape((Nfft*np.floor(N/2.0)), order='F')
    output_data[:,k] = cv

    return output_data

def scipy_signal(array_1, array_2,mode='full'):
    """ Convolves two 1-dim arrays using fftconvolve from scipy.
        The length of the convolved array is given by the convolution mode as

        'full'  -> len(array_1)+len(array_2)-1
        'same'  -> len(array_1)-len(array_2)+1
        'valid' -> max(len(array_1),len(array_2))

    """ 
    if len(array_1) > len(array_2):
        conv_signal = ss.fftconvolve(array_1, array_2, mode=mode)
    else:
        conv_signal = ss.fftconvolve(array_2,array_1,mode=mode)
    return conv_signal

def convolve_audio(array_1,array_2,mode='full',kind='ss'):
    """ TO WRITE """
    if not array_1.ndim==1==array_2.ndim:
        raise ValueError('Both arrays to convolve must be one dimensional.')

    if kind=='ss':
        return scipy_signal(array_1, array_2,mode)
    elif kind=='ola':
        return filter_OLA(array_1, array_2)

def convolve_signals(sig_1,sig_2,mode='full',kind='ss'):
    """ TO WRITE """
    if not sig_1.fs==sig_2.fs:
        raise ValueError('Both signals to convolve must have the same sampling rate.')
    cv = convolve_audio(sig_1.data[:,0],sig_2.data[:,0],mode=mode,kind=kind)
    return signals.Signal(cv,sig_1.fs)

def convolve_paths(audio_path_1,audio_path_2,mode='full',kind='ss'):
    """ TO WRTITE """
    # read audio and convert to mono
    sr_1, audio_1 = read_audio(audio_path_1,mono=True)
    sr_2, audio_2 = read_audio(audio_path_2,mono=True)
    if not sr_1==sr_2:
        raise ValueError("Convolve between two audio files only implemented for equal sampling rates." 
                         "Got sr_1 = %s and sr_2 = %s" % (str(sr_1),str(sr_2)))
    # return convolution signal
    return convolve(audio_1,audio_2,mode=mode,kind=kind)

def convolve(data_1,data_2,mode='full',kind='ss'):
    if not type(data_1)==type   (data_2):
        raise ValueError("Both datas to convolve must be of same kind. Got %s, %s." % (kind(data_1),kind(data_2)))
    if isinstance(data_1,str):
        return convolve_paths(data_1,data_2,mode,kind)
    elif isinstance(data_1,np.ndarray):
        return convolve_audio(data_1,data_2,mode,kind)
    elif isinstance(data_1,signals.Signal):
        return convolve_signals(data_1,data_2,mode,kind)
    else:
        raise ValueError("Wrong data kinds to convolve. Got %s" % kind(data_1))
