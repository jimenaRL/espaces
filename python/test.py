import os

from convolutions import convolve
from signals import Signal

from utils import  open_osx

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

if __name__:

    # impulse reponse 
    path_ir = os.path.join(ESPACES_PROJECT,'data','examples','ir_align1.wav')
    sig_ir = Signal(path_ir,mono=True)

    # audio example
    path_ex = os.path.join(ESPACES_PROJECT,'data','examples','man2_48.wav')
    sig_ex = Signal(path_ex,mono=True)

    # convolved signal
    sig_cv = convolve(sig_ir,sig_ex,mode='full')

    # save audio and image
    for name in ['ex','ir','cv']:
        save_path = os.path.join(ESPACES_PROJECT,'data','examples','to_erase_'+name)
        sig = locals()['sig_'+name]
        sig.write(save_path+'.wav')
        sig.save_image(save_path+'.png', title=name)

        open_osx(save_path+'.png',save_path+'.wav')