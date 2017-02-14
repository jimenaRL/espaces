import numpy as np

from espaces import espaces
from ee_utils import cartesian

def compute_s2e1():

    ir_params = {  'ev_params'      : {'space':'s2e1', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e2,
                   'sampling_rate'  : 44100,
                }

    for _ in range(10):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = tuple(np.random.uniform(20,2000,2).tolist())
        espaces(ir_params)

def compute_h2e1():

    ir_params = {  'ev_params'      : {'space':'h2e1', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 44100,
                }

    for _ in range(10):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = tuple(np.random.uniform(20,2000,1).tolist())
        espaces(ir_params)

def compute_s3():

    ir_params = {  'ev_params'      : {'space':'s3', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 5.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 44100,
                }

    for _ in range(1):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = [10.]
        espaces(ir_params)

def compute_e3():

    ir_params = {  'ev_params'      : {'space':'e3', 'c':3.4e2, 'j_max': 15},
                   'duration'       : 5.0,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 44100,
                }


    for _ in range(1):
        ir_params['ev_params']['F'] = np.array([20., 20., 20.])
        print "\n--------%s--------\n" % ir_params
        espaces(ir_params)


def compute_cube():

    from ee_utils import get_paths
    import copy
    from green_fn import compute_green_fn_cube
    from signals import Signal

    for _ in range(10):

        ir_params = {  'ev_params'    : {'space':'cube', 'c':3.4e2, 'j_max': 10},
                     'duration'       : 15.0,
                     'nu'             : 1.7e-5 * .75e3,
                     'sampling_rate'  : 44100,
                  }

        ir_params['ev_params']['F'] = tuple(np.random.uniform(20,200,3).tolist())


        # set save paths results
        path_kwargs = copy.deepcopy(ir_params['ev_params'])
        path_kwargs.update({'duration' : ir_params['duration'],
                            'nu'       : ir_params['nu'] })
        paths  = get_paths(**path_kwargs)
        au_path = paths.get('audio')


        # compute ir
        cube_params = ir_params
        cube_params.update(cube_params['ev_params'])
        del cube_params['space']
        del cube_params['ev_params']

        cube_params['x_t'] = tuple(np.random.uniform(0,100,3).tolist())
        cube_params['x_0'] = tuple(np.random.uniform(0,100,3).tolist())

        print "\n--------%s--------\n" % cube_params

        green_fn = compute_green_fn_cube(**cube_params)

        ir_signal = Signal(green_fn,fs=cube_params['sampling_rate'],mono=True,normalize=True)

        au_path = au_path.split('.wav')[0]
        au_path += '_x_0_'+'_'.join([("%i" % x) for x in cube_params['x_0']])
        au_path += '_x_t_'+'_'.join([("%i" % x) for x in cube_params['x_t']])
        au_path += '.wav'
        ir_signal.write(au_path)
        print "Audio file saved at %s." % au_path

        # save ir image
        if 'image' in paths:
            im_path = paths.get('image')
            im_path = im_path.split('.png')[0]
            im_path += '_x_0_'+'_'.join(["1.1%f" % x for x in cube_params['x_0']])
            im_path += '_x_t_'+'_'.join(["1.1%f" % x for x in cube_params['x_t']])
            im_path += '.png'
            ir_signal.save_image(im_path, title='impulse response')



if __name__:

    # compute_cube()
    # compute_s2e1()
    # compute_h2e1()
    compute_s3()
    # compute_e3()
