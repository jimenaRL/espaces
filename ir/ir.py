#
#                                                                            */
#                            ir.py                                           */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)
import copy

from eigenvalues import get_eigenvalues
from green_fn import compute_green_fn
from signals import Signal


def _check_params(params):

    default_params = {'nu': 1.7e-5, 'sampling_rate': 8000}

    for key in ['ev_params','duration']:
        if not key in params:
            raise ValueError('Missing key "%s" in eigenvalues params : %s' % (key,params))

    params.update({k:v if not k in params else params[k]  for k,v in default_params.items()})

    return params

def get_ir(ir_params):
    """
        Computes the impulse reponse (ir) associated with a the Green function at x=0
        of the wave equation in a manifold M defined by its eigen-values.
        
        Return an instance of the class Signal containing the Green function at given
        sampling rate.

        ir_params : [dict] dictionary containing params

                    {  'ev_params'      : {'space':'e3', 'F': [0.1,0.1,0.1], 'j_max':1},
                       'duration'       : 0.1,
                       'nu'             : 1.7e-5,
                       'sampling_rate'  : 8000,
                    }
    """

    ir_params = _check_params(ir_params)
    eigen_vals, ev_params = get_eigenvalues(ir_params['ev_params'])
    ir_params_ = copy.deepcopy(ir_params)
    ir_params_.update({'eigen_vals':eigen_vals, 'c':ev_params['c']})
    del ir_params_['ev_params']

    green_fn_0 = compute_green_fn(**ir_params_)

    sig_gf = Signal(green_fn_0,fs=ir_params_['sampling_rate'],mono=True,normalize=True)

    return sig_gf, eigen_vals


