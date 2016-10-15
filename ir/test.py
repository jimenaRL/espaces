import os
import tempfile

# from utils import  open_osx

# from convolutions import convolve_signals
from signals import Signal
# from espaces import espaces

ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def test_eigenvalues():
    from eigenvalues import eigenvalues
    eigenvalues({'space':'e3'  , 'F':[0.1,0.1,0.1], 'j_max':2})
    eigenvalues({'space':'s3'  , 'F':[0.1], 'c':1})
    eigenvalues({'space':'h2e1', 'F':[0.1], 'kind':3})
    eigenvalues({'space':'s2e1', 'F':[0.1,0.1], 'unused_kwarg':'unused_kwarg'})

def test_compute_green_fn():
    from green_fn import compute_green_fn
    compute_green_fn(c=1, nu=1,  eigen_vals=[{'multiplicity':1, 'value':1}], duration=0.1,sampling_rate=8000)

def test_signals():

    test_track = os.path.join(ESPACES_PROJECT, "dev", "ir", "data", "crash.wav")

    args = {"normalize": False, "mono": False}
    sig = Signal(test_track, **args)
    file_name = os.path.basename(sig.location)
    assert sig.data.shape[0] == sig.length
    assert sig.data.shape[1] == sig.n_chan
    print sig.length, sig.n_chan
    assert sig.length > sig.n_chan

    args = {"normalize": False, "mono": True}
    sigmono = Signal(test_track, **args)
    assert sigmono.n_chan == 1

    with tempfile.NamedTemporaryFile(suffix='.mp3') as output_file:
        sigmono.write(output_file.name)

# def test(save=False,open=False):

#     # ordinary impulse reponse 
#     path_ir = os.path.join(ESPACES_PROJECT,'data','examples','ir.wav')
#     sig_ir = Signal(path_ir,mono=True)

#     # audio example
#     path_ex = os.path.join(ESPACES_PROJECT,'data','examples','speech.wav')
#     sig_ex = Signal(path_ex,mono=True)

#     # convolved signal
#     mode = 'full' # 'full' or 'valid' or 'same'
#     kind = 'ola' # 'ola' or 'ss'
#     sig_cv = convolve_signals(sig_ex, sig_ir, mode, kind)

#     # save audio and image
#     for name in ['ex','ir','cv']:
#         if save:
#             save_path = os.path.join(ESPACES_PROJECT,'data','examples','to_erase_'+name+'_'+kind)
#             save_au = save_path+'_'+mode+'.wav'
#             save_im = save_path+'_'+mode+'.png'
#             sig = locals()['sig_'+name]
#             sig.write(save_au)
#             sig.save_image(save_im, title=name+' '+mode+' '+kind)
#         if open:
#             open_osx(save_au,save_im)

# def profiling():
#     import time
#     import sys
#     from cProfile import Profile
#     from pstats import Stats

#     p = Profile()
#     p.runcall(test)
#     stats = Stats(p, stream=sys.stdout)
#     stats.sort_stats('time')
#     stats.print_stats(10)

