import os, sys, time
import tempfile

from ee_utils import ESPACES_PROJECT

# All units in International System of Units (SI)

from impulse_reponse import get_ir
from eigenvalues import get_eigenvalues
from green_fn import *
from espaces import espaces

def test_ir():
    ir_params = { 'ev_params'       : {'space':'e3', 'F':[0.1,0.1,0.1], 'j_max':1},
                   'duration'       : 0.01,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 44100,
                }
    get_ir(ir_params)

def test_eigenvalues():
    get_eigenvalues({'space':'e3'  , 'F':[0.1,0.1,0.1], 'j_max':2})
    get_eigenvalues({'space':'s3'  , 'F':[0.1], 'c':3.4e2})
    get_eigenvalues({'space':'h2e1', 'F':[0.1], 'kind':3})
    get_eigenvalues({'space':'s2e1', 'F':[0.1,0.1], 'unused_kwarg':'unused_kwarg'})

def test_compute_green_fn():
    compute_green_fn(c=1, nu=1,  eigen_vals=[{'multiplicity':1, 'value':1}], duration=0.1,sampling_rate=8000)
    compute_green_fn_cube(x_t=[1,1,1],x_0=[1,-1,0],c=1, nu=1,F=[440.,440.,440.],j_max=2,duration=0.1,sampling_rate=8000)


def test_espaces():
    ir_params = { 'ev_params'       : {'space':'s3', 'F':[0.1], 'j_max':1,},
                   'duration'       : 0.01,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 44100,
                }
    espaces(ir_params)


def notest_signals_conv():

    from convolutions import convolve_signals
    from signals import Signal

    test_track = os.path.join(ESPACES_PROJECT, "dev", "ir", "data", "speech.wav")

    args = {"normalize": True, "mono": True}
    sig = Signal(test_track, **args)
    file_name = os.path.basename(sig.location)
    assert sig.data.shape[0] == sig.length
    assert sig.data.shape[1] == sig.n_chan
    assert sig.length > sig.n_chan

    args = {"normalize": True, "mono": True}
    sigmono = Signal(test_track, **args)
    assert sigmono.n_chan == 1

    with tempfile.NamedTemporaryFile(suffix='.mp3') as output_file:
        sigmono.write(output_file.name)

    convolve_signals(sig,sig,mode='full',kind='ss')


def profiling():

    from cProfile import Profile
    from pstats import Stats

    ir_params = {  'ev_params'      : {'space':'e3', 'F': [0.1,0.1,0.1], 'j_max':30},
                   'duration'       : 1,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 8000,
                }

    p = Profile()
    p.runcall(lambda : get_ir(ir_params))
    stats = Stats(p, stream=sys.stdout)
    stats.sort_stats('time')
    stats.print_stats(10)

if __name__=='__main__':
    pass
    # profiling()
