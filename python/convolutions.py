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
import dzrutils

def convolve_ola(signal, impulse_response):
    """
    partitionned convolution (also known as "overlap and add method") of short Signal "impulse_response" with long Signal "signal"
    """
    x = signal.data
    h = impulse_response.data

    M = h.shape[0];
    N = np.ceil(x.shape[0]/float(M));
    Nfft = 2*M ;

    output_data = np.zeros((max(Nfft*np.ceil(N/2.0),M+Nfft*(N/2.0)), signal.n_chan));

    for k in range(signal.n_chan):
        x_buff = np.zeros((M,N));
        x = signal.data[:,k]
        h = impulse_response.data[:,k]

        if x.shape[0]%M == 0:
            x_buff[:,:] = x.reshape((M,N), order='F');
        else:
            x[0:np.floor(x.shape[0]/float(M))*M].reshape((M,np.floor(x.shape[0]/float(M))));
            x_buff[:,0:-1] = x[0:np.floor(x.shape[0]/float(M))*M].reshape((M,np.floor(x.shape[0]/float(M))), order='F');
            x_buff[0:x.shape[0]-np.floor(x.shape[0]/float(M))*M,-1] = x[np.floor(x.shape[0]/float(M))*M:];


        x_buff_ft = dzrutils.fft(x_buff, n=Nfft, axis=0)

        h_ft = dzrutils.fft(h, n=Nfft)

        cv_buff = np.real(dzrutils.ifft(h_ft.reshape((Nfft,1))*x_buff_ft, axis=0))

        cv = np.zeros(max(Nfft*np.ceil(N/2.0),M+Nfft*(N/2)));

        cv[0:Nfft*np.ceil(N/2.0)] = cv_buff[:,0::2].reshape((Nfft*np.ceil(N/2.0)), order='F')
        cv[M:M+Nfft*np.floor(N/2.0)] += cv_buff[:,1::2].reshape((Nfft*np.floor(N/2.0)), order='F')
        output_data[:,k] = cv;

    return signals.Signal(output_data, fs=signal.fs)

def convolve_scipy(sig_1,sig_2,mode='full'):
    """ Convolves two signals using fftconvolve from scipy.
    """
    if mode=='full':
        output_length = sig_1.length + sig_2.length - 1
    elif mode=='valid':
        if sig_2.length > sig_1.length:
            temp  = sig_1
            sig_1 = sig_2
            sig_2 = temp
        output_length = sig_1.length - sig_2.length + 1
    else:
        output_length = np.min((sig_1.length,sig_2.length))
    conv_data = np.zeros((output_length, sig_1.n_chan))
    for k in range(sig_1.n_chan):
        conv_data[:,k] = ss.fftconvolve(sig_1.data[:,k], sig_2.data[:,k], mode=mode)
    return signals.Signal(conv_data, fs=sig_1.fs)

def convolve_signals(sig_1,sig_2,mode='full',kind='ss'):
    """ TO WRITE """
    if sig_1.n_chan != sig_2.n_chan:
        raise ValueError("impulse response and signal must have the same number of channels")
    if sig_1.fs != sig_2.fs:
        raise ValueError("impulse response and signal must have the same sampling frequency")
    if kind=='ss':
        return convolve_scipy(sig_1,sig_2,mode)
    elif kind=='ola':
        return convolve_ola(sig_1,sig_2)